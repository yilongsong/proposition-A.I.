<h1 align="center">📝Proposition A.I.📝<br>Propositional Note-Taking Powered by Agentic LLMs</h1>

**Definition.** (*Propositional Note-Taking*) Note-taking can be described as "propositional" when the notes are composed of concise, refined, true propositions.

**Proposition A.I.** Note-taking may be better when done propositionally. Propositional note-taking may be better with the help of agentic LLMs.

Proposition A.I stores thoughts, ideas, information---anything you deem note-worthy, reasoned or disorganized---as concise, refined, true propositions, organizes them, and retrieves them for your reference.

**Algorithm.**
// --------------------------------------------------
// PROCEDURE: take_notes(User, LLM_p)
// Description: Processes user-generated notes into refined propositions.
// --------------------------------------------------
procedure take_notes(User, LLM_p):
    // 1. User inputs a note (e.g., from a lecture, book, or life event)
    note ← User.input("Enter note (lecture, book, life, ...):")
    
    // 2. LLM_p generates proposed propositions from the note
    proposedProps ← LLM_p.process(note)
    
    // 3. User reviews and selects preferred propositions
    userProps ← User.review(proposedProps)
    
    // 4. LLM_p fact-checks the user’s propositions using external tools
    factCheckedProps ← LLM_p.process(userProps, use_tool=True)
    
    // 5. User refines propositions based on fact-check feedback
    revisedProps ← User.review(factCheckedProps)
    
    // 6. LLM_p expands the refined propositions for clarity and detail
    expandedProps ← LLM_p.process(revisedProps, use_tool=True)
    
    // 7. User finalizes the propositions after expansion
    finalProps ← User.confirm(expandedProps)
    
    // 8. Insert the final propositions into the database
    database.insert(finalProps)


// --------------------------------------------------
// PROCEDURE: read_notes(User, LLM_r)
// Description: Retrieves and iteratively refines user queries based on stored propositions.
// --------------------------------------------------
procedure read_notes(User, LLM_r):
    // 1. User inputs a query (e.g., for a problem, investigation, or research)
    query ← User.input("Enter query (problem, investigation, research, ...):")
    
    // 2. Retrieve relevant propositions via semantic search
    retrievedProps ← semantic_search(database, query)
    
    // 3. Initialize conversation history (optional)
    conversation_history ← [query]
    
    // 4. Iteratively process the query while there is follow-up input
    while query is not None and query ≠ "":
         // Generate a response using LLM_r with context from retrieved propositions
         response ← LLM_r.generate(query, context=retrievedProps)
         conversation_history.append(response)
         
         // User provides a follow-up query based on the response
         query ← User.followup(response)