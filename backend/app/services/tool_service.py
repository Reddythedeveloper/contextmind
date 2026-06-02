SEARCH_DOCUMENTS_TOOL = {
    "type": "function",
    "function": {
        "name": "search_documents",
        "description": "Search user's uploaded documents for relevant information.",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "Search query"},
                "top_k": {"type": "integer", "default": 5}
            },
            "required": ["query"]
        }
    }
}

SUMMARIZE_TOOL = {
    "type": "function",
    "function": {
        "name": "summarize_topic",
        "description": "Generate a structured summary of a topic from retrieved documents.",
        "parameters": {
            "type": "object",
            "properties": {
                "topic": {"type": "string"},
                "format": {"type": "string", "enum": ["bullet", "paragraph", "table"]}
            },
            "required": ["topic"]
        }
    }
}

ALL_TOOLS = [SEARCH_DOCUMENTS_TOOL, SUMMARIZE_TOOL]
