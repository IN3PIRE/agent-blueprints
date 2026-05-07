"""
Example: Basic code review usage
"""

from agent import CodeReviewerAgent, review_code

# Quick review
def example_quick_review():
    """Quick code review example"""
    code = """
def calculate_sum(numbers):
    total = 0
    for i in range(len(numbers)):
        total += numbers[i]
    return total
"""
    
    result = review_code(code)
    
    print(f"Score: {result.score}/100")
    print(f"Summary: {result.summary}")
    print(f"Issues: {len(result.issues)}")
    print(f"Positive: {result.positive}")

# Advanced usage with custom settings
def example_custom_review():
    """Advanced review with custom settings"""
    agent = CodeReviewerAgent(
        model="gpt-4",
        language="python",
        strict_mode=True,
        verbose=True,
        custom_prompts={
            "focus_areas": ["security", "performance"]
        }
    )
    
    code = """
def authenticate(user_input, stored_hash):
    if user_input == stored_hash:
        return True
    return False
"""
    
    result = agent.review(code)
    
    print(f"\nSecurity Review Score: {result.score}/100")
    for issue in result.issues:
        print(f"- [{issue.severity}] {issue.message}")
        print(f"  Suggestion: {issue.suggestion}")

if __name__ == "__main__":
    example_quick_review()
    example_custom_review()
