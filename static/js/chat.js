document.addEventListener('DOMContentLoaded', function () {
    const chatForm = document.getElementById('chat-form');
    const userInput = document.getElementById('user-input');
    const chatMessages = document.getElementById('chat-messages');

    if (!chatForm || !userInput || !chatMessages) {
        console.error('Required chat elements not found in DOM');
        return;
    }

    // Initialize chat interface
    function initializeChatInterface() {
        // Update time and date
        const timeElement = document.querySelector('.lucide-clock + span');
        const dateElement = document.querySelector('.lucide-calendar + span');
        if (timeElement && dateElement) {
            const now = new Date();
            timeElement.textContent = now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
            dateElement.textContent = now.toLocaleDateString();
        }
    }

    initializeChatInterface();
    // Update time every minute
    setInterval(initializeChatInterface, 60000);

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
        const messageContainer = document.createElement('div');
        messageContainer.classList.add('d-flex', sender === 'user' ? 'justify-content-end' : 'justify-content-start');
        
        const messageDiv = document.createElement('div');
        messageDiv.classList.add(
            'message-bubble',
            'rounded-lg',
            'p-3',
            'mb-2',
            sender === 'user' ? 'bg-primary text-white' : 'bg-light'
        );
        messageDiv.textContent = message;
        
        messageContainer.appendChild(messageDiv);
        chatMessages.appendChild(messageContainer);
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
