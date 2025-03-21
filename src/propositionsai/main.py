# src/propositionsai/main.py
from propositionsai import process_note
from propositionsai import init_db, insert_note, search_notes

def main():
    # Initialize the database (create tables if not exists)
    init_db()
    
    # Get user input
    note = input("Enter your proposition: ")
    
    # Process the note with the LLM
    logic = process_note(note)
    
    # Print the resulting logical formula
    print("\nProcessed Logical Statement:")
    print(logic)
    
    # Store the note and logical formula in the database
    insert_note(note, logic)
    print("\nNote stored in the database.")
    
    # (Optional) Demonstrate a simple search for testing retrieval
    query = input("\nEnter a search term to query logical statements: ")
    results = search_notes(query)
    print("\nSearch Results:")
    for row in results:
        print(f"ID: {row[0]}, Original: {row[1]}, Logic: {row[2]}")

if __name__ == "__main__":
    main()