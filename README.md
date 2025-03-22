<h1 align="center">📝Proposition A.I.📝<br>Propositional Note-Taking Powered by Agentic LLMs</h1>

**Definition.** (*Propositional Note-Taking*) Note-taking can be described as "propositional" when the notes are composed of *concise, refined, true* propositions.

**Proposition A.I.** Note-taking may be better when done propositionally; propositional note-taking may be better done with the help of agentic LLMs.

Proposition A.I stores thoughts, ideas, information---anything you deem note-worthy---as concise, refined, true propositions, organizes them, and retrieves them for your reference.

We divide what we call propositions into four categories:
1. Knowledge propositions:
    *A half space classifier is typically defined by a decision boundary of the form: $f(x)=\text{sign}(w^Tx+b) \in \{-1, +1\}.$*

2. Interpretations:
    *A half space can be understood as one side of a hyperplane, which splits a space into two "halves".*

3. Examples:
    *An example of a simple half space: consider the $\mathbb{R}^2$ coordinate space. A vertical line at $x=3$ devides the plane into two half spaces, where the left half space contains all points with $x < 3$ (e.g., (2,4)) and the right half space all points with $x > 3$ (e.g., (4,0)). The line $x = 3$ acts as the decision boundary.*

4. Opinions:
    *Professor: standalone half space classifiers are rarely used, but the concept of half spaces is foundational to many widely used algorithms (e.g. SVMs, perceptrons, linear programming, etc.).*

Note-taking in Proposition A.I consists of note-jotting and note-refining. User need not worry about wording, arranging, or typesetting at "note-jotting" time---although they should be conscious of the four categories, which is more useful than worrying about non-essential wording or typesetting. Note refining can be done immediately after note-jotting or at another time.

**Algorithm.** (*Take Notes*) We design a human-in-the-loop (HITL) pipeline for note-taking. This process obtains and refines the propositions stored both in the database and in your brain---or you can just select "accept" or "persist" to take the LLM's suggestions unaltered or ignore.
```
// --------------------------------------------------
// PROCEDURE: take_notes(you, Agent_L.L.M.-1)
// Description: Processes your notes into refined propositions and store.
// --------------------------------------------------
procedure take_notes(you, Agent_L.L.M.-1):
    // 1. You write down some notes (note-taking time)
    note ← you.input("Enter note:")
    
    // 2. Agent_L.L.M.-1 generates proposed propositions from the note
    proposed_propositions_ ← Agent_L.L.M.-1.propose_propositions(note)
    
    // 3. You review, select, or edit propositions
    user_insisted_propositions ← you.review(proposed_propositions)
    
    // 4. Agent_L.L.M.-1 fact-checks the propositions using external tools
    fact_checked_propositions_ ← Agent_L.L.M.-1.fact_check(user_insisted_propositions, use_tool=True)
    
    // 5. You refine propositions based on fact-check feedback
    user_insisted_propositions ← you.review(fact_checked_propositions)
    
    // 6. Agent_L.L.M.-1 expands the refined propositions to include other relevant and true statements
    expanded_propositions ← Agent_L.L.M.-1.expand(user_insisted_propositions, use_tool=True)
    
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