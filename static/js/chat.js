document.addEventListener('DOMContentLoaded', () => {
    // Only initialize chat if we're on the chat page
    const chatContainer = document.querySelector('#chat-messages');
    if (!chatContainer) {
        console.log('Not on chat page, skipping initialization');
        return;
    }

    // Get DOM elements with error handling
    const elements = {
        chatForm: document.getElementById('chat-form'),
        userInput: document.getElementById('user-input'),
        chatMessages: document.getElementById('chat-messages'),
        timeElement: document.getElementById('current-time'),
        dateElement: document.getElementById('current-date')
    };

    // Verify all required elements exist
    const requiredElements = ['chatForm', 'userInput', 'chatMessages'];
    const missingElements = requiredElements.filter(key => !elements[key]);

    if (missingElements.length > 0) {
        console.error('Missing required elements:', missingElements.join(', '));
        return;
    }

    // Initialize time display
    function updateTimeDisplay() {
        const now = new Date();
        if (elements.timeElement) {
            elements.timeElement.textContent = now.toLocaleTimeString([], { 
                hour: '2-digit', 
                minute: '2-digit' 
            });
        }
        if (elements.dateElement) {
            elements.dateElement.textContent = now.toLocaleDateString();
        }
    }

    // Update time display initially and start interval
    updateTimeDisplay();
    const timeInterval = setInterval(updateTimeDisplay, 60000);

    // Cleanup on page unload
    window.addEventListener('unload', () => {
        clearInterval(timeInterval);
    });

    // Handle message submission
    elements.chatForm.addEventListener('submit', function(e) {
        e.preventDefault();
        const message = elements.userInput.value.trim();
        if (message) {
            addMessage('user', message);
            sendMessage(message);
            elements.userInput.value = '';
        }
    });

    // Add message to chat
    function addMessage(sender, message) {
        try {
            const messageContainer = document.createElement('div');
            messageContainer.className = `flex ${sender === 'user' ? 'justify-end' : 'justify-start'} mb-4`;
            
            const messageDiv = document.createElement('div');
            messageDiv.className = `rounded-lg px-4 py-2 max-w-[80%] ${
                sender === 'user' ? 'bg-primary text-white' : 'bg-[#fff7e4] text-blue-900'
            }`;
            messageDiv.textContent = message;
            
            messageContainer.appendChild(messageDiv);
            elements.chatMessages.appendChild(messageContainer);
            elements.chatMessages.scrollTop = elements.chatMessages.scrollHeight;
        } catch (error) {
            console.error('Error adding message to chat:', error);
            logError('Failed to add message to chat');
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
                throw new Error('Invalid response format');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            addMessage('bot', 'There was an error. Please try again later.');
            logError(error.message);
        });
    }

    // Log client-side errors
    function logError(errorMessage) {
        fetch('/log_error', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ error: errorMessage }),
        }).catch(err => console.error('Error logging:', err));
    }
});
