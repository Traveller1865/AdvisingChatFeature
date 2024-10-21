document.addEventListener('DOMContentLoaded', function() {
    const chatForm = document.getElementById('chat-form');
    const userInput = document.getElementById('user-input');
    const chatMessages = document.getElementById('chat-messages');

    chatForm.addEventListener('submit', function(e) {
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
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            if (data && data.response) {
                addMessage('bot', data.response);
            } else {
                throw new Error('Invalid response from server');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            addMessage('bot', 'Sorry, there was an error processing your request. Please try again later.');
        });
    }
});
