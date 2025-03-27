1. **`package.json`**

- **In Your App**: Defines your project's dependencies (Electron and python-shell) and scripts to run the app
- **General Purpose**: The manifest file for Node.js applications, managing dependencies, scripts, and project metadata

2. **`src/main.js`**
```javascript
<vscode_codeblock_uri>file:///Users/yilongsong/Desktop/propositions.ai/frontend/src/main.js</vscode_codeblock_uri>
```
- **In Your App**: Creates the main application window with specific security settings (contextIsolation, nodeIntegration) and loads your UI
- **General Purpose**: The main process in Electron apps, manages application lifecycle and creates browser windows

3. **`src/preload.js`**
```javascript
<vscode_codeblock_uri>file:///Users/yilongsong/Desktop/propositions.ai/frontend/src/preload.js</vscode_codeblock_uri>
```
- **In Your App**: Safely exposes the [processNote](http://_vscodecontentref_/0) function to the renderer process through contextBridge
- **General Purpose**: Provides a secure way to expose Node.js functionality to the renderer process

4. **`src/bridge.js`**
```javascript
<vscode_codeblock_uri>file:///Users/yilongsong/Desktop/propositions.ai/frontend/src/bridge.js</vscode_codeblock_uri>
```
- **In Your App**: Creates the Python-JavaScript bridge, spawning Python processes to run your LLM note processing
- **General Purpose**: Handles inter-process communication between JavaScript and other languages/processes

5. **`src/renderer/index.html`**
```html
<vscode_codeblock_uri>file:///Users/yilongsong/Desktop/propositions.ai/frontend/src/renderer/index.html</vscode_codeblock_uri>
```
- **In Your App**: Defines your two-panel UI with note-taking and note-query sections
- **General Purpose**: The main UI template for the application

6. **`src/renderer/renderer.js`**
```javascript
<vscode_codeblock_uri>file:///Users/yilongsong/Desktop/propositions.ai/frontend/src/renderer/renderer.js</vscode_codeblock_uri>
```
- **In Your App**: Handles UI interactions, processes notes through the bridge, and updates the display
- **General Purpose**: Contains frontend logic and event handlers

7. **`src/renderer/styles.css`**
```css
<vscode_codeblock_uri>file:///Users/yilongsong/Desktop/propositions.ai/frontend/src/renderer/styles.css</vscode_codeblock_uri>
```
- **In Your App**: Implements a VS Code-like dark theme and layouts for your two-panel interface
- **General Purpose**: Defines the visual styling of the application

The data flow in your application works like this:

1. User enters text in the UI (`index.html`)
2. UI events are handled by [renderer.js](http://_vscodecontentref_/1)
3. [renderer.js](http://_vscodecontentref_/2) calls [window.api.processNote](http://_vscodecontentref_/3)
4. [preload.js](http://_vscodecontentref_/4) receives this call through the contextBridge
5. [bridge.js](http://_vscodecontentref_/5) spawns a Python process to handle the note processing
6. Results flow back through the same chain in reverse
7. [renderer.js](http://_vscodecontentref_/6) updates the UI with the results

This architecture provides:
- Security (through contextIsolation)
- Clean separation of concerns
- Bridge between Node.js/Electron and Python
- Responsive UI with proper event handling