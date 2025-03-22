# src/propositionsai/llm_processor.py

'''
Function abstractions for processing incoming notes using LLM-Processor.
'''

import os
from openai import OpenAI
from dotenv import load_dotenv

from propositionai.config import *

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def propose_propositions(note: str) -> str:
    """
    Uses LLM_PROCESSOR_MODEL to convert a natural language note into a 
    list of propositions. Returns the propositions as a list.
    
    """
    prompt = (
        f"Processing the following text into one or more well formed, "
        f"non-overlapping, complete, and concise propositions that covers "
        f"all significant information:"
        f"\n\n\"{note}\"\n\n"        
        "Output only the processed propositions."
    )
    response = client.chat.completions.create(
        model=LLM_PROCESSOR_MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=LLM_PROCESSOR_TEMPERATURE)  # leaning towards deterministic output
    
    raw_propositions = response.choices[0].message.content.strip()
    propositions = [prop.strip() for prop in raw_propositions.split("\n") if prop.strip()]
    return propositions

def fact_check_propositions(propositions: list) -> list:
    """
    Uses GPT-3.5-turbo to fact-check a list of propositions.
    Returns a list of tuples (proposition, is_fact).
    """
    results = []
    for proposition in propositions:
        prompt = (
            f"Is the following statement a fact? Answer with 'yes' or 'no'. "
            f"\n\n\"{proposition}\"\n\n"
        )
        response = client.chat.completions.create(
            model=LLM_PROCESSOR_MODEL,
            messages=[{"role": "user", "content": prompt}],
            temperature=LLM_PROCESSOR_TEMPERATURE
        )
        is_fact = response.choices[0].message.content.strip().lower()
        results.append((proposition, is_fact))
    return results

