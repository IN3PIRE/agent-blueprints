# News Curator Agent 🚧

**Framework:** AutoGen  
**Status:** 🚧 In Progress

Daily news aggregation and summarization agent powered by AutoGen.

## Features

- 📰 **Multi-Source Aggregation**: Pull from RSS feeds and APIs
- 🏷️ **Topic Classification**: Auto-categorize by topic
- 📝 **AI Summarization**: Concise, informative summaries
- 📊 **Priority Ranking**: Surface most important stories
- ⚖️ **Bias Detection**: Flag potential bias in sources

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```python
from news_curator import NewsCuratorAgent

# Initialize agent
curator = NewsCuratorAgent(
    model="gpt-4",
    topics=["technology", "business", "science"],
    sources=["reuters", "bloomberg", "techcrunch"]
)

# Get daily briefing
briefing = curator.curate_daily_briefing()
print(briefing)

# Get topic-specific briefing
tech_news = curator.get_topic_briefing("technology", limit=5)
print(tech_news)
```

## Features (In Progress)

- [x] Multi-agent system with AutoGen
- [x] News fetching and ranking
- [ ] RSS feed integration (TODO)
- [ ] API integrations (NewsAPI, GDELT)
- [ ] Bias detection algorithm
- [ ] Personalization based on user preferences

## Configuration

```python
curator = NewsCuratorAgent(
    model="gpt-4",
    sources=["reuters", "bloomberg", "nytimes"],
    topics=["AI", "climate", "finance"]
)
```

## Output Format

```json
{
  "date": "2024-01-15",
  "topics": ["technology", "business"],
  "news": {
    "technology": [
      {
        "title": "AI Breakthrough",
        "source": "reuters",
        "summary": "....",
        "key_points": [...],
        "relevance_score": 0.95
      }
    ]
  }
}
```

## TODO

- [ ] Add RSS feed parser
- [ ] Integrate NewsAPI
- [ ] Implement ML-based ranking
- [ ] Add user preference learning
- [ ] Create web dashboard

## License

MIT
