"""Tests for Finance Tracker."""
import pytest
from agent import FinanceTrackerAgent

def test_finance_agent():
    agent = FinanceTrackerAgent()
    assert agent is not None

if __name__ == "__main__":
    pytest.main([__file__])
