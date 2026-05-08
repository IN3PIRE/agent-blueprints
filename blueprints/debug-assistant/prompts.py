"""Prompts for debugging."""

DEBUG_PROMPT = """Analyze the following code for potential bugs:

```{language}
{code}
```

Error message (if any):
{error_message}

Identify:
1. Syntax errors
2. Logic errors
3. Common anti-patterns
4. Performance issues
5. Security vulnerabilities

For each issue found:
- Describe the problem
- Explain why it's problematic
- Provide fixed code
- Suggest test case
"""

EXPLANATION_PROMPT = """Explain this bug in simple terms:

Bug: {bug_description}
Code: {code}

Provide:
1. What's wrong
2. Why it happens
3. How to fix it
4. How to prevent it in the future
"""
