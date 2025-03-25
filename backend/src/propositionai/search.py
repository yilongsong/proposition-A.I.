# src/propositionsai/search.py
"""
Module for performing semantic search over stored propositions.
Computes embeddings for a given query and for each proposition in the database,
then ranks them using cosine similarity.
"""

import os
import sqlite3
import numpy as np
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

from propositionai.config import *


# Define the embedding model (you can adjust as needed)

def get_embedding(text: str, model: str = EMBEDDING_MODEL) -> np.ndarray:
    """
    Get the embedding for a given text using OpenAI's API.
    
    Args:
        text: The text to embed.
        model: The embedding model to use.
        
    Returns:
        A numpy array representing the embedding.
    """
    response = client.embeddings.create(input=text, model=model)
    embedding = response.data[0].embedding
    return np.array(embedding)

def cosine_similarity(vec1: np.ndarray, vec2: np.ndarray) -> float:
    """
    Compute the cosine similarity between two vectors.
    
    Args:
        vec1: First vector.
        vec2: Second vector.
    
    Returns:
        The cosine similarity (a float between -1 and 1).
    """
    norm1 = np.linalg.norm(vec1)
    norm2 = np.linalg.norm(vec2)
    if norm1 == 0 or norm2 == 0:
        return 0.0
    return np.dot(vec1, vec2) / (norm1 * norm2)

def semantic_search(query: str, top_k: int = 3) -> str:
    """
    Perform semantic search over the propositions stored in the database.
    
    The function:
      1. Computes an embedding for the query.
      2. Retrieves all notes from the database.
      3. Computes the cosine similarity between the query embedding and each note's embedding.
      4. Selects the top_k most similar propositions.
      5. Returns a concatenated string of the selected propositions (e.g., for prompt context).
    
    Args:
        query: The user's query string.
        top_k: The number of top results to return.
    
    Returns:
        A string containing the selected logical propositions.
    """
    # Compute the embedding for the query
    query_embedding = get_embedding(query)

    # Connect to the SQLite database (adjust the path if necessary)
    conn = sqlite3.connect("notes.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, original, logic FROM notes")
    rows = cursor.fetchall()
    conn.close()

    # Compute similarity scores for each stored note
    results = []
    for row in rows:
        note_id, original, logic = row
        # Compute embedding for the 'logic' field of the note
        note_embedding = get_embedding(logic)
        sim = cosine_similarity(query_embedding, note_embedding)
        results.append((sim, note_id, original, logic))

    # Sort results by similarity in descending order
    results.sort(key=lambda x: x[0], reverse=True)
    top_results = results[:top_k]

    # Build a context string with the top results
    context_lines = []
    for sim, note_id, original, logic in top_results:
        context_lines.append(f"Note ID {note_id}: {logic}")
    context = "\n".join(context_lines)
    return context
