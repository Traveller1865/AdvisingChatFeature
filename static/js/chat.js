document.addEventListener('DOMContentLoaded', function () {
    const chatForm = document.getElementById('chat-form');
    const userInput = document.getElementById('user-input');
    const chatMessages = document.getElementById('chat-messages');
    const currentTimeEl = document.getElementById('current-time');
    const currentDateEl = document.getElementById('current-date');

    // Update time and date
    function updateDateTime() {
        const now = new Date();
        if (currentTimeEl) {
            currentTimeEl.textContent = now.toLocaleTimeString('en-US', { 
                hour: '2-digit', 
                minute: '2-digit'
            });
        }
        if (currentDateEl) {
            currentDateEl.textContent = now.toLocaleDateString('en-US', {
                month: '2-digit',
                day: '2-digit',
                year: 'numeric'
            });
        }
    }

    // Update immediately and then every minute
    updateDateTime();
    setInterval(updateDateTime, 60000);

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
            const messageContainer = document.createElement('div');
            messageContainer.classList.add('flex', sender === 'user' ? 'justify-end' : 'justify-start');
            
            const messageDiv = document.createElement('div');
            messageDiv.classList.add(
                'message-bubble',
                'rounded-lg',
                'px-4',
                'py-2',
                'max-w-[80%]',
                'mb-4',
                sender === 'user' ? 'bg-primary' : 'bg-[#fff7e4]',
                sender === 'user' ? 'text-white' : 'text-blue-900'
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
                .then((response) => {
                    if (!response.ok) {
                        throw new Error('Network response was not ok');
                    }
                    return response.json();
                })
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
