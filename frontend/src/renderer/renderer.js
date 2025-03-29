document.addEventListener('DOMContentLoaded', () => {
    // Get required DOM elements
    const elements = {
        propositionalizeButton: document.getElementById('propositionalize-button'),
        cleanupResults: document.getElementById('cleanup-results'),
        notesInput: document.getElementById('notes-input'),
        noteTakingMenu: document.getElementById('note-taking-menu'),
        noteQueryMenu: document.getElementById('note-query-menu'),
        savePropositionsButton: document.getElementById('save-propositions')
    };

    // Debug log to check which elements are missing
    Object.entries(elements).forEach(([name, element]) => {
        if (!element) {
            console.error(`Missing element: ${name}`);
        }
    });

    // Exit if required elements are missing
    if (!elements.propositionalizeButton || !elements.cleanupResults || !elements.notesInput) {
        console.error('Required elements not found. Check your HTML structure.');
        return;
    }

    // Auto-focus the text area on page load if we're in note-taking section
    if (document.getElementById('note-taking-section').classList.contains('active')) {
        elements.notesInput.focus();
    }

    // Add click handler for propositionalize button
    elements.propositionalizeButton.addEventListener('click', async () => {
        const notes = elements.notesInput.value;
        if (!notes.trim()) return;

        try {
            elements.propositionalizeButton.classList.add('processing');
            elements.propositionalizeButton.disabled = false;
            elements.cleanupResults.innerHTML = '';
            
            // Show split view and loading state
            document.querySelector('.note-taking-area').classList.add('split');
            document.querySelector('.proposition-review-area').classList.add('visible');
            
            // Reset and show loading message
            const loadingMessage = document.getElementById('loading-message');
            loadingMessage.style.display = '';
            loadingMessage.classList.remove('hidden');
            
            // Create handleStop function that can be removed later
            const handleStop = async () => {
                await window.api.killProcess();
                elements.propositionalizeButton.classList.remove('processing');
                loadingMessage.classList.add('hidden');
                
                // Collapse the bottom section
                document.querySelector('.note-taking-area').classList.remove('split');
                document.querySelector('.proposition-review-area').classList.remove('visible');
                
                // Clear any existing content
                elements.cleanupResults.innerHTML = '';
                
                // Clean up the event listener
                elements.propositionalizeButton.removeEventListener('click', handleStop);
            };

            // Add stop handler
            elements.propositionalizeButton.addEventListener('click', handleStop);
            
            try {
                const result = await window.api.processNote(notes);
                // Remove stop handler after successful completion
                elements.propositionalizeButton.removeEventListener('click', handleStop);
                
                const propositions = JSON.parse(result);
                
                // Hide loading message
                loadingMessage.classList.add('hidden');
                loadingMessage.style.display = 'none';
                
                // Show propositions
                propositions.forEach((proposition, index) => {
                    const div = document.createElement('div');
                    div.className = 'proposition-item';
                    div.innerHTML = `
                        <span class="proposition-number">${index + 1}.</span>
                        <span contenteditable="true">${proposition.proposition} <span class="label-text">(${proposition.label})</span></span>
                    `;
                    elements.cleanupResults.appendChild(div);
                });

            } catch (parseError) {
                // Remove stop handler in case of error
                elements.propositionalizeButton.removeEventListener('click', handleStop);
                console.error('Parse error:', parseError);
                throw new Error(`Failed to parse response: ${result}`);
            }
        } catch (error) {
            console.error('Error:', error);
            loadingMessage.classList.add('hidden');
            elements.cleanupResults.innerHTML = `<div class="error">Error: ${error.message}</div>`;
        } finally {
            elements.propositionalizeButton.classList.remove('processing');
            elements.propositionalizeButton.disabled = false;
        }
    });

    // Add click handlers for menu items
    elements.noteTakingMenu?.addEventListener('click', () => {
        elements.noteTakingMenu.classList.add('active');
        elements.noteQueryMenu.classList.remove('active');
        document.getElementById('note-taking-section').classList.add('active');
        document.getElementById('note-query-section').classList.add('hidden');
        elements.notesInput.focus(); // Add this line to focus the textarea
    });

    elements.noteQueryMenu?.addEventListener('click', () => {
        elements.noteQueryMenu.classList.add('active');
        elements.noteTakingMenu.classList.remove('active');
        document.getElementById('note-query-section').classList.remove('hidden');
        document.getElementById('note-taking-section').classList.remove('active');
    });

    // Handle cleanup button click
    const cleanupButton = document.getElementById('cleanup-button');
    const cleanupResults = document.getElementById('cleanup-results');
    const cleanupResponse = document.getElementById('cleanup-response');

    if (!cleanupResults || !cleanupResponse) {
        console.error('Required elements not found in the DOM');
        return;
    }

    cleanupButton.addEventListener('click', async () => {
        const notes = elements.notesInput.value;
        if (!notes.trim()) {
            return;
        }

        try {
            cleanupButton.disabled = true;
            cleanupButton.textContent = 'Processing...';
            cleanupResults.innerHTML = '';
            
            const result = await window.api.processNote(notes);
            
            try {
                const propositions = JSON.parse(result);
                
                propositions.forEach(({proposition, label}) => {
                    const li = document.createElement('li');
                    li.innerHTML = `<strong>${label}:</strong> ${proposition}`;
                    cleanupResults.appendChild(li);
                });
            } catch (parseError) {
                console.error('Parse error:', parseError);
                throw new Error('Failed to process response');
            }
            
        } catch (error) {
            console.error('Error:', error);
            cleanupResults.innerHTML = `<li class="error">Error: ${error.message}</li>`;
        } finally {
            cleanupButton.disabled = false;
            cleanupButton.textContent = 'Cleanup';
            cleanupResponse.classList.remove('hidden');
        }
    });

    // Handle save button click
    elements.savePropositionsButton?.addEventListener('click', async () => {
        const notes = elements.notesInput.value;
        const selectedPropositions = [];
        
        document.querySelectorAll('.proposition-item').forEach(item => {
            if (item.querySelector('.proposition-checkbox').checked) {
                const content = item.querySelector('.proposition-content');
                const label = content.querySelector('strong').textContent.replace(':', '');
                const proposition = content.textContent.substring(label.length + 2);
                selectedPropositions.push({
                    proposition: proposition,
                    label: label
                });
            }
        });

        if (selectedPropositions.length > 0) {
            try {
                elements.savePropositionsButton.disabled = true;
                elements.savePropositionsButton.textContent = 'Saving...';
                
                await window.api.savePropositions('save', {
                    note: notes,
                    propositions: selectedPropositions
                });
                
                alert('Propositions saved successfully!');
                
            } catch (error) {
                alert('Error saving propositions: ' + error.message);
            } finally {
                elements.savePropositionsButton.disabled = false;
                elements.savePropositionsButton.textContent = 'Save Selected';
            }
        }
    });

    // Handle chat session
    const chatWindow = document.getElementById('chat-window');
    const chatInput = document.getElementById('chat-input');
    const sendButton = document.getElementById('send-button');

    sendButton.addEventListener('click', () => {
        const message = chatInput.value.trim();
        if (message) {
            appendMessage('User', message);
            chatInput.value = '';
            
            setTimeout(() => {
                appendMessage('Assistant', 'This is a simulated response.');
            }, 500);
        }
    });
    
    chatInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            sendButton.click();
        }
    });
    
    function appendMessage(sender, text) {
        const messageDiv = document.createElement('div');
        messageDiv.classList.add('message');
        messageDiv.innerHTML = `<strong>${sender}:</strong> ${text}`;
        chatWindow.appendChild(messageDiv);
        chatWindow.scrollTop = chatWindow.scrollHeight;
    }
});