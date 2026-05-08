"""Documentation generation prompts."""

DOCSTRING_PROMPT = """Generate a {style} style docstring for this code:

{code}

Include:
- One-line summary
- Detailed description
- Args with types
- Returns
- Raises
- Example usage
"""

README_PROMPT = """Generate a comprehensive README.md for this project.

Files:
{file_summaries}

Include:
- Project title and description
- Installation instructions
- Usage examples
- API reference
- Contributing guidelines
- License
"""

API_DOCS_PROMPT = """Generate API documentation for these modules.

Modules:
{modules}

Format as markdown with:
- Module overview
- Function signatures
- Parameter descriptions
- Return types
- Examples
"""
