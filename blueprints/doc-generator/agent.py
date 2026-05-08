"""Documentation Generator Agent - Auto-generate docs from code using AutoGen."""

from typing import Dict, List, Optional
import autogen
from autogen import AssistantAgent


class DocGeneratorAgent:
    """Agent for automatic documentation generation."""
    
    def __init__(self,
                 model: str = "gpt-4",
                 style: str = "google",
                 api_key: Optional[str] = None):
        """
        Initialize the Doc Generator agent.
        
        Args:
            model: LLM model to use
            style: Documentation style (google, numpy, sphinx)
            api_key: Optional API key
        """
        self.model = model
        self.style = style
        self.api_key = api_key
        
        llm_config = {"config_list": [{"model": self.model, "api_key": self.api_key}]}
        
        self.doc_agent = AssistantAgent(
            name="Doc_Generator",
            system_message=self._get_system_message(),
            llm_config=llm_config
        )
    
    def _get_system_message(self) -> str:
        """Get system message for doc generation."""
        return """You are an expert technical writer specializing in Python documentation.
Your task is to generate clear, comprehensive, and well-structured documentation.

Follow the specified documentation style strictly (Google, NumPy, or Sphinx).
Include:
- Purpose and functionality
- Parameters with types and descriptions
- Return values
- Examples
- Notes on edge cases
"""
    
    def generate_docstring(self, code: str, func_name: str = None) -> str:
        """
        Generate documentation for a function or method.
        
        Args:
            code: Function/method code
            func_name: Optional function name
            
        Returns:
            Generated docstring
        """
        # This is a placeholder - actual implementation would use LLM
        return f'"""\nDocstring for {func_name or "function"}\n\nArgs:\n    None\n\nReturns:\n    None\n"""'
    
    def generate_readme(self, project_files: Dict[str, str]) -> str:
        """
        Generate README.md for a project.
        
        Args:
            project_files: Dict of filename -> content
            
        Returns:
            Generated README content
        """
        return "# Project\n\nDocumentation placeholder"
    
    def generate_api_docs(self, code_files: List[Dict]) -> str:
        """
        Generate API documentation.
        
        Args:
            code_files: List of code files with metadata
            
        Returns:
            Generated API documentation
        """
        return "# API Documentation\n\nPlaceholder"


# Convenience function
def generate_docs(code: str, doc_type: str = "docstring") -> str:
    """Quick function to generate documentation."""
    agent = DocGeneratorAgent()
    if doc_type == "docstring":
        return agent.generate_docstring(code)
    return ""
