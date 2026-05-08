"""Prompts for news curation."""

SUMMARIZATION_PROMPT = """Summarize the following news article concisely:

Article: {content}

Provide:
1. One-sentence summary (max 20 words)
2. Three key bullet points
3. Relevance score (1-10)
4. Potential bias flag (if any)"""

TOPIC_CLASSIFICATION_PROMPT = """Classify this news article into one of these topics: {topics}

Article: {content}

Return only the topic name."""

HEADLINE_GENERATION_PROMPT = """Generate an engaging but factual headline for this summary:

Summary: {summary}

Constraints:
- Max 12 words
- No clickbait
- Include key entity names"""
