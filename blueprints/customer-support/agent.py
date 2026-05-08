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
        self.model = model
        self.api_key = api_key
        self.llm = OpenAI(model=model, api_key=api_key, temperature=0.5)
        
        self.tools = self._get_tools()
        self.agent = self._create_agent()
    
    def _get_tools(self) -> List[Tool]:
        return [
            Tool(name="classify_ticket", func=self._classify_ticket, description="Classify ticket"),
            Tool(name="search_knowledge_base", func=self._search_kb, description="Search KB"),
            Tool(name="generate_response", func=self._generate_response, description="Generate response"),
            Tool(name="escalate_ticket", func=self._escalate, description="Escalate")
        ]
    
    def _classify_ticket(self, ticket_text: str) -> str:
        return "Category: technical, Priority: medium"
    
    def _search_kb(self, query: str) -> str:
        return "Found 3 similar issues"
    
    def _generate_response(self, issue: str, solution: str) -> str:
        return f"Response: {solution}"
    
    def _escalate(self, reason: str) -> str:
        return f"Escalated: {reason}"
    
    def _create_agent(self) -> AgentExecutor:
        template = """You are a helpful customer support agent.

{tools}

Use format:
Question: customer issue
Thought: analyze
Action: action
Action Input: input
Observation: result
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
    agent = CustomerSupportAgent()
    return agent.handle_ticket(ticket_text)
