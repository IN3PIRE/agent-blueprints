"""Tests for Content Writer."""
import pytest
from agent import ContentWriterAgent

def test_writer():
    agent = ContentWriterAgent()
    assert agent is not None

if __name__ == "__main__":
    pytest.main([__file__])
