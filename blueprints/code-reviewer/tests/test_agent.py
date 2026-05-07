"""Tests for Code Reviewer Agent"""

import pytest
import os
from code_reviewer.agent import CodeReviewerAgent, ReviewResult


class TestCodeReviewerAgent:
    """Test suite for CodeReviewerAgent"""
    
    def test_initialization(self):
        """Test agent initialization"""
        agent = CodeReviewerAgent(
            model="gpt-3.5-turbo",
            language="python"
        )
        
        assert agent.language == "python"
        assert agent.model == "gpt-3.5-turbo"
    
    def test_review_simple_code(self):
        """Test reviewing simple code"""
        if not os.getenv("OPENAI_API_KEY"):
            pytest.skip("No API key available")
        
        agent = CodeReviewerAgent(model="gpt-3.5-turbo")
        
        code = "def add(a, b): return a + b"
        result = agent.review(code)
        
        assert isinstance(result, ReviewResult)
        assert hasattr(result, 'summary')
        assert hasattr(result, 'score')
    
    def test_review_finds_issues(self):
        """Test that review identifies obvious issues"""
        if not os.getenv("OPENAI_API_KEY"):
            pytest.skip("No API key available")
        
        agent = CodeReviewerAgent(
            model="gpt-3.5-turbo",
            strict_mode=True
        )
        
        code = """
def calculate_average(numbers):
    total = 0
    for i in range(len(numbers)):
        total += numbers[i]
    return total / len(numbers)
"""
        
        result = agent.review(code)
        
        assert result.score < 100


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
