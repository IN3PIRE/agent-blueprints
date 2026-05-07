# 🤖 Code Reviewer Agent

> **Automated PR review and code quality feedback using AI**

[![Framework: CrewAI](https://img.shields.io/badge/Framework-CrewAI-red)](https://github.com/joaomdmoura/crewAI)
[![Python: 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](../../LICENSE)

---

## 📋 Overview

The Code Reviewer Agent automatically analyzes pull requests and code changes, providing intelligent feedback on:

- ✅ Code quality and best practices
- ✅ Potential bugs and edge cases
- ✅ Security vulnerabilities
- ✅ Performance improvements
- ✅ Style and consistency
- ✅ Test coverage suggestions

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Environment

Create a `.env` file:

```bash
OPENAI_API_KEY=your_openai_key_here
GITHUB_TOKEN=your_github_token (optional)
```

### 3. Basic Usage

```python
from code_reviewer.agent import CodeReviewerAgent

reviewer = CodeReviewerAgent(model="gpt-4")
review = reviewer.review("def foo(x): return x+1")
print(review)
```

## 📖 API Reference

### `CodeReviewerAgent`

- `review(code: str)` - Review code snippet
- `review_pr(owner, repo, pull_number)` - Review GitHub PR
- `review_file(file_path)` - Review specific file

## 📦 Requirements

```
crewai>=0.20.0
langchain>=0.1.0
python-dotenv>=1.0.0
PyGithub>=2.0.0
```

## 📄 License

MIT License - see [LICENSE](../../LICENSE)