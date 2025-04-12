document.addEventListener('DOMContentLoaded', function() {
    // Elements
    const aiToggleButton = document.getElementById('aiToggleButton');
    const aiSidebar = document.getElementById('aiSidebar');
    const aiCloseButton = document.getElementById('aiCloseButton');
    const aiForm = document.getElementById('aiForm');
    const aiInput = document.getElementById('aiInput');
    const aiSubmit = document.getElementById('aiSubmit');
    const aiMessages = document.getElementById('aiMessages');
    
    // Toggle sidebar
    aiToggleButton.addEventListener('click', function() {
        aiSidebar.classList.add('open');
        // Focus the input field when sidebar opens
        setTimeout(() => {
            aiInput.focus();
        }, 300);
    });
    
    // Close sidebar
    aiCloseButton.addEventListener('click', function() {
        aiSidebar.classList.remove('open');
    });
    
    // Handle form submission
    aiForm.addEventListener('submit', function(e) {
        e.preventDefault();
        
        const query = aiInput.value.trim();
        if (!query) return;
        
        // Disable input and button while processing
        aiInput.disabled = true;
        aiSubmit.disabled = true;
        
        // Show loading state
        aiSubmit.innerHTML = '<div class="ai-loading"></div>';
        
        // Add user message to chat
        addMessage(query, 'user');
        
        // Clear input
        aiInput.value = '';
        
        // Send query to backend
        fetch('/ai/query/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCsrfToken()
            },
            body: JSON.stringify({ query: query })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // Add AI response to chat
                addMessage(data.response, 'assistant');
            } else {
                // Add error message
                addMessage('Error: ' + (data.error || 'Something went wrong'), 'assistant error');
            }
        })
        .catch(error => {
            // Add error message
            addMessage('Error: ' + error.message, 'assistant error');
        })
        .finally(() => {
            // Re-enable input and button
            aiInput.disabled = false;
            aiSubmit.disabled = false;
            aiSubmit.innerHTML = '<i class="fas fa-paper-plane"></i>';
            aiInput.focus();
        });
    });
    
    // Function to add a message to the chat
    function addMessage(content, role) {
        const messageDiv = document.createElement('div');
        messageDiv.className = 'ai-message ' + role;
        
        const messageContent = document.createElement('div');
        messageContent.className = 'ai-message-content';
        messageContent.textContent = content;
        
        messageDiv.appendChild(messageContent);
        aiMessages.appendChild(messageDiv);
        
        // Scroll to bottom
        aiMessages.scrollTop = aiMessages.scrollHeight;
    }
    
    // Function to get CSRF token
    function getCsrfToken() {
        return document.querySelector('[name=csrfmiddlewaretoken]').value;
    }
    
    // Add initial welcome message
    addMessage('Hello! I\'m your inventory assistant. How can I help you today?', 'assistant');
});
