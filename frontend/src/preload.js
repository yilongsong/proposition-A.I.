const { contextBridge } = require('electron');
const { callPythonFunction, killCurrentProcess } = require('./bridge');

contextBridge.exposeInMainWorld(
  'api',
  {
    processNote: async (note) => {
      try {
        console.log('processNote called with:', note); // Add this
        const result = await callPythonFunction('process', note);
        console.log('processNote result:', result); // Add this
        return result;
      } catch (error) {
        console.error('Error in processNote:', error);
        throw error;
      }
    },
    savePropositions: async (data) => {
      try {
        const result = await callPythonFunction('save', data);
        return result;
      } catch (error) {
        console.error('Error saving propositions:', error);
        throw error;
      }
    },
    killProcess: () => {
      killCurrentProcess();
    }
  }
);