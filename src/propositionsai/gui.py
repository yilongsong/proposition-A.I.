# src/propositionsai/gui.py

'''
Simple GUI for testing and debugging
'''

import sys
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QTextEdit, QLineEdit, QPushButton, QLabel, QSplitter
)
from PySide6.QtCore import Qt

from propositionsai.llm_processor import process_note
from propositionsai.llm_qa import answer_query
from propositionsai.db import insert_note
from propositionsai.search import semantic_search
from propositionsai.config import QA_TOP_K

class NoteChatBox(QWidget):
    """Chat box for note taking: processes notes into propositions and saves them."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout(self)
        self.title_label = QLabel("Take Notes")
        layout.addWidget(self.title_label)
        
        # Scrollable display for conversation/history
        self.chat_display = QTextEdit()
        self.chat_display.setReadOnly(True)
        layout.addWidget(self.chat_display)
        
        # Input area: QLineEdit for text entry and a send button (arrow)
        input_layout = QHBoxLayout()
        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("Enter your note here...")
        self.send_button = QPushButton("↑")
        self.send_button.setFixedWidth(40)
        input_layout.addWidget(self.input_field)
        input_layout.addWidget(self.send_button)
        layout.addLayout(input_layout)
        
        self.send_button.clicked.connect(self.send_message)
        self.input_field.returnPressed.connect(self.send_message)
    
    def send_message(self):
        note = self.input_field.text().strip()
        if not note:
            self.chat_display.append("Please enter a note.")
            return
        
        # Display user note
        self.chat_display.append(f"<b>User:</b> {note}")
        self.input_field.clear()
        
        # Process note into propositions using llm_processor
        propositions = process_note(note)
        if propositions:
            self.chat_display.append("<b>Assistant:</b>")
            # Display and store each proposition, numbered
            for idx, proposition in enumerate(propositions, start=1):
                line = f"Proposition {idx}: {proposition[3:]}"
                self.chat_display.append(line)
                insert_note(note, proposition)
        else:
            self.chat_display.append("<b>Assistant:</b> No propositions were generated.")


class QueryChatBox(QWidget):
    """Chat box for querying: maintains a conversation with the QA system."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.conversation = []  # Maintain multi-turn conversation history
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout(self)
        self.title_label = QLabel("Query Notes")
        layout.addWidget(self.title_label)
        
        self.chat_display = QTextEdit()
        self.chat_display.setReadOnly(True)
        layout.addWidget(self.chat_display)
        
        input_layout = QHBoxLayout()
        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("Query your notes...")
        self.send_button = QPushButton("↑")
        self.send_button.setFixedWidth(40)
        input_layout.addWidget(self.input_field)
        input_layout.addWidget(self.send_button)
        layout.addLayout(input_layout)
        
        self.send_button.clicked.connect(self.send_message)
        self.input_field.returnPressed.connect(self.send_message)
    
    def send_message(self):
        query = self.input_field.text().strip()
        if not query:
            self.chat_display.append("Please enter a query.")
            return
        
        self.chat_display.append(f"<b>User:</b> {query}")
        self.input_field.clear()
        
        # Append user's query to conversation history
        self.conversation.append({"role": "user", "content": query})
        
        # Retrieve context via semantic search and add as a system message
        context = semantic_search(query, top_k=QA_TOP_K)
        if context:
            self.conversation.append({"role": "system", "content": f"Context: {context}"})
        
        # Get the assistant's response using the conversation history
        answer = answer_query(self.conversation)
        self.chat_display.append(f"<b>Assistant:</b> {answer}")
        self.conversation.append({"role": "assistant", "content": answer})


class MainWindow(QWidget):
    """Main window with two side-by-side chat boxes for note taking and querying."""
    def __init__(self):
        super().__init__()
        self.setWindowTitle("propositions.ai")
        self.resize(1280, 720)
        self.init_ui()
    
    def init_ui(self):
        splitter = QSplitter(Qt.Horizontal)
        self.note_box = NoteChatBox()
        self.query_box = QueryChatBox()
        splitter.addWidget(self.note_box)
        splitter.addWidget(self.query_box)
        splitter.setSizes([640, 640])
        
        main_layout = QHBoxLayout(self)
        main_layout.addWidget(splitter)
        self.setLayout(main_layout)

def run_gui():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    run_gui()
