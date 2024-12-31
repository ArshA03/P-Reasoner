const socket = io();
const messageContainer = document.getElementById('messageContainer');
const userInput = document.getElementById('userInput');
const sendButton = document.getElementById('sendButton');
const reasoningToggle = document.getElementById('reasoningToggle');

let isReasoningMode = false;

function addMessage(content, sender) {
    const messageDiv = document.createElement('div');
    messageDiv.classList.add('message', `${sender}-message`);
    if (isReasoningMode && sender === 'bot') {
        messageDiv.classList.add('reasoning-mode-active');
    }
    messageDiv.textContent = content;
    messageContainer.appendChild(messageDiv);
    messageContainer.scrollTop = messageContainer.scrollHeight;
}

function addMessage(content, sender) {
    const messageDiv = document.createElement('div');
    messageDiv.classList.add('message', `${sender}-message`);
    messageDiv.textContent = content;
    messageContainer.appendChild(messageDiv);
    messageContainer.scrollTop = messageContainer.scrollHeight;
}

function showTypingIndicator() {
    const indicator = document.createElement('div');
    indicator.classList.add('typing-indicator');
    indicator.innerHTML = '<span></span><span></span><span></span>';
    messageContainer.appendChild(indicator);
    messageContainer.scrollTop = messageContainer.scrollHeight;
    return indicator;
}

function sendMessage() {
    const message = userInput.value.trim();
    if (message) {
        addMessage(message, 'user');
        socket.emit('send_message', { message: message });
        userInput.value = '';
        
        const typingIndicator = showTypingIndicator();
        setTimeout(() => typingIndicator.remove(), 1000);
    }
}

reasoningToggle.addEventListener('change', () => {
    socket.emit('toggle_reasoning');
});

socket.on('reasoning_toggled', (data) => {
    isReasoningMode = data.enabled;
    // Visual feedback when mode changes
    const feedback = document.createElement('div');
    feedback.classList.add('message', 'bot-message', 'mode-change-message');
    feedback.textContent = `Reasoning mode ${isReasoningMode ? 'enabled' : 'disabled'}`;
    messageContainer.appendChild(feedback);
    setTimeout(() => feedback.remove(), 3000);
});


sendButton.addEventListener('click', sendMessage);
userInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') sendMessage();
});

socket.on('receive_message', (data) => {
    const typingIndicator = document.querySelector('.typing-indicator');
    if (typingIndicator) typingIndicator.remove();
    
    addMessage(data.message, 'bot');
});

// Add loading state handling
function setLoadingState(loading) {
    sendButton.disabled = loading;
    userInput.disabled = loading;
    reasoningToggle.disabled = loading;
    
    if (loading) {
        sendButton.classList.add('loading');
    } else {
        sendButton.classList.remove('loading');
    }
}

// Update send message function to handle loading state
function sendMessage() {
    const message = userInput.value.trim();
    if (message) {
        addMessage(message, 'user');
        socket.emit('send_message', { message: message });
        userInput.value = '';
        
        const typingIndicator = showTypingIndicator();
        setLoadingState(true);
        
        // Remove typing indicator after response is received
        socket.once('receive_message', () => {
            typingIndicator.remove();
            setLoadingState(false);
        });
    }
}