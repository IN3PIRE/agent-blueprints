# Market Analyst Agent

**Framework:** LangChain  
**Status:** ✅ Ready

Market research and competitive analysis agent powered by LangChain.

## Features

- 🎯 **Market Research**: Comprehensive industry analysis
- 🏢 **Competitor Analysis**: Identify and analyze key competitors
- 📊 **Market Sizing**: Estimate TAM, SAM, and SOM
- 📈 **Trend Analysis**: Identify market trends and drivers
- 💡 **Strategic Insights**: Actionable recommendations

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```python
from market_analyst import MarketAnalystAgent

# Initialize agent
analyst = MarketAnalystAgent(model="gpt-4")

# Analyze a market
results = analyst.analyze_market(
    industry="Electric Vehicles",
    focus_areas=["competitors", "market_size", "trends"]
)

print(results)
```

## Example Output

```json
{
  "industry": "Electric Vehicles",
  "analysis": {
    "competitors": "Tesla leads with 30% market share...",
    "market_size": "Global EV market valued at $388B...",
    "trends": "Increasing battery efficiency, government incentives..."
  },
  "recommendations": [
    "Focus on battery technology partnerships",
    "Target emerging markets in Asia",
    "Develop charging infrastructure strategy"
  ]
}
```

## Configuration

```python
analyst = MarketAnalystAgent(
    model="gpt-4",
    api_key="your-api-key"
)
```

## Tools

- **search_companies**: Find companies by industry/keyword
- **analyze_competitors**: Competitive landscape analysis
- **market_size_estimation**: TAM/SAM/SOM calculations
- **trend_analysis**: Market trend identification

## Examples

See `examples/` directory for complete usage examples.

## License

MIT
