"""Debug Assistant Agent - Bug detection and fix suggestions using LangChain."""

from typing import Dict, List, Optional, Tuple
from langchain.agents import AgentExecutor, create_react_agent
from langchain.llms import OpenAI
from langchain.tools import Tool
from langchain.prompts import PromptTemplate
import re


class DebugAssistantAgent:
    """Agent for detecting bugs and suggesting fixes in code."""
    
    def __init__(self, 
                 model: str = "gpt-4",
                 language: str = "python",
                 api_key: Optional[str] = None):
        """
        Initialize the Debug Assistant agent.
        
        Args:
            model: LLM model to use
            language: Programming language
            api_key: Optional API key
        """
        self.model = model
        self.language = language
        self.api_key = api_key
        self.llm = OpenAI(model=model, api_key=api_key, temperature=0.2)
        
        self.tools = self._get_tools()
        self.agent = self._create_agent()
    
    def _get_tools(self) -> List[Tool]:
        """Get available debugging tools."""
        return [
            Tool(
                name="analyze_error",
                func=self._analyze_error_message,
                description="Analyze error messages and stack traces"
            ),
            Tool(
                name="check_common_patterns",
                func=self._check_common_bug_patterns,
                description="Check for common bug patterns in code"
            ),
            Tool(
                name="suggest_fix",
                func=self._suggest_fix,
                description="Suggest potential fixes for identified issues"
            ),
            Tool(
                name="validate_syntax",
                func=self._validate_syntax,
                description="Check code syntax"
            )
        ]
    
    def _analyze_error_message(self, error: str) -> str:
        """Analyze an error message."""
        return f"Analysis of error: {error}"
    
    def _check_common_bug_patterns(self, code: str) -> str:
        """Check for common bug patterns."""
        patterns_found = []
        
        # Check for common Python issues
        if self.language == "python":
            if "== None" in code:
                patterns_found.append("Use 'is None' instead of '== None'")
            if re.search(r"for\s+\w+\s+in\s+\w+:\s*\n\s+\w+\[", code):
                patterns_found.append("Modifying dict during iteration - potential issue")
        
        return "Found patterns: " + "; ".join(patterns_found) if patterns_found else "No common patterns detected"
    
    def _suggest_fix(self, issue: str, code: str) -> str:
        """Suggest a fix for the issue."""
        return f"Suggested fix for {issue}: [Fix here]"
    
    def _validate_syntax(self, code: str) -> Tuple[bool, str]:
        """Validate code syntax."""
        try:
            compile(code, '<string>', 'exec')
            return True, "Syntax OK"
        except SyntaxError as e:
            return False, str(e)
    
    def _create_agent(self) -> AgentExecutor:
        """Create the debugging agent."""
        template = """You are an expert code debugger. Analyze code for bugs and suggest fixes.

{tools}

Use the following format:
Question: input problem
Thought: analyze the issue
Action: action to take
Action Input: input to action
Observation: result
Thought: I now know the final answer
Final Answer: diagnosis and fix suggestions

Begin!

Question: {input}
Thought:{agent_scratchpad}"""
        
        prompt = PromptTemplate(
            template=template,
            input_variables=["input", "agent_scratchpad"],
            partial_variables={
                "tools": "\n".join([t.name + ": " + t.description for t in self.tools]),
                "tool_names": ", ".join([t.name for t in self.tools])
            }
        )
        
        agent = create_react_agent(self.llm, self.tools, prompt)
        return AgentExecutor(agent=agent, tools=self.tools, verbose=True)
    
    def debug_code(self, code: str, error_message: str = None) -> Dict:
        """
        Analyze code for bugs and suggest fixes.
        
        Args:
            code: Code to analyze
            error_message: Optional error message
            
        Returns:
            Dictionary with debug results
        """
        results = {
            "language": self.language,
            "issues": [],
            "suggestions": [],
            "fixed_code": code
        }
        
        # Check syntax
        is_valid, syntax_msg = self._validate_syntax(code)
        if not is_valid:
            results["issues"].append({
                "type": "syntax_error",
                "message": syntax_msg,
                "severity": "critical"
            })
        
        # Check for common patterns
        pattern_results = self._check_common_bug_patterns(code)
        if "Found patterns" in pattern_results:
            results["issues"].append({
                "type": "common_pattern",
                "message": pattern_results,
                "severity": "warning"
            })
        
        # Analyze error message if provided
        if error_message:
            error_analysis = self.agent.run(f"Analyze this error: {error_message}")
            results["error_analysis"] = error_analysis
        
        # Generate fix suggestions
        if results["issues"]:
            fix_response = self.agent.run(f"Suggest fixes for: {code}")
            results["suggestions"].append(fix_response)
        
        return results
    
    def explain_issue(self, code: str, issue: str) -> str:
        """
        Explain a specific issue in the code.
        
        Args:
            code: Code with the issue
            issue: Description of the issue
            
        Returns:
            Explanation of the issue
        """
        response = self.agent.run(f"Explain this issue in the code: {code}\nIssue: {issue}")
        return response


# Convenience function
def debug_code(code: str, error_message: str = None, language: str = "python") -> Dict:
    """Quick function to debug code."""
    agent = DebugAssistantAgent(language=language)
    return agent.debug_code(code, error_message)
