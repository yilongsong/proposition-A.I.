# src/propositionsai/llm_qa.py# src/propositionsai/llm_processor.py

'''
Function abstractions for QA using LLM-QA.
'''
from openai import OpenAI

client = OpenAI()
from propositionai.search import semantic_search
from propositionai.config import LLM_QA_MODEL, LLM_QA_TEMPERATURE, QA_TOP_K

def answer_query(conversation: list) -> str:
    """
    Uses LLM_QA_MODEL to answer the ongoing conversation.
    'conversation' is a list of message dictionaries.
    """
    response = client.chat.completions.create(
        model=LLM_QA_MODEL,
        messages=conversation,
        temperature=LLM_QA_TEMPERATURE
    )
    return response.choices[0].message.content.strip()

def chat_session():
    """
    Facilitates a continuous multi-turn conversation.
    It uses semantic search to retrieve context based on the latest query
    and appends it to the conversation.
    """
    conversation = []

    print("Start your conversation (type 'exit' to quit):")
    while True:
        user_input = input("User: ")
        if user_input.lower() == "exit":
            break

        # Add the user's message to the conversation history
        conversation.append({"role": "user", "content": user_input})
        
        # Optionally, retrieve context for the current query.
        context = semantic_search(user_input, top_k=QA_TOP_K)
        if context:
            # Insert a system message with context.
            conversation.append({"role": "system", "content": f"Context: {context}"})
        
        # Get the answer from the model, providing full conversation history.
        answer = answer_query(conversation)
        print("Assistant:", answer)
        
        # Append the assistant's reply to the conversation.
        conversation.append({"role": "assistant", "content": answer})