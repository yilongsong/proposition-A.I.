# src/propositionsai/llm_processor.py

'''
Function abstractions for processing incoming notes using LLM-Processor.
'''

import os
from openai import OpenAI
from dotenv import load_dotenv

from propositionsai.config import *

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def process_note(note: str) -> str:
    """
    Uses GPT-3.5-turbo to convert a natural language note into a 
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