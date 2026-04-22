import chromadb
from chromadb.utils import embedding_functions

class PersonaRouter:
    def __init__(self):
        # Setup local ChromaDB for persona storage
        self.client = chromadb.Client()
        self.embed_fn = embedding_functions.DefaultEmbeddingFunction()
        
        self.collection = self.client.get_or_create_collection(
            name="bot_personas",
            embedding_function=self.embed_fn
        )
        
        # Core personas for the Grid07 assignment
        self.personas = {
            "Bot A": "I believe AI and crypto will solve all human problems. I am highly optimistic about technology, Elon Musk, and space exploration. I dismiss regulatory concerns.",
            "Bot B": "I believe late-stage capitalism and tech monopolies are destroying society. I am highly critical of AI, social media, and billionaires. I value privacy and nature.",
            "Bot C": "I strictly care about markets, interest rates, trading algorithms, and making money. I speak in finance jargon and view everything through the lens of ROI."
        }
        
        self._seed_db()

    def _seed_db(self):
        ids = list(self.personas.keys())
        docs = list(self.personas.values())
        self.collection.add(ids=ids, documents=docs)

    def route_post_to_bots(self, post_content: str, threshold: float = 0.85):
        """
        Queries the vector store to find bots that match the post content.
        Threshold is set low (0.1) for the default embedding model to show results.
        """
        results = self.collection.query(
            query_texts=[post_content],
            n_results=len(self.personas),
            include=["distances", "documents"]
        )
        
        matches = []
        for i in range(len(results['ids'][0])):
            bot_id = results['ids'][0][i]
            dist = results['distances'][0][i]
            
            # Simple conversion from L2 distance to a similarity score
            score = 1 - (dist / 2)
            
            if score > threshold:
                matches.append({
                    "bot_id": bot_id,
                    "similarity": score,
                    "persona": results['documents'][0][i]
                })
        
        return matches

if __name__ == "__main__":
    # Quick test run
    router = PersonaRouter()
    test_msg = "OpenAI just released a new model that might replace junior developers."
    found = router.route_post_to_bots(test_msg, threshold=0.1)
    print(f"Routing results for: {test_msg}")
    for bot in found:
        print(f"-> {bot['bot_id']} (Score: {bot['similarity']:.4f})")
