document.addEventListener('DOMContentLoaded', () => {
    const noteTakingMenu = document.getElementById('note-taking-menu');
    const noteQueryMenu = document.getElementById('note-query-menu');
    const noteTakingSection = document.getElementById('note-taking-section');
    const noteQuerySection = document.getElementById('note-query-section');
    const cleanupButton = document.getElementById('cleanup-button');
    const cleanupResponse = document.getElementById('cleanup-response');
    const cleanupResults = document.getElementById('cleanup-results');
    const propositionalizeButton = document.getElementById('propositionalize-button');
    
    const chatWindow = document.getElementById('chat-window');
    const chatInput = document.getElementById('chat-input');
    const sendButton = document.getElementById('send-button');
    
    // Sidebar navigation handling
    noteTakingMenu.addEventListener('click', () => {
      noteTakingMenu.classList.add('active');
      noteQueryMenu.classList.remove('active');
      noteTakingSection.classList.add('active');
      noteQuerySection.classList.add('hidden');
    });
    
    noteQueryMenu.addEventListener('click', () => {
      noteQueryMenu.classList.add('active');
      noteTakingMenu.classList.remove('active');
      noteQuerySection.classList.remove('hidden');
      noteTakingSection.classList.remove('active');
    });
    
    // Handle cleanup button click
    cleanupButton.addEventListener('click', async () => {
      const notes = document.getElementById('notes-input').value;
      if (!notes.trim()) {
        return;
      }

      try {
        // Show loading state
        cleanupButton.disabled = true;
        cleanupButton.textContent = 'Processing...';
        cleanupResults.innerHTML = '';
        
        // Call the Python function through our bridge
        const result = await window.api.processNote(notes);
        
        try {
          const propositions = JSON.parse(result);
          
          // Display each proposition
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
        // Reset button state
        cleanupButton.disabled = false;
        cleanupButton.textContent = 'Cleanup';
        // Show the results section
        cleanupResponse.classList.remove('hidden');
      }
    });

    // Handle propositionalize button click
    propositionalizeButton.addEventListener('click', async () => {
      const notes = document.getElementById('notes-input').value;
      if (!notes.trim()) {
        return;
      }

      try {
        // Show loading state
        propositionalizeButton.disabled = true;
        propositionalizeButton.textContent = 'Processing...';
        cleanupResults.innerHTML = '';
        
        // Call the Python function through our bridge
        const result = await window.api.processNote(notes);
        
        try {
          const propositions = JSON.parse(result);
          
          // Display each proposition
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
        // Reset button state
        propositionalizeButton.disabled = false;
        propositionalizeButton.textContent = 'Propositionalize';
        // Show the results section
        cleanupResponse.classList.remove('hidden');
      }
    });
    
    // Handle chat session
    sendButton.addEventListener('click', () => {
      const message = chatInput.value.trim();
      if (message) {
        appendMessage('User', message);
        chatInput.value = '';
        
        // Simulate an assistant response (replace with your chat_session integration)
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