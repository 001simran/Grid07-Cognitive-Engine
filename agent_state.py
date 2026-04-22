from typing import TypedDict, List, Dict, Optional

class ContentState(TypedDict):
    bot_id: str
    persona: str
    topic: Optional[str]
    search_query: Optional[str]
    search_results: Optional[str]
    post_content: Optional[str]
    json_output: Optional[Dict]
