"""Tests for Social Media Agent."""
import pytest
from agent import SocialMediaAgent

def test_social_agent():
    agent = SocialMediaAgent()
    assert agent is not None

if __name__ == "__main__":
    pytest.main([__file__])
