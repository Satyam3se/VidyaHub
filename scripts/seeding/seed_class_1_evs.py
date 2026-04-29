import os
import django
import sys

sys.path.append('c:/VidyaHub')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vidyahub.settings')
django.setup()

from main.models import Grade, Subject, Chapter, MCQQuestion

def seed_evs_questions():
    print("🌿 Seeding 30 EVS Questions for Class 1...")
    
    grade = Grade.objects.get(name='Class 1')
    subject = Subject.objects.get(grade=grade, slug='evs')
    chapter = Chapter.objects.get(subject=subject, slug='basics')

    MCQQuestion.objects.filter(chapter=chapter).delete()

    questions = [
        ("What do plants need to make food?", "Water only", "Sunlight only", "Sunlight, water & air", "Soil only", "C", "Plants need sunlight, water and air to make food."),
        ("Which animal gives us wool?", "Cow", "Sheep", "Goat", "Dog", "B", "Sheep gives us wool."),
        ("The process of water falling from clouds is called:", "Evaporation", "Rain", "Dew", "Snow", "B", "Rain is when water falls from clouds."),
        ("Which part of a plant makes food?", "Root", "Stem", "Leaf", "Flower", "C", "Leaves make food using sunlight."),
        ("Air is:", "Visible", "Invisible", "Yellow", "Solid", "B", "We cannot see air, it is invisible."),
        ("Which of these is a source of light?", "Moon", "Mirror", "Sun", "Cloud", "C", "The Sun is a natural source of light."),
        ("We breathe in:", "Carbon Dioxide", "Oxygen", "Nitrogen", "Smoke", "B", "Humans breathe in oxygen."),
        ("Which sense organ do we use to smell?", "Eyes", "Ears", "Nose", "Tongue", "C", "We use our nose to smell."),
        ("A cactus plant stores water in its:", "Leaves", "Roots", "Stem", "Flowers", "C", "Cactus stores water in its thick stem."),
        ("Which season is cold?", "Summer", "Monsoon", "Winter", "Spring", "C", "Winter is the cold season."),
        # 11-20
        ("The young one of a cat is called:", "Puppy", "Calf", "Kitten", "Foal", "C", "A baby cat is called a kitten."),
        ("Which is a natural resource?", "Plastic", "Glass", "Water", "Paper", "C", "Water is a natural resource from nature."),
        ("We should plant more trees because they give us:", "Rain", "Oxygen", "Rocks", "Sand", "B", "Trees give us oxygen to breathe."),
        ("What protects us from the sun's heat?", "Clouds", "Stars", "Moon", "Wind", "A", "Clouds block the sun's direct heat."),
        ("A tadpole grows into a:", "Fish", "Snake", "Frog", "Turtle", "C", "A tadpole is a baby frog."),
        ("We get milk from:", "Hen", "Cow", "Goat & Cow", "Fish", "C", "We get milk from both goat and cow."),
        ("Which is a water animal?", "Lion", "Tiger", "Fish", "Camel", "C", "Fish live in water."),
        ("Which part of the plant is underground?", "Flower", "Root", "Leaf", "Fruit", "B", "Roots are underground."),
        ("We should throw garbage in:", "River", "Road", "Dustbin", "Garden", "C", "Always throw garbage in a dustbin."),
        ("Caterpillar becomes a:", "Ant", "Bee", "Butterfly", "Spider", "C", "A caterpillar turns into a butterfly."),
        # 21-30
        ("Which animal can live on both land and water?", "Dog", "Frog", "Parrot", "Horse", "B", "A frog is an amphibian (land & water)."),
        ("We use raincoat during:", "Summer", "Winter", "Rain", "Night", "C", "Raincoats protect us from the rain."),
        ("What should we do to save water?", "Bathe 3 times a day", "Leave taps open", "Close taps when not in use", "Wash clothes in rivers", "C", "Closing taps saves water."),
        ("Which of these gives us fruits?", "Clouds", "Trees", "Rocks", "Rivers", "B", "Trees give us fruits."),
        ("The organ we use to taste is:", "Nose", "Tongue", "Skin", "Eyes", "B", "We taste with our tongue."),
        ("Where do birds live?", "Underground", "In the sea", "On trees/nests", "In deserts", "C", "Most birds live in nests on trees."),
        ("Which food gives us energy?", "Rice", "Stone", "Sand", "Air", "A", "Rice (carbohydrate) gives us energy."),
        ("Honey is made by:", "Ants", "Butterflies", "Bees", "Spiders", "C", "Bees make honey."),
        ("Sunlight, air and water are ___.", "Man-made", "Natural gifts", "Harmful", "Artificial", "B", "They are gifts of nature."),
        ("Earthworm helps the soil by:", "Polluting it", "Making it loose & fertile", "Drying it", "Hardening it", "B", "Earthworms loosen the soil for plants."),
    ]

    for i, q in enumerate(questions):
        MCQQuestion.objects.create(
            chapter=chapter,
            question_text=q[0],
            option_a=q[1],
            option_b=q[2],
            option_c=q[3],
            option_d=q[4],
            correct_option=q[5],
            explanation=q[6],
            order=i
        )
    print("✅ Successfully seeded 30 EVS questions!")

if __name__ == '__main__':
    seed_evs_questions()
