const { contextBridge } = require('electron');
const { callPythonFunction } = require('./bridge');

// Explicitly expose the API
contextBridge.exposeInMainWorld(
  'api',
  {
    processNote: async (note) => {
      try {
        console.log('Processing note:', note); // Debug log
        const result = await callPythonFunction(note);
        console.log('Result:', result); // Debug log
        return result;
      } catch (error) {
        console.error('Error in processNote:', error);
        throw error;
      }
    }
  }
);