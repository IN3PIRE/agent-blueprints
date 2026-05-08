# Content Writer Agent ✅

**Framework:** CrewAI  
**Status:** ✅ Ready

Blog post and article generation.

## Features

- ✍️ **Article Writing**: Generate full articles
- 📝 **Multiple Tones**: Professional, casual, technical
- 🔍 **Research-Backed**: Well-researched content
- ✏️ **Auto-Editing**: Built-in editing
- 📊 **SEO Optimization**: Keyword-optimized content

## Usage

```python
from content_writer import ContentWriterAgent

agent = ContentWriterAgent(tone="professional")
article = agent.write_article("AI in Healthcare", word_count=1500)
print(article["content"])
```

## License

MIT
