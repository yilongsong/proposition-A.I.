const { spawn } = require('child_process');
const path = require('path');

function callPythonFunction(note) {
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

try:
    result = propose_propositions_and_labels(sys.argv[1])
    output = []
    for p, l in result[0]:
        output.append({"proposition": p, "label": l})
    print(json.dumps(output))
except Exception as e:
    error_msg = {
        "error": str(e),
        "traceback": traceback.format_exc()
    }
    print(json.dumps(error_msg))
    sys.exit(1)
      `,
      note
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
      error += data.toString();
    });

    pythonProcess.on('close', (code) => {
      if (code !== 0) {
        reject(new Error(error || result));
      } else {
        resolve(result.trim());
      }
    });
  });
}

module.exports = { callPythonFunction };