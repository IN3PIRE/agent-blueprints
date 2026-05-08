"""Tests for News Curator Agent."""

import pytest
from agent import NewsCuratorAgent


def test_news_curator_initialization():
    """Test that the agent initializes correctly."""
    agent = NewsCuratorAgent(model="gpt-3.5-turbo")
    assert agent is not None
    assert len(agent.sources) > 0


def test_curate_daily_briefing():
    """Test daily briefing curation."""
    agent = NewsCuratorAgent(model="gpt-3.5-turbo")
    briefing = agent.curate_daily_briefing()
    assert "date" in briefing
    assert "news" in briefing


if __name__ == "__main__":
    pytest.main([__file__])
