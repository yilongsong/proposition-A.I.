# src/propositionsai/main.py

from propositionsai.db import init_db, insert_note
from propositionsai.llm_processor import process_note
from propositionsai.llm_qa import chat_session

def take_notes():
    note = input("Enter your note: ")
    propositions = process_note(note)
    if propositions:
        print("Generated Propositions:")
        for i, proposition in enumerate(propositions, start=1):
            print(f"{i}: {proposition}")
            # Store each proposition separately.
            insert_note(note, proposition)
        print("Notes stored in the database.")
    else:
        print("No propositions were generated.")

def main():
    # Initialize the database (creates tables if needed)
    init_db()

    while True:
        print("\nMain Menu:")
        print("1. Take Notes")
        print("2. Query")
        print("3. Exit")
        choice = input("Enter your choice (1/2/3): ").strip()
        
        if choice == "1":
            print("Entering 'Take Notes' mode. Type 'menu' at any prompt to return to the main menu.")
            take_notes()
        elif choice == "2":
            print("Entering 'Query' mode. Type 'exit' within the conversation to return to the main menu.")
            chat_session()
        elif choice == "3":
            print("Exiting the program.")
            break
        else:
            print("Invalid option. Please try again.")

if __name__ == "__main__":
    main()