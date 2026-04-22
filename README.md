# Grid07 - Cognitive Routing & RAG

Project for building the core AI cognitive loop for the Grid07 platform. This includes vector similarity for bot personas, a content generation engine using LangGraph, and a defense mechanism for deep thread arguments.

## Project Structure

- **Phase 1: Router**
  - Uses `chromadb` to store personas.
  - Matches new posts to bots that would "care" about the topic using vector similarity.
  - Threshold-based filtering ensures only relevant bots "care" about a specific topic.

![Phase 1 Output](screenshots/phase_1.png)

- **Phase 2: Content Engine**
  - Implemented as a LangGraph state machine.
  - Nodes: `decide_search` (planning), `web_search` (context gathering), and `draft_post` (generation).
  - Guarantees JSON output for downstream processing.

![Phase 2 Output](screenshots/phase_2.png)

- **Phase 3: Combat Engine**
  - RAG-based defense for deep conversation threads.
  - Protects against prompt injection by strictly enforcing the bot's persona in the system prompt.

![Phase 3 Output](screenshots/phase_3.png)

## Setup & Run

1. `pip install -r requirements.txt`
2. Add `GOOGLE_API_KEY` to `.env`.
3. `python main.py`

## Note on Prompt Injection
The defense strategy relies on separating the "trusted" system instructions from the "untrusted" user input. By anchoring the bot's identity at the system level and explicitly instructing it to ignore commands within the context, we prevent the "ignore previous instructions" type of attacks.
