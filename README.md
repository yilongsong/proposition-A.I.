<h1 align="center">📝Proposition A.I.📝<br>Propositional Note-Taking Powered by Agentic LLMs</h1>

**Definition.** (*Propositional Note-Taking*) Note-taking can be described as "propositional" when the notes are composed of concise, refined, true propositions.

**Proposition A.I.** Note-taking may be better when done propositionally. Propositional note-taking may be better with the help of agentic LLMs.

Proposition A.I stores thoughts, ideas, information---anything you deem note-worthy, reasoned or disorganized---as concise, refined, true propositions, organizes them, and retrieves them for your reference.

**Algorithm.**
```
// --------------------------------------------------
// PROCEDURE: take_notes(you, Agent_L.L.M.)
// Description: Processes you-generated notes into refined propositions.
// --------------------------------------------------
procedure take_notes(you, Agent_L.L.M.):
    // 1. You write down some notes
    note ← you.input("Enter note:")
    
    // 2. Agent_L.L.M. generates proposed propositions from the note
    proposed_propositions_ ← Agent_L.L.M..process(note)
    
    // 3. You review and selects preferred propositions
    user_insisted_propositions ← you.review(proposed_propositions)
    
    // 4. Agent_L.L.M. fact-checks the you’s propositions using external tools
    fact_checked_propositions_ ← Agent_L.L.M..process(youProps, use_tool=True)
    
    // 5. You refine propositions based on fact-check feedback
    user_insisted_propositions ← you.review(fact_checked_propositions)
    
    // 6. Agent_L.L.M. expands the refined propositions for clarity and detail
    expanded_propositions ← Agent_L.L.M..process(user_insisted_propositions, use_tool=True)
    
    // 7. You finalize the propositions after expansion
    user_insisted_propositions ← you.confirm(expanded_propositions)
    
    // 8. Insert the final propositions into the database
    database.insert(user_insisted_propositions)
```
```
// --------------------------------------------------
// PROCEDURE: read_notes(you, Agent_L.L.M.)
// Description: Retrieves and iteratively refines your queries based on stored propositions.
// --------------------------------------------------
procedure read_notes(you, Agent_L.L.M.):
    // 1. You make a query
    query ← you.input("Enter query (problem, investigation, research, ...):")
    
    // 2. Retrieve relevant propositions via semantic search
    retrieved_propositions ← semantic_search(database, query)
    
    // 3. Initialize conversation history
    conversation_history ← [query]
    
    // 4. Interrogation
    while query is not None and query ≠ "":
         response ← Agent_L.L.M..generate(query, context=retrievedProps)
         conversation_history.append(response)
         query ← you.followup(response)
```