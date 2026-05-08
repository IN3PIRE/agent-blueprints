"""Tests for Debug Assistant Agent."""

import pytest
from agent import DebugAssistantAgent


def test_debug_assistant_initialization():
    """Test that the agent initializes correctly."""
    agent = DebugAssistantAgent(language="python")
    assert agent is not None
    assert len(agent.tools) > 0


def test_debug_code():
    """Test code debugging functionality."""
    agent = DebugAssistantAgent(language="python")
    code = "def foo(): return 1 / 0"
    results = agent.debug_code(code)
    assert "issues" in results or "language" in results


if __name__ == "__main__":
    pytest.main([__file__])
