document.addEventListener('DOMContentLoaded', function () {
    const chatForm = document.getElementById('chat-form');
    const userInput = document.getElementById('user-input');
    const chatMessages = document.getElementById('chat-messages');

    if (chatForm && userInput && chatMessages) {
        chatForm.addEventListener('submit', function (e) {
            e.preventDefault();
            const message = userInput.value.trim();
            if (message) {
                addMessage('user', message);
                sendMessage(message);
                userInput.value = '';
            }
        });

        function addMessage(sender, message) {
            const messageDiv = document.createElement('div');
            messageDiv.classList.add('message-bubble', `${sender}-message`);
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
                body: `message=${encodeURIComponent(message)}`,
            })
                .then((response) => response.json())
                .then((data) => {
                    if (data.response) {
                        addMessage('bot', data.response);
                    } else {
                        addMessage('bot', 'Unexpected response. Please try again.');
                    }
                })
                .catch((error) => {
                    console.error('Error:', error);
                    addMessage('bot', 'There was an error. Please try again later.');
                });
        }
    } else {
        console.error('Required chat elements not found in the DOM');
    }
});
