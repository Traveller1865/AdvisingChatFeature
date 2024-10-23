document.addEventListener('DOMContentLoaded', function() {
    // Update time and date
    function updateDateTime() {
        const timeElement = document.getElementById('current-time');
        const dateElement = document.getElementById('current-date');
        if (timeElement && dateElement) {
            const now = new Date();
            timeElement.textContent = now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
            dateElement.textContent = now.toLocaleDateString();
        }
    }
    
    // Update time every minute
    updateDateTime();
    const timeInterval = setInterval(updateDateTime, 60000);

    // Chat functionality
    const chatForm = document.getElementById('chat-form');
    const userInput = document.getElementById('user-input');
    const chatMessages = document.getElementById('chat-messages');

    if (chatForm && userInput && chatMessages) {
        chatForm.addEventListener('submit', function(e) {
            e.preventDefault();
            const message = userInput.value.trim();
            if (message) {
                addMessage('user', message);
                sendMessage(message);
                userInput.value = '';
            }
        });
    }

    function addMessage(sender, message) {
        const messageContainer = document.createElement('div');
        messageContainer.className = `flex ${sender === 'user' ? 'justify-end' : 'justify-start'} mb-4`;
        
        const messageDiv = document.createElement('div');
        messageDiv.className = `rounded-lg px-4 py-2 max-w-[80%] ${
            sender === 'user' ? 'bg-primary text-white' : 'bg-[#fff7e4] text-blue-900'
        }`;
        messageDiv.textContent = message;
        
        messageContainer.appendChild(messageDiv);
        chatMessages.appendChild(messageContainer);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    function sendMessage(message) {
        fetch('/chat/message', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: 'message=' + encodeURIComponent(message)
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok: ' + response.status);
            }
            return response.json();
        })
        .then(data => {
            if (data && data.response) {
                addMessage('bot', data.response);
            } else if (data && data.error) {
                throw new Error('Server error: ' + data.error);
            } else {
                throw new Error('Invalid response from server');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            addMessage('bot', 'Sorry, there was an error processing your request. Please try again.');
        });
    }

    // Clean up interval on page unload
    window.addEventListener('unload', () => {
        clearInterval(timeInterval);
    });
});
