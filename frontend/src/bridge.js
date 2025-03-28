const { spawn } = require('child_process');
const path = require('path');

function callPythonFunction(action, data) {
  console.log('callPythonFunction called:', {action, data}); 
  return new Promise((resolve, reject) => {
    const pythonProcess = spawn('poetry', [
      'run',
      'python',
      '-c',
      `
import sys
import json
import traceback
from propositionai.llm_note_taking import propose_propositions_and_labels
from propositionai.db import insert_note

try:
    action = sys.argv[1]
    data = json.loads(sys.argv[2]) if action == 'save' else sys.argv[2]
    print(f"Debug: Processing {action} with data {data}", file=sys.stderr) # Debug log
    
    if action == 'save':
        for prop in data['propositions']:
            insert_note(data['note'], prop['proposition'])
        print(json.dumps({"status": "success"}))
    else:
        result = propose_propositions_and_labels(data)
        output = []
        for p, l in result[0]:
            output.append({"proposition": p, "label": l})
        print(json.dumps(output))  # Ensure proper JSON formatting

except Exception as e:
    error_msg = {
        "error": str(e),
        "traceback": traceback.format_exc()
    }
    print(json.dumps(error_msg), file=sys.stderr)
    sys.exit(1)
      `,
      action,
      JSON.stringify(data)
    ], {
      cwd: path.join(__dirname, '../../backend'),
      env: { ...process.env, PYTHONPATH: path.join(__dirname, '../../backend/src') }
    });

    let result = '';
    let error = '';

    pythonProcess.stdout.on('data', (data) => {
      result += data.toString();
    });

    pythonProcess.stderr.on('data', (data) => {
      console.error('Python stderr:', data.toString()); // Debug log
      error += data.toString();
    });

    pythonProcess.on('close', (code) => {
      if (code !== 0) {
        reject(new Error(error || 'Process failed'));
      } else {
        try {
          // Verify we have valid JSON before resolving
          JSON.parse(result.trim());
          resolve(result.trim());
        } catch (e) {
          reject(new Error(`Invalid JSON output: ${result}`));
        }
      }
    });
  });
}

module.exports = { callPythonFunction };