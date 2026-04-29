"""
VidyaHub Socket Server for Live Battles
Handles real-time multiplayer quiz battles between students
Class-based matchmaking: Class 1 students battle Class 1, JEE with JEE, etc.
"""
import socketio
import random
import json
import time
from main.models import MCQQuestion, Chapter, Subject, Profile
from main.utils import update_user_score
from django.contrib.auth.models import User

# Create a Socket.IO server with threading for async
sio = socketio.Server(
    async_mode='threading',
    cors_allowed_origins='*',
    cors_credentials=True,
    transports=['polling', 'websocket'],
    ping_timeout=60,
    ping_interval=25
)

# Matchmaking queue: {queue_key: [ {sid, user_id, username, grade, target_exam} ]}
# queue_key = f"{grade}_{target_exam}" or "global" for no specific group
matchmaking_queue = {}

# Active battles: {room_id: {players: [], questions: [], scores: {}, answered: [], subject_id: int}}
active_battles = {}

# User session mapping: {sid: {user_id, subject_id, username, grade, target_exam}}
user_sessions = {}

QUESTION_TIME = 15  # seconds per question
DELAY_BETWEEN_QUESTIONS = 2  # seconds

def get_queue_key(grade, target_exam, subject_id):
    """Generate matchmaking queue key based solely on subject to ensure players match!"""
    return f"subject_{subject_id}"

@sio.event
def connect(sid, environ):
    print(f"User connected: {sid}")
    user_sessions[sid] = {'user_id': None, 'subject_id': None, 'username': None, 'grade': None, 'target_exam': None}

@sio.event
def disconnect(sid):
    print(f"User disconnected: {sid}")
    
    # Get user info before removing
    session = user_sessions.get(sid, {})
    grade = session.get('grade')
    target_exam = session.get('target_exam')
    subject_id = session.get('subject_id')
    
    if grade or target_exam:
        queue_key = get_queue_key(grade, target_exam, subject_id)
        if queue_key in matchmaking_queue:
            matchmaking_queue[queue_key] = [p for p in matchmaking_queue[queue_key] if p['sid'] != sid]
            if not matchmaking_queue[queue_key]:
                del matchmaking_queue[queue_key]
    
    # Handle battle disconnection
    for room_id, battle in list(active_battles.items()):
        if sid in battle['players']:
            opponent_sid = battle['players'][0] if sid == battle['players'][1] else battle['players'][1]
            if opponent_sid:
                sio.emit('opponent_left', {'message': 'Opponent disconnected. You win!'}, room=opponent_sid)
            
            battle['scores'][sid] = battle['scores'].get(sid, 0)
            sio.emit('battle_end', {'scores': battle['scores'], 'reason': 'opponent_left'}, room=room_id)
            del active_battles[room_id]
            
            for player_sid in battle['players']:
                sio.leave_room(player_sid, room_id)
    
    if sid in user_sessions:
        del user_sessions[sid]

@sio.event
def join_battle(sid, data):
    subject_id = int(data.get('subject_id'))
    user_id = int(data.get('user_id'))
    
    # Get user info from database
    try:
        user = User.objects.get(id=user_id)
        profile = Profile.objects.get(user=user)
        username = user.username
        grade = profile.grade
        target_exam = profile.target_exam
    except (User.DoesNotExist, Profile.DoesNotExist):
        username = f"Player_{user_id}"
        grade = None
        target_exam = 'none'
    
    # Store session
    user_sessions[sid] = {
        'user_id': user_id,
        'subject_id': subject_id,
        'username': username,
        'grade': grade,
        'target_exam': target_exam
    }
    
    # Generate queue key based on class/exam
    queue_key = get_queue_key(grade, target_exam, subject_id)
    
    # Initialize queue for this group if needed
    if queue_key not in matchmaking_queue:
        matchmaking_queue[queue_key] = []
    
    # Check if already in queue
    in_queue = any(p['sid'] == sid for p in matchmaking_queue[queue_key])
    
    # Get queue description based on subject
    try:
        subject = Subject.objects.get(id=subject_id)
        queue_desc = f"{subject.name} Arena"
    except Subject.DoesNotExist:
        queue_desc = "Battle Arena"
    
    if not in_queue:
        matchmaking_queue[queue_key].append({
            'sid': sid,
            'user_id': user_id,
            'username': username,
            'grade': grade,
            'target_exam': target_exam,
            'subject_id': subject_id
        })
        sio.emit('queue_update', {
            'position': len(matchmaking_queue[queue_key]),
            'queue_type': queue_desc,
            'message': f'Waiting for opponent ({queue_desc})...'
        }, room=sid)
        # Schedule AI bot to join if no one else connects after 5 seconds
        def delayed_bot_spawn():
            sio.sleep(5)
            check_and_spawn_bot(queue_key, sid, subject_id)
            
        sio.start_background_task(delayed_bot_spawn)
    
    print(f"Player {username} joined queue: {queue_key} (total: {len(matchmaking_queue[queue_key])})")
    
    # Try to match two players from same queue
    if len(matchmaking_queue[queue_key]) >= 2:
        p1 = matchmaking_queue[queue_key].pop(0)
        p2 = matchmaking_queue[queue_key].pop(0)
        
        room_id = f"battle_{p1['sid']}_{p2['sid']}"
        
        sio.enter_room(p1['sid'], room_id)
        sio.enter_room(p2['sid'], room_id)
        
        start_battle(room_id, p1, p2, subject_id)

def check_and_spawn_bot(queue_key, sid, subject_id):
    """Spawns an AI bot if the user is still waiting in the queue"""
    if queue_key in matchmaking_queue:
        for i, p in enumerate(matchmaking_queue[queue_key]):
            if p['sid'] == sid:
                # User is still waiting! Remove them and start a bot match
                p1 = matchmaking_queue[queue_key].pop(i)
                
                print(f"No human opponent found. Spawning VidyaBot for {p1['username']}")
                
                bot_sid = f"bot_{sid}"
                p2 = {
                    'sid': bot_sid,
                    'user_id': 0,
                    'username': 'VidyaBot (AI)',
                    'grade': p1['grade'],
                    'target_exam': p1['target_exam'],
                    'subject_id': subject_id
                }
                
                room_id = f"battle_{p1['sid']}_{p2['sid']}"
                sio.enter_room(p1['sid'], room_id)
                # No need for bot to physically join a room
                
                start_battle(room_id, p1, p2, subject_id)
                
                # Start bot answer loop in background
                sio.start_background_task(bot_answer_loop, room_id, bot_sid)
                return

def bot_answer_loop(room_id, bot_sid):
    """Simulates an AI opponent answering questions"""
    last_q_idx = -1
    
    while True:
        battle = active_battles.get(room_id)
        if not battle:
            break
            
        current_q_idx = battle['current_q']
        
        # Ensure we are on a valid question and we haven't answered it yet
        if current_q_idx < len(battle['questions']) and current_q_idx != last_q_idx:
            # Wait a random time between 2 and 8 seconds to simulate thinking
            wait_time = random.uniform(2.0, 8.0)
            sio.sleep(wait_time)
            
            # Re-check battle state after waiting (might have been closed or advanced)
            battle = active_battles.get(room_id)
            if not battle or current_q_idx != battle['current_q'] or bot_sid in battle['answered']:
                continue
                
            q = battle['questions'][current_q_idx]
            
            # Bot answers correctly 60% of the time
            if random.random() < 0.6:
                bot_answer = q['correct']
            else:
                wrong_options = ['A', 'B', 'C', 'D']
                if q['correct'] in wrong_options:
                    wrong_options.remove(q['correct'])
                bot_answer = random.choice(wrong_options)
                
            # Submit answer
            submit_answer(bot_sid, {'room_id': room_id, 'answer': bot_answer})
            last_q_idx = current_q_idx
            
        sio.sleep(1)

def start_battle(room_id, p1, p2, subject_id):
    """Initialize and start a new battle with grade-appropriate questions"""
    
    # Determine which grade/exam questions to use
    p1_grade = p1.get('grade')
    p2_grade = p2.get('grade')
    p1_exam = p1.get('target_exam')
    p2_exam = p2.get('target_exam')
    
    # Use the higher grade if they differ, or fall back to subject
    from main.models import Subject
    try:
        subject = Subject.objects.get(id=subject_id)
        
        # Build query based on grade/exam
        questions_query = MCQQuestion.objects.filter(
            chapter__subject_id=subject_id
        )
        
        # If students have specific grades, prioritize those questions
        if p1_exam and p1_exam != 'none':
            # JEE/NEET/NDA - get questions from Class 11-12
            exam_grade_map = {'jee': ['Class 11', 'Class 12'], 'neet': ['Class 11', 'Class 12'], 'nda': ['Class 11', 'Class 12']}
            grades = exam_grade_map.get(p1_exam, ['Class 11', 'Class 12'])
            questions_query = questions_query.filter(
                chapter__subject__grade__name__in=grades
            )
        elif p1_grade:
            questions_query = questions_query.filter(
                chapter__subject__grade__name=p1_grade
            )
        
        # Get 5 random questions
        questions_query = questions_query.order_by('?')[:5]
        
    except Subject.DoesNotExist:
        questions_query = MCQQuestion.objects.filter(
            chapter__subject_id=subject_id
        ).order_by('?')[:5]
    
    questions = []
    for q in questions_query:
        questions.append({
            'id': q.id,
            'question': q.question_text,
            'options': [q.option_a, q.option_b, q.option_c, q.option_d],
            'correct': q.correct_option
        })
    
    if not questions:
        # Fallback: get any questions for this subject
        questions_query = MCQQuestion.objects.filter(
            chapter__subject_id=subject_id
        ).order_by('?')[:5]
        
        for q in questions_query:
            questions.append({
                'id': q.id,
                'question': q.question_text,
                'options': [q.option_a, q.option_b, q.option_c, q.option_d],
                'correct': q.correct_option
            })
    
    if not questions:
        sio.emit('battle_error', {'message': 'No questions available'}, room=p1['sid'])
        sio.emit('battle_error', {'message': 'No questions available'}, room=p2['sid'])
        return
    
    # Create battle state
    active_battles[room_id] = {
        'players': [p1['sid'], p2['sid']],
        'player_info': {p1['sid']: p1, p2['sid']: p2},
        'questions': questions,
        'current_q': 0,
        'scores': {p1['sid']: 0, p2['sid']: 0},
        'answered': [],  # List of sids who answered
        'start_times': {},  # When each player started the question
        'subject_id': subject_id
    }
    
    # Notify both players
    sio.emit('match_found', {
        'room_id': room_id,
        'opponent': p1['username'] if p2['sid'] == p1['sid'] else p2['username'],
        'your_username': p1['username']
    }, room=p1['sid'])
    
    sio.emit('match_found', {
        'room_id': room_id,
        'opponent': p2['username'] if p1['sid'] == p2['sid'] else p1['username'],
        'your_username': p2['username']
    }, room=p2['sid'])
    
    # Small delay before first question
    eventlet_sleep(1)
    send_next_question(room_id)

def send_next_question(room_id):
    """Send the next question to both players"""
    battle = active_battles.get(room_id)
    if not battle:
        return
    
    # Check if all questions done
    if battle['current_q'] >= len(battle['questions']):
        end_battle(room_id)
        return
    
    # Get current question
    q = battle['questions'][battle['current_q']]
    
    # Reset answered for new question
    battle['answered'] = []
    battle['start_times'] = {sid: None for sid in battle['players']}
    
    # Send question to both players
    for sid in battle['players']:
        # Shuffle options for each player
        options = q['options'][:]
        # Store original indices for answer checking
        original_correct = q['correct']
        
        # Send with timer info
        sio.emit('next_question', {
            'question': q['question'],
            'options': options,
            'q_index': battle['current_q'],
            'total_q': len(battle['questions']),
            'time_limit': QUESTION_TIME
        }, room=sid)

@sio.event
def submit_answer(sid, data):
    """Handle player answer submission"""
    room_id = data.get('room_id')
    answer = data.get('answer')  # 'A', 'B', 'C', 'D' or 'NONE' for timeout
    
    battle = active_battles.get(room_id)
    
    # Validation
    if not battle:
        return
    if sid not in battle['players']:
        return
    if sid in battle['answered']:
        return  # Already answered
    
    # Mark as answered
    battle['answered'].append(sid)
    
    # Get current question
    q = battle['questions'][battle['current_q']]
    is_correct = (answer == q['correct'])
    
    # Calculate score based on speed (first correct = 10, second correct = 5)
    points = 0
    if is_correct:
        if len(battle['answered']) == 1:
            points = 10  # First to answer correctly
        else:
            points = 5   # Second to answer correctly
        battle['scores'][sid] += points
    
    # Update score in DB
    try:
        session = user_sessions.get(sid, {})
        if session.get('user_id'):
            user = User.objects.get(id=session['user_id'])
            subject_id = battle['subject_id']
            update_user_score(user, subject_id, points)
    except Exception as e:
        print(f"Error updating score: {e}")
    
    # Notify about answer
    sio.emit('answer_result', {
        'player': sid,
        'is_correct': is_correct,
        'points': points,
        'your_score': battle['scores'][sid],
        'total_answered': len(battle['answered'])
    }, room=room_id)
    
    # Check if both answered - move to next question immediately
    if len(battle['answered']) >= 2:
        battle['current_q'] += 1
        # Shorter delay if both answered
        eventlet_sleep(1)
        send_next_question(room_id)

@sio.event
def time_up(sid, data):
    """Handle when a player's timer runs out"""
    room_id = data.get('room_id')
    battle = active_battles.get(room_id)
    
    if not battle or sid not in battle['players']:
        return
    if sid in battle['answered']:
        return
    
    # Mark as answered with no answer
    battle['answered'].append(sid)
    
    # Notify
    sio.emit('answer_result', {
        'player': sid,
        'is_correct': False,
        'points': 0,
        'your_score': battle['scores'].get(sid, 0),
        'total_answered': len(battle['answered']),
        'timeout': True
    }, room=room_id)
    
    # If both timed out or one answered and other timed out
    if len(battle['answered']) >= 2:
        battle['current_q'] += 1
        eventlet_sleep(1)
        send_next_question(room_id)

def end_battle(room_id):
    """End the battle and send final results"""
    battle = active_battles.get(room_id)
    if not battle:
        return
    
    # Calculate winner
    scores = battle['scores']
    p1_score = scores.get(battle['players'][0], 0)
    p2_score = scores.get(battle['players'][1], 0)
    
    if p1_score > p2_score:
        winner = battle['players'][0]
    elif p2_score > p1_score:
        winner = battle['players'][1]
    else:
        winner = None  # Draw
    
    # Send results to both
    result_data = {
        'scores': scores,
        'winner': winner,
        'p1_score': p1_score,
        'p2_score': p2_score,
        'total_questions': len(battle['questions'])
    }
    
    sio.emit('battle_end', result_data, room=room_id)
    
    # Clean up
    for sid in battle['players']:
        sio.leave_room(sid, room_id)
    
    del active_battles[room_id]

def eventlet_sleep(seconds):
    time.sleep(seconds)