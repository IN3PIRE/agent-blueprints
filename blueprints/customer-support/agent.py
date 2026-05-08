"""Customer Support Agent - Automated support ticket handling using LangChain."""

from typing import Dict, List, Optional
from langchain.agents import AgentExecutor, create_react_agent
from langchain.llms import OpenAI
from langchain.tools import Tool
from langchain.prompts import PromptTemplate


class CustomerSupportAgent:
    """Agent for handling customer support tickets."""
    
    def __init__(self,
                 model: str = "gpt-4",
                 api_key: Optional[str] = None):
        """
        Initialize the Customer Support agent.
        
        Args:
            model: LLM model to use
            api_key: Optional API key
        """
        self.model = model
        self.api_key = api_key
        self.llm = OpenAI(model=model, api_key=api_key, temperature=0.5)
        
        self.tools = self._get_tools()
        self.agent = self._create_agent()
    
    def _get_tools(self) -> List[Tool]:
        """Get support tools."""
        return [
            Tool(
                name="classify_ticket",
                func=self._classify_ticket,
                description="Classify ticket by category and priority"
            ),
            Tool(
                name="search_knowledge_base",
                func=self._search_kb,
                description="Search knowledge base for solutions"
            ),
            Tool(
                name="generate_response",
                func=self._generate_response,
                description="Generate customer response"
            ),
            Tool(
                name="escalate_ticket",
                func=self._escalate,
                description="Escalate to human agent"
            )
        ]
    
    def _classify_ticket(self, ticket_text: str) -> str:
        """Classify the ticket."""
        categories = ["technical", "billing", "general", "bug_report"]
        return f"Category: technical, Priority: medium"
    
    def _search_kb(self, query: str) -> str:
        """Search knowledge base."""
        return "Found 3 similar issues in KB"
    
    def _generate_response(self, issue: str, solution: str) -> str:
        """Generate response."""
        return f"Response: {solution}"
    
    def _escalate(self, reason: str) -> str:
        """Escalate ticket."""
        return f"Escalated: {reason}"
    
    def _create_agent(self) -> AgentExecutor:
        """Create support agent."""
        template = """You are a helpful customer support agent.

{tools}

Use format:
Question: customer issue
Thought: analyze
Action: action
Action Input: input
Observation: result
Thought: I know the answer
Final Answer: response

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
    
    def handle_ticket(self, ticket_text: str, customer_info: Dict = None) -> Dict:
        """Handle a support ticket."""
        classification = self._classify_ticket(ticket_text)
        kb_results = self._search_kb(ticket_text)
        
        response = self.agent.run(f"Respond to: {ticket_text}")
        
        return {
            "ticket": ticket_text,
            "classification": classification,
            "kb_results": kb_results,
            "response": response,
            "escalated": False
        }


def handle_support_ticket(ticket_text: str) -> Dict:
    """Quick function to handle ticket."""
    agent = CustomerSupportAgent()
    return agent.handle_ticket(ticket_text)
