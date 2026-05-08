"""Tests for Customer Support Agent."""
import pytest
from agent import CustomerSupportAgent

def test_support_agent():
    agent = CustomerSupportAgent()
    assert agent is not None

if __name__ == "__main__":
    pytest.main([__file__])
