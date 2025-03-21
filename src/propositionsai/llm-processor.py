# src/propositionsai/llm-processor.py
import os
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")

def process_note(note: str) -> str:
    """
    Uses GPT-3.5-turbo to convert a natural language note into a 
    propositional logic formula. Returns the logical formula as a string.
    """
    prompt = (
        f"Translate the following statement into a well-formed formula "
        f"in propositional logic:\n\n\"{note}\"\n\n"
        "Output only the logical formula."
    )
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0  # for deterministic output
    )
    logical_formula = response["choices"][0]["message"]["content"].strip()
    return logical_formula