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

    # --- Stage 1: Generate Propositions ---
    prompt_generate = (
        "You are an expert in logical natural language processing.\n\n"
        "Let's define some terminologies first. These terminologies are crucial for the task you will need to perform.\n\n"
        "Here's the definition of a \"proposition\" in this context: a unit of idea--written concisely and expressively--"
        "that belongs to one of four categories: knowledge proposition, interpretation, example, and opinion.\n\n"
        "Here are three examples of knowledge:\n \"The Earth revolves around the Sun.\"\n"
        "\"Water freezes at 0 degrees Celsius.\"\n\"A half space classifier is typically defined by a decision "
        "boundary of the form: $f(x)=\text{sign}(w^Tx+b) \in \{-1, +1\}.$\"\n"
        "Knowledge are direct assertions without an identified human source.\n\n"
        
        "Here are three examples of \"interpretations\":\n \"A half space can be understood as one side of a hyperplane, "
        "which splits a space into two \"halves\".\"\n"
        "\"LLMs can be thought of as a parrot trained to mimic human languages.\"\n"
        "\"Gravity can be interpreted as the curvature of space-time caused by mass, much like a heavy ball deforms a stretched rubber sheet.\"\"\n"
        "\"Interpretations\" here does not refer to subjective remarks about something, but rather a description, analogy, or altered perspective "
        "that makes a concept easier to understand. Its difference from a knowledge proposition is that "
        "it contains phrases like \"can be thought of as\" or \"can be interpreted as\" while knowledge propositions are "
        "direct assertions.\n\n"
        
        "Here are two examples of examples:"
        "\"Example: The task 'last letter concatenation' is"
        "extremely simple for humans, but ML model requires a lot of data to train to get 85 percent, 90 percent accuracy.\"\n"
        "Example: Evaluate the integral $$\int_0^1 x^2\, dx.$$"
        "Solution:"
        "We start by applying the power rule for integration:"
        "$$\int x^n\, dx = \frac{x^{n+1}}{n+1} + C.$$"
        "Thus,"
        "  $$\int x^2\, dx = \frac{x^3}{3} + C.$$"
        "Evaluating the definite integral from 0 to 1 gives:"
        "$$\left[\frac{x^3}{3}\right]_{0}^{1} = \frac{1^3}{3} - \frac{0^3}{3} = \frac{1}{3}.$$\"\n"
        "Examples are specific concrete instances that illustrate a concept, such as how to do an integral, or performance gap between "
        "humans and ML models on certain tasks.\n\n"
        
        "Here are three examples of \"opinions\":\n \"Bob: I believe that the Earth is flat.\"\n"
        "\"Professor: standalone half space classifiers are rarely used, but the concept of half spaces is foundational "
        "to many widely used algorithms (e.g. SVMs, perceptrons, linear programming, etc.).\"\n"
        "\"Denny Zhou expectation's for AI: AI should be able to learn from just a few examples, like what humans usually do.\"\n"
        "Note that the key element of opinioin in this context is not subjectivity, but rather whether or not a source is identified"
        " for a statement. Sometimes a source is not explicitly identified, but can be inferred clearly from the context, then the"
        "proposition is also an opinion\n\n"
        
        "We do not count questions as propositions; a question should be merged with its answer to form a proposition, and such "
        "a proposition belongs to the answer's category.\n\n"
        
        "Something that is not a proposition but we still should be aware of is a \"source\". Usually it is the name of a book, academic paper, or project.\n\n"
        
        "Analyze the following text sentence by sentence and identify each unit of idea that qualifies as a \"proposition\".\n"
        f"Text: \"{note}\"\n\n"
        "Reason step by step for each unit of idea on what it is stating, and which of the four categories of proposition it belongs to.\n"
       # "For each proposition, summarize it such that it is concise and refined. Output each proposition on a new line."
    )
    
    messages.append({"role": "user", "content": prompt_generate})
    
    response_generate = client.chat.completions.create(
        model=LLM_PROCESSOR_MODEL,
        messages=messages,
        temperature=LLM_PROCESSOR_TEMPERATURE  # leaning towards deterministic output
    )
    
    raw_propositions = response_generate.choices[0].message.content.strip()
    
    messages.append({"role": "assistant", "content": raw_propositions})
    
    # --- Stage 2: Label the Propositions (with full context) ---
    prompt_label = (
        "Now, based on your reasoning above, summarize the units of idea into propositions (not necessarily one-to-one)\n "
        "such that it is grammatically correct, concise and refined, "
        "and label each proposition with its category "
        "(knowledge, interpretation, example, opinion, source).\n\n"
        "For each proposition, output the result on a new line in the format 'label: proposition'."
    )
    
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

def expand_and_find_background(propositions: list[tuple]) -> list[tuple]:
    """
    Uses model to expand on propositions and find background information.
    Returns a list of tuples (proposition, background_info).
    """
    results = []
    for proposition in propositions:
        prompt = (
            f"Expand on the following proposition and provide background "
            f"information if available. "
            f"\n\n\"{proposition}\"\n\n"
        )
        response = client.chat.completions.create(
            model=LLM_PROCESSOR_MODEL,
            messages=[{"role": "user", "content": prompt}],
            temperature=LLM_PROCESSOR_TEMPERATURE
        )
        background_info = response.choices[0].message.content.strip()
        results.append((proposition, background_info))
    return results
