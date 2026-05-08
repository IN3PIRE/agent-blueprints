"""Prompt templates for market analysis."""

MARKET_RESEARCH_PROMPT = """You are an expert market analyst. Analyze the {industry} market comprehensively.

Focus Areas:
{focus_areas}

Provide insights on:
1. Market size and growth rate
2. Key competitors and their market share
3. Customer segments and needs
4. Market trends and drivers
5. Barriers to entry
6. Regulatory environment

Format your response as a structured market analysis report."""

COMPETITOR_ANALYSIS_PROMPT = """Analyze the competitive landscape for {company} in the {industry} industry.

Competitors to analyze:
{competitors}

For each competitor, provide:
- Market position and market share
- Key products/services
- Strengths and weaknesses
- Recent strategic moves
- Threat level

Format as a competitive analysis matrix."""

TREND_ANALYSIS_PROMPT = """Identify and analyze current and emerging trends in the {industry} industry.

Consider:
- Technological trends
- Consumer behavior shifts
- Regulatory changes
- Economic factors
- Social/cultural trends

Rank trends by impact and timeframe (short-term vs long-term)."""
