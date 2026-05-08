"""Market Analyst Agent - Market research and competitive analysis using LangChain."""

from typing import Dict, List, Optional
from langchain.agents import AgentExecutor, create_react_agent
from langchain.llms import OpenAI
from langchain.tools import Tool
import json


class MarketAnalystAgent:
    """Agent for conducting market research and competitive analysis."""
    
    def __init__(self, model: str = "gpt-4", api_key: Optional[str] = None):
        """
        Initialize the Market Analyst agent.
        
        Args:
            model: LLM model to use
            api_key: Optional API key
        """
        self.llm = OpenAI(model=model, api_key=api_key, temperature=0.3)
        self.tools = self._get_tools()
        self.agent = self._create_agent()
    
    def _get_tools(self) -> List[Tool]:
        """Get available tools for market analysis."""
        return [
            Tool(
                name="search_companies",
                func=self._search_companies,
                description="Search for companies by industry or keyword"
            ),
            Tool(
                name="analyze_competitors",
                func=self._analyze_competitors,
                description="Analyze competitive landscape"
            ),
            Tool(
                name="market_size_estimation",
                func=self._estimate_market_size,
                description="Estimate total addressable market"
            ),
            Tool(
                name="trend_analysis",
                func=self._analyze_trends,
                description="Analyze market trends"
            )
        ]
    
    def _search_companies(self, query: str) -> str:
        """Search for companies matching criteria."""
        # Simulated company search
        return json.dumps({
            "query": query,
            "companies": [
                {"name": "Company A", "market_share": "25%", "growth": "15%"},
                {"name": "Company B", "market_share": "20%", "growth": "10%"},
                {"name": "Company C", "market_share": "15%", "growth": "20%"}
            ]
        }, indent=2)
    
    def _analyze_competitors(self, company_list: str) -> str:
        """Analyze competitive positioning."""
        return "Competitive analysis complete. Key insights: Market is fragmented with top 3 players controlling 60% share."
    
    def _estimate_market_size(self, industry: str) -> str:
        """Estimate market size for an industry."""
        return f"Estimated TAM for {industry}: $50B, SAM: $15B, SOM: $2B"
    
    def _analyze_trends(self, sector: str) -> str:
        """Analyze market trends."""
        return f"Key trends in {sector}: AI adoption, sustainability focus, remote work"
    
    def _create_agent(self) -> AgentExecutor:
        """Create the market analysis agent."""
        from langchain.prompts import PromptTemplate
        
        template = """You are an expert market analyst. Use the available tools to research and analyze markets.

{tools}

Use the following format:

Question: input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

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
    
    def analyze_market(self, industry: str, focus_areas: List[str] = None) -> Dict:
        """
        Conduct comprehensive market analysis.
        
        Args:
            industry: Industry to analyze
            focus_areas: Specific areas to focus on
            
        Returns:
            Dictionary containing market analysis results
        """
        focus = focus_areas or ["competitors", "market_size", "trends"]
        
        results = {
            "industry": industry,
            "analysis": {},
            "recommendations": []
        }
        
        # Analyze each focus area
        for area in focus:
            if area == "competitors":
                response = self.agent.run(f"Who are the main competitors in {industry}?")
                results["analysis"]["competitors"] = response
            elif area == "market_size":
                response = self.agent.run(f"What is the market size for {industry}?")
                results["analysis"]["market_size"] = response
            elif area == "trends":
                response = self.agent.run(f"What are the key trends in {industry}?")
                results["analysis"]["trends"] = response
        
        # Generate recommendations
        results["recommendations"] = self._generate_recommendations(results["analysis"])
        
        return results
    
    def _generate_recommendations(self, analysis: Dict) -> List[str]:
        """Generate strategic recommendations based on analysis."""
        recommendations = []
        
        if "competitors" in analysis:
            recommendations.append("Focus on differentiation strategies")
        if "market_size" in analysis:
            recommendations.append("Validate SOM before scaling")
        if "trends" in analysis:
            recommendations.append("Align product roadmap with identified trends")
        
        return recommendations


# Convenience function
def analyze_market(industry: str, focus_areas: List[str] = None) -> Dict:
    """Quick function to analyze a market."""
    agent = MarketAnalystAgent()
    return agent.analyze_market(industry, focus_areas)
