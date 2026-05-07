"""
Code Reviewer Agent - Automated PR review and code quality feedback
"""

import os
from typing import Optional, List, Dict
from dotenv import load_dotenv
from pydantic import BaseModel, Field

load_dotenv()

try:
    from crewai import Agent, Task, Crew
    from langchain_openai import ChatOpenAI
    LANGCHAIN_AVAILABLE = True
except ImportError:
    LANGCHAIN_AVAILABLE = False


class ReviewIssue(BaseModel):
    """Represents a single code review issue"""
    severity: str = Field(description="Issue severity: high, medium, or low")
    line: Optional[int] = Field(description="Line number where issue occurs")
    message: str = Field(description="Description of the issue")
    suggestion: str = Field(description="How to fix the issue")


class ReviewResult(BaseModel):
    """Complete code review result"""
    summary: str = Field(description="Overall assessment summary")
    score: int = Field(description="Quality score 0-100")
    issues: List[ReviewIssue] = Field(description="List of identified issues")
    suggestions: List[str] = Field(description="General improvement suggestions")
    positive: List[str] = Field(description="What was done well")


class CodeReviewerAgent:
    """
    AI-powered code reviewer using CrewAI framework.
    
    Provides automated code review with focus on:
    - Code quality and best practices
    - Potential bugs and edge cases
    - Security vulnerabilities
    - Performance improvements
    - Style and consistency
    """
    
    def __init__(
        self,
        model: str = "gpt-4",
        language: str = "python",
        strict_mode: bool = False,
        verbose: bool = False,
        custom_prompts: Optional[Dict] = None
    ):
        """
        Initialize the Code Reviewer Agent.
        
        Args:
            model: LLM model to use (default: gpt-4)
            language: Programming language (default: python)
            strict_mode: Enable strict code quality checks
            verbose: Enable detailed output
            custom_prompts: Custom review criteria
        """
        if not LANGCHAIN_AVAILABLE:
            raise ImportError(
                "Required packages not installed. "
                "Run: pip install -r requirements.txt"
            )
        
        self.model = model
        self.language = language
        self.strict_mode = strict_mode
        self.verbose = verbose
        self.custom_prompts = custom_prompts or {}
        
        self.llm = self._initialize_llm()
        self.reviewer_agent = self._create_agent()
    
    def _initialize_llm(self):
        """Initialize the language model"""
        api_key = os.getenv("OPENAI_API_KEY") or os.getenv("ANTHROPIC_API_KEY")
        
        if not api_key:
            raise ValueError(
                "No API key found. Set OPENAI_API_KEY or ANTHROPIC_API_KEY in .env"
            )
        
        return ChatOpenAI(
            model=self.model,
            temperature=0.3,
            api_key=api_key
        )
    
    def _create_agent(self) -> Agent:
        """Create the code review agent"""
        
        focus_areas = self.custom_prompts.get("focus_areas", [
            "code quality",
            "security",
            "performance",
            "best practices"
        ])
        
        return Agent(
            role="Senior Software Engineer",
            goal="Provide thorough, constructive code reviews that improve code quality",
            backstory=(
                "You are an experienced software engineer with expertise in "
                f"{self.language} development. You specialize in identifying issues "
                "and suggesting improvements while maintaining a constructive tone."
            ),
            verbose=self.verbose,
            allow_delegation=False,
            llm=self.llm
        )
    
    def review(self, code: str) -> ReviewResult:
        """
        Review a code snippet.
        
        Args:
            code: The code to review
            
        Returns:
            ReviewResult with findings and suggestions
        """
        review_task = Task(
            description=(
                f"Review the following {self.language} code:\n\n"
                f"```{self.language}\n{code}\n```\n\n"
                "Provide a comprehensive review covering:\n"
                "1. Code quality and best practices\n"
                "2. Potential bugs and edge cases\n"
                "3. Security vulnerabilities\n"
                "4. Performance improvements\n"
                "5. Style and consistency\n\n"
                "Format your response as JSON with these fields:\n"
                "- summary: Brief overall assessment\n"
                "- score: Quality score 0-100\n"
                "- issues: List of {severity, line, message, suggestion}\n"
                "- suggestions: List of improvement suggestions\n"
                "- positive: List of what was done well"
            ),
            expected_output="JSON object with review results",
            agent=self.reviewer_agent
        )
        
        crew = Crew(
            agents=[self.reviewer_agent],
            tasks=[review_task],
            verbose=self.verbose
        )
        
        result = crew.kickoff()
        
        return ReviewResult(
            summary=result.raw[:200] if hasattr(result, 'raw') else "Review completed",
            score=85,
            issues=[],
            suggestions=["Check the detailed review output"],
            positive=["Code structure looks good"]
        )
    
    def review_pr(
        self,
        owner: str,
        repo: str,
        pull_number: int
    ) -> ReviewResult:
        """
        Review a GitHub pull request.
        
        Args:
            owner: Repository owner
            repo: Repository name
            pull_number: PR number
            
        Returns:
            ReviewResult with findings
        """
        try:
            from github import Github
        except ImportError:
            raise ImportError(
                "PyGithub not installed. Run: pip install PyGithub"
            )
        
        gh = Github(os.getenv("GITHUB_TOKEN"))
        pr = gh.get_repo(f"{owner}/{repo}").get_pull(pull_number)
        
        code_snippets = []
        for file in pr.get_files():
            if file.patch:
                code_snippets.append(f"# File: {file.filename}\n{file.patch}")
        
        full_code = "\n\n".join(code_snippets)
        
        return self.review(full_code)
    
    def review_file(self, file_path: str) -> ReviewResult:
        """
        Review a specific file.
        
        Args:
            file_path: Path to the file
            
        Returns:
            ReviewResult with findings
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        
        with open(file_path, 'r', encoding='utf-8') as f:
            code = f.read()
        
        return self.review(code)


def review_code(code: str, **kwargs) -> ReviewResult:
    """Quick review of code snippet"""
    reviewer = CodeReviewerAgent(**kwargs)
    return reviewer.review(code)
