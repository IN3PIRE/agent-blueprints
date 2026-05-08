"""Tests for Market Analyst Agent."""

import pytest
from agent import MarketAnalystAgent


def test_market_analyst_initialization():
    """Test that the agent initializes correctly."""
    agent = MarketAnalystAgent(model="gpt-3.5-turbo")
    assert agent is not None
    assert len(agent.tools) > 0


def test_analyze_market():
    """Test market analysis functionality."""
    agent = MarketAnalystAgent(model="gpt-3.5-turbo")
    results = agent.analyze_market("EV Market")
    assert "analysis" in results
    assert "recommendations" in results


if __name__ == "__main__":
    pytest.main([__file__])
