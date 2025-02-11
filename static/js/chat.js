document.addEventListener('DOMContentLoaded', function() {
    const chatForm = document.getElementById('chat-form');
    const userInput = document.getElementById('user-input');
    const chatMessages = document.getElementById('chat-messages');

    // Only initialize chat functionality if all required elements exist
    if (chatForm && userInput && chatMessages) {
        function addMessage(sender, message) {
            const messageDiv = document.createElement('div');
            messageDiv.classList.add('message', sender + '-message');
            messageDiv.textContent = message;
            chatMessages.appendChild(messageDiv);
            chatMessages.scrollTop = chatMessages.scrollHeight;
        }

        function sendMessage(message) {
            fetch('/chat', {
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
                    throw new Error('Invalid response from server: ' + JSON.stringify(data));
                }
            })
            .catch(error => {
                console.error('Error:', error);
                addMessage('bot', 'Sorry, there was an error processing your request. Please try again later.');
                logError(error);
            });
        }

        function logError(error) {
            fetch('/log_error', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({error: error.toString()})
            })
            .then(response => response.json())
            .then(data => console.log('Error logged:', data))
            .catch(err => console.error('Error logging failed:', err));
        }

        // Add event listener only if we're on the chat page
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
});
