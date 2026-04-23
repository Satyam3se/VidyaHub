document.addEventListener('DOMContentLoaded', () => {
    // Select elements
    const navbar = document.querySelector('.navbar');
    const mobileToggle = document.getElementById('mobileToggle');
    const mobileMenu = document.getElementById('mobileMenu');
    const navLinks = document.querySelectorAll('.nav-link, .mobile-link');

    // Scroll handler with throttle
    let lastScrollY = window.scrollY;
    let ticking = false;

    const updateNavbar = () => {
        if (window.scrollY > 50) {
            navbar.classList.add('scrolled');
        } else {
            navbar.classList.remove('scrolled');
        }
        
        ticking = false;
    };

    window.addEventListener('scroll', () => {
        if (!ticking) {
            window.requestAnimationFrame(() => {
                updateNavbar();
                ticking = false;
            });
            ticking = true;
        }
    });

    // Initial check
    updateNavbar();

    // Mobile menu toggle
    if (mobileToggle && mobileMenu) {
        mobileToggle.addEventListener('click', () => {
            const isActive = mobileToggle.classList.toggle('active');
            mobileMenu.classList.toggle('active');
            
            // Prevent scrolling when menu is open
            document.body.style.overflow = isActive ? 'hidden' : '';
        });
    }

    // Close mobile menu on link click
    navLinks.forEach(link => {
        link.addEventListener('click', () => {
            mobileToggle.classList.remove('active');
            mobileMenu.classList.remove('active');
            document.body.style.overflow = '';
        });
    });

    // Subtle parallax effect for hero if exists
    const hero = document.querySelector('.hero');
    if (hero) {
        window.addEventListener('scroll', () => {
            const scrolled = window.scrollY;
            if (scrolled < 1000) {
                hero.style.backgroundPositionY = `${scrolled * 0.5}px`;
            }
        });
    }
    // Initialize Lucide Icons
    if (window.lucide) {
        lucide.createIcons();
    }

    // Vidya AI Chatbot Logic
    const aiToggleBtn = document.getElementById('ai-toggle-btn');
    const aiCloseBtn = document.getElementById('ai-close-btn');
    const aiChatWindow = document.getElementById('ai-chat-window');
    const aiMessages = document.getElementById('ai-messages');
    const aiUserInput = document.getElementById('ai-user-input');
    const aiSendBtn = document.getElementById('ai-send-btn');

    // Global function to open Vidya AI
    window.openVidyaAI = (initialQuestion = null) => {
        if (!aiChatWindow) return;
        
        aiChatWindow.classList.remove('hidden');
        if (initialQuestion) {
            aiUserInput.value = initialQuestion;
            sendMessage();
        } else {
            aiUserInput.focus();
        }
    };

    // --- Embedded AI Logic ---
    const embeddedSection = document.getElementById('embedded-ai-section');
    const embeddedMessages = document.getElementById('embedded-ai-messages');
    const embeddedInput = document.getElementById('embedded-ai-input');
    const embeddedSend = document.getElementById('embedded-ai-send');

    window.triggerEmbeddedAI = (question) => {
        if (!embeddedSection) {
            // Fallback to floating if embedded not found
            window.openVidyaAI(question);
            return;
        }

        embeddedSection.classList.remove('hidden');
        embeddedSection.scrollIntoView({ behavior: 'smooth', block: 'center' });
        
        if (question) {
            sendEmbeddedMessage(question);
        } else {
            embeddedInput.focus();
        }
    };

    const sendEmbeddedMessage = async (text = null) => {
        const question = text || embeddedInput.value.trim();
        if (!question) return;

        if (!text) embeddedInput.value = '';

        appendMessageTo('embedded', 'user', question);
        const typingId = addTypingIndicatorTo('embedded');

        try {
            const response = await fetch('/api/ai/ask/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken')
                },
                body: JSON.stringify({ question: question })
            });

            const data = await response.json();
            removeIndicatorFrom('embedded', typingId);

            if (data.answer) {
                appendMessageTo('embedded', 'ai', data.answer);
            } else {
                appendMessageTo('embedded', 'ai', "I'm sorry, I encountered an error.");
            }
        } catch (error) {
            removeIndicatorFrom('embedded', typingId);
            appendMessageTo('embedded', 'ai', "Vidya AI is currently offline.");
        }
    };

    if (embeddedSend) {
        embeddedSend.addEventListener('click', () => sendEmbeddedMessage());
        embeddedInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') sendEmbeddedMessage();
        });
    }

    // Helper functions for multiple chat instances
    function appendMessageTo(type, sender, text) {
        const container = type === 'embedded' ? embeddedMessages : aiMessages;
        if (!container) return;
        
        const msgDiv = document.createElement('div');
        msgDiv.className = `message ${sender}-message`;
        msgDiv.innerHTML = text.replace(/\n/g, '<br>');
        container.appendChild(msgDiv);
        container.scrollTop = container.scrollHeight;
    }

    function addTypingIndicatorTo(type) {
        const container = type === 'embedded' ? embeddedMessages : aiMessages;
        if (!container) return;

        const id = 'typing-' + Date.now();
        const indicator = document.createElement('div');
        indicator.id = id;
        indicator.className = 'message ai-message typing-indicator';
        indicator.innerHTML = '<span></span><span></span><span></span>';
        container.appendChild(indicator);
        container.scrollTop = container.scrollHeight;
        return id;
    }

    function removeIndicatorFrom(type, id) {
        const indicator = document.getElementById(id);
        if (indicator) indicator.remove();
    }
    // --- End Embedded AI Logic ---

    // Send message function
    const sendMessage = async () => {
        const question = aiUserInput.value.trim();
        if (!question) return;

        // Clear input
        aiUserInput.value = '';

        // Add user message to UI
        appendMessageTo('floating', 'user', question);

        // Add typing indicator
        const typingId = addTypingIndicatorTo('floating');

        try {
            const response = await fetch('/api/ai/ask/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken')
                },
                body: JSON.stringify({ question: question })
            });

            const data = await response.json();
            removeIndicatorFrom('floating', typingId);

            if (data.answer) {
                appendMessageTo('floating', 'ai', data.answer);
            } else {
                appendMessageTo('floating', 'ai', "I'm sorry, I encountered an error. Please try again.");
            }
        } catch (error) {
            removeIndicatorFrom('floating', typingId);
            appendMessageTo('floating', 'ai', "Vidya AI is currently offline. Please check your connection.");
        }
    };

    if (aiToggleBtn && aiChatWindow) {
        // Toggle chat window
        aiToggleBtn.addEventListener('click', () => {
            aiChatWindow.classList.toggle('hidden');
            if (!aiChatWindow.classList.contains('hidden')) {
                aiUserInput.focus();
            }
        });

        aiCloseBtn.addEventListener('click', () => {
            aiChatWindow.classList.add('hidden');
        });

        aiSendBtn.addEventListener('click', sendMessage);
        aiUserInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') sendMessage();
        });
    }

    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
});
