document.addEventListener('DOMContentLoaded', function() {
    // Get DOM elements with error handling
    const chatForm = document.getElementById('chat-form');
    const userInput = document.getElementById('user-input');
    const chatMessages = document.getElementById('chat-messages');
    const timeElement = document.getElementById('current-time');
    const dateElement = document.getElementById('current-date');

    // Verify required elements exist
    const requiredElements = {
        'chat-form': chatForm,
        'user-input': userInput,
        'chat-messages': chatMessages
    };

    // Check for missing elements
    const missingElements = Object.entries(requiredElements)
        .filter(([_, element]) => !element)
        .map(([id]) => id);

    if (missingElements.length > 0) {
        console.error('Missing required elements:', missingElements.join(', '));
        return;
    }

    // Initialize chat interface
    function initializeChatInterface() {
        if (!timeElement || !dateElement) {
            console.warn('Time/date elements not found. Time display will be disabled.');
            return;
        }

        const now = new Date();
        timeElement.textContent = now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
        dateElement.textContent = now.toLocaleDateString();
    }

    // Update time and date initially and every minute
    initializeChatInterface();
    const timeUpdateInterval = setInterval(initializeChatInterface, 60000);

    // Cleanup interval on page unload
    window.addEventListener('unload', () => {
        clearInterval(timeUpdateInterval);
    });

    // Handle message submission
    chatForm.addEventListener('submit', function(e) {
        e.preventDefault();
        const message = userInput.value.trim();
        if (message) {
            addMessage('user', message);
            sendMessage(message);
            userInput.value = '';
        }
    });

    // Add message to chat
    function addMessage(sender, message) {
        try {
            const messageContainer = document.createElement('div');
            messageContainer.classList.add('flex', sender === 'user' ? 'justify-end' : 'justify-start', 'mb-4');
            
            const messageDiv = document.createElement('div');
            messageDiv.classList.add(
                'rounded-lg',
                'px-4',
                'py-2',
                'max-w-[80%]',
                sender === 'user' ? 'bg-primary text-white' : 'bg-[#fff7e4] text-blue-900'
            );
            messageDiv.textContent = message;
            
            messageContainer.appendChild(messageDiv);
            chatMessages.appendChild(messageContainer);
            chatMessages.scrollTop = chatMessages.scrollHeight;
        } catch (error) {
            console.error('Error adding message to chat:', error);
        }
    }

    // Send message to server
    function sendMessage(message) {
        fetch('/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: `message=${encodeURIComponent(message)}`,
        })
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            if (data.response) {
                addMessage('bot', data.response);
            } else {
                throw new Error('Unexpected response format');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            addMessage('bot', 'There was an error. Please try again later.');
            // Log client-side error
            fetch('/log_error', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ error: error.message }),
            }).catch(err => console.error('Error logging:', err));
        });
    }
});
