document.addEventListener('DOMContentLoaded', function() {
    // Get DOM elements
    const chatForm = document.getElementById('chat-form');
    const userInput = document.getElementById('user-input');
    const chatMessages = document.getElementById('chat-messages');
    const timeElement = document.getElementById('current-time');
    const dateElement = document.getElementById('current-date');

    // Check if required elements exist
    if (!chatForm || !userInput || !chatMessages) {
        console.error('Required chat elements not found in DOM');
        return;
    }

    // Initialize chat interface
    function initializeChatInterface() {
        if (timeElement && dateElement) {
            const now = new Date();
            timeElement.textContent = now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
            dateElement.textContent = now.toLocaleDateString();
        }
    }

    // Update time and date initially and every minute
    initializeChatInterface();
    setInterval(initializeChatInterface, 60000);

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
        const messageContainer = document.createElement('div');
        messageContainer.classList.add('flex', sender === 'user' ? 'justify-end' : 'justify-start');
        
        const messageDiv = document.createElement('div');
        messageDiv.classList.add(
            'rounded-lg',
            'px-4',
            'py-2',
            'max-w-[80%]',
            'mb-2',
            sender === 'user' ? 'bg-primary text-white' : 'bg-[#fff7e4] text-blue-900'
        );
        messageDiv.textContent = message;
        
        messageContainer.appendChild(messageDiv);
        chatMessages.appendChild(messageContainer);
        chatMessages.scrollTop = chatMessages.scrollHeight;
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
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            if (data.response) {
                addMessage('bot', data.response);
            } else {
                addMessage('bot', 'Unexpected response. Please try again.');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            addMessage('bot', 'There was an error. Please try again later.');
        });
    }
});
