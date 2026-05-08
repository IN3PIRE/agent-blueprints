"""Tests for Documentation Generator Agent."""

import pytest
from agent import DocGeneratorAgent


def test_doc_generator_initialization():
    """Test that the agent initializes correctly."""
    agent = DocGeneratorAgent()
    assert agent is not None


def test_generate_docstring():
    """Test docstring generation."""
    agent = DocGeneratorAgent()
    code = "def add(a, b): return a + b"
    docstring = agent.generate_docstring(code, "add")
    assert "docstring" in docstring.lower() or '"""' in docstring


if __name__ == "__main__":
    pytest.main([__file__])
