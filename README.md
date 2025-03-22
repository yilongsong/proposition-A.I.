<h1 align="center">📝Proposition A.I.📝<br>Propositional Note-Taking Powered by Agentic LLMs</h1>

**Definition.** (*Propositional Note-Taking*) Note-taking can be described as "propositional" when the notes are composed of concise, refined, true propositions.

**Proposition A.I.** Note-taking may be better when done propositionally. Propositional note-taking may be better done with the help of agentic LLMs.

Proposition A.I stores thoughts, ideas, information---anything you deem note-worthy, already well-arranged or disorganized---as concise, refined, true propositions, organizes them, and retrieves them for your reference.

**Algorithm.** (*Take Notes*) We design a human-in-the-loop (HITL) pipeline for note taking. This process refines the propositions stored both in the database and in your brain---or you can just spam click "accept" and take the LLM's suggestion unaltered.
```
// --------------------------------------------------
// PROCEDURE: take_notes(you, Agent_L.L.M.-1)
// Description: Processes your notes into refined propositions and store.
// --------------------------------------------------
procedure take_notes(you, Agent_L.L.M.-1):
    // 1. You write down some notes
    note ← you.input("Enter note:")
    
    // 2. Agent_L.L.M.-1 generates proposed propositions from the note
    proposed_propositions_ ← Agent_L.L.M.-1.process(note)
    
    // 3. You review and selects preferred propositions
    user_insisted_propositions ← you.review(proposed_propositions)
    
    // 4. Agent_L.L.M.-1 fact-checks the you’s propositions using external tools
    fact_checked_propositions_ ← Agent_L.L.M.-1.process(youProps, use_tool=True)
    
    // 5. You refine propositions based on fact-check feedback
    user_insisted_propositions ← you.review(fact_checked_propositions)
    
    // 6. Agent_L.L.M.-1 expands the refined propositions to include more meaningful and true ideas
    expanded_propositions ← Agent_L.L.M.-1.process(user_insisted_propositions, use_tool=True)
    
    // 7. You finalize the propositions after expansion
    user_insisted_propositions ← you.confirm(expanded_propositions)
    
    // 8. Save final propositions to the database
    database.insert(user_insisted_propositions)
```
**Algorithm.** (*Read Notes (Assisted)*) You interrogate Agent_L.L.M.-2 to tell you what you want to know based on your notes.
```
// --------------------------------------------------
// PROCEDURE: read_notes(you, Agent_L.L.M.-2)
// Description: 
// --------------------------------------------------
procedure read_notes(you, Agent_L.L.M.-2):
    // 1. You make a query
    query ← you.input("Enter query:")
    
    // 2. Retrieve relevant propositions
    retrieved_propositions ← semantic_search(database, query)
    
    // 3. Initialize conversation history
    conversation_history ← [query]
    
    // 4. Interrogation
    while query is not None and query ≠ "":
         response ← Agent_L.L.M.-2.generate(query, context=retrieved_propositions)
         conversation_history.append(response)
         query ← you.followup(response)
```

Of-course, you may read notes unassisted. Propositions are organized into graphs and lists by topics or narratives. Or you can view them by date of creation.