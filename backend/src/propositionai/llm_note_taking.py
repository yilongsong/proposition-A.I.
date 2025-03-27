# src/propositionsai/llm_processor.py

'''
Function abstractions for processing incoming notes using LLM-Processor.
'''

import os
from openai import OpenAI
from dotenv import load_dotenv

from propositionai.config import *
from propositionai.prompts.loader import PromptLoader

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
prompt_loader = PromptLoader()

def propose_propositions_and_labels(note: str) -> tuple[list[tuple[str, str]], list[dict]]:
    """
    Converts a natural language note into a list of propositions paired with their corresponding labels.

    This function operates in two stages:
    
    1. **Proposition Generation:**  
       The LLM is asked to analyze the note sentence by sentence and extract each unit of idea that qualifies as a proposition.
       A proposition is defined as a concise, refined, and true statement. Valid proposition types include:
         - knowledge propositions
         - interpretations
         - examples
         - opinions  
       The LLM outputs one proposition per line.

    2. **Proposition Labeling:**  
       The previously generated propositions are then passed to the LLM, which assigns a label from the set 
       `["knowledge proposition", "interpretation", "example", "opinion"]` to each proposition.
       The output format for each line should be: "label: proposition".

    Parameters:
        note (str): A string containing the note text (e.g., from a lecture, book, or personal observation).

    Returns:
        list[tuple[str, str]]: A list of tuples, where each tuple consists of a proposition and its associated label.
        list[dict]: A list of messages used in the LLM conversation.
    """
    messages = []
    
    # Load and format prompts
    prompt_generate = prompt_loader.get_prompt('note_taking/proposition_generation', note=note)
    prompt_label = prompt_loader.get_prompt('note_taking/proposition_labeling')

    # --- Stage 1: Generate Propositions ---
    messages.append({"role": "user", "content": prompt_generate})
    
    response_generate = client.chat.completions.create(
        model=LLM_PROCESSOR_MODEL,
        messages=messages,
        temperature=LLM_PROCESSOR_TEMPERATURE  # leaning towards deterministic output
    )
    
    raw_propositions = response_generate.choices[0].message.content.strip()
    
    messages.append({"role": "assistant", "content": raw_propositions})
    
    # --- Stage 2: Label the Propositions (with full context) ---
    messages.append({"role": "user", "content": prompt_label})
    
    response_label = client.chat.completions.create(
        model=LLM_PROCESSOR_MODEL,
        messages=messages,
        temperature=LLM_PROCESSOR_TEMPERATURE  # leaning towards deterministic output
    )
    
    messages.append({"role": "assistant", "content": response_label.choices[0].message.content.strip()})
    
    raw_labeled = response_label.choices[0].message.content.strip()
    proposition_lines = [line.strip() for line in raw_labeled.split("\n") if line.strip()]
    
    labeled_propositions = []
    for line in proposition_lines:
        if ':' in line:
            label, proposition = line.split(":", 1)
            labeled_propositions.append((proposition.strip(), label.strip()))
        else:
            # Fallback in case a label isn't provided.
            labeled_propositions.append((line, "unknown"))
    
    return labeled_propositions, messages

# def expand_and_find_background(propositions: list[tuple]) -> list[tuple]:
#     """
#     Uses model to expand on propositions and find background information.
#     Returns a list of tuples (proposition, background_info).
#     """
#     results = []
#     for proposition in propositions:
#         prompt = (
#             f"Expand on the following proposition and provide background "
#             f"information if available. "
#             f"\n\n\"{proposition}\"\n\n"
#         )
#         response = client.chat.completions.create(
#             model=LLM_PROCESSOR_MODEL,
#             messages=[{"role": "user", "content": prompt}],
#             temperature=LLM_PROCESSOR_TEMPERATURE
#         )
#         background_info = response.choices[0].message.content.strip()
#         results.append((proposition, background_info))
#     return results
