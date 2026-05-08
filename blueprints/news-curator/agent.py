"""News Curator Agent - Daily news aggregation and summarization using AutoGen."""

from typing import Dict, List, Optional
import autogen
from autogen import AssistantAgent, UserProxyAgent
import json


class NewsCuratorAgent:
    """Agent for curating and summarizing daily news."""
    
    def __init__(self, 
                 model: str = "gpt-4",
                 sources: List[str] = None,
                 topics: List[str] = None,
                 api_key: Optional[str] = None):
        """
        Initialize the News Curator agent.
        
        Args:
            model: LLM model to use
            sources: News sources to monitor
            topics: Topics of interest
            api_key: Optional API key
        """
        self.model = model
        self.sources = sources or ["reuters", "bloomberg", "techcrunch"]
        self.topics = topics or ["technology", "business", "science"]
        self.api_key = api_key
        
        # Configure LLM
        llm_config = {"config_list": [{"model": self.model, "api_key": self.api_key}]}
        
        # Create agents
        self.curator = AssistantAgent(
            name="News_Curator",
            system_message=self._get_system_message(),
            llm_config=llm_config
        )
        
        self.user_proxy = UserProxyAgent(
            name="User_Proxy",
            human_input_mode="NEVER",
            max_consecutive_auto_reply=3
        )
    
    def _get_system_message(self) -> str:
        """Get the system message for the curator agent."""
        return """You are a professional news curator. Your role is to:
        1. Aggregate news from multiple sources
        2. Filter by relevance and quality
        3. Summarize key points concisely
        4. Organize by topic and importance
        5. Provide balanced perspectives
        
        Always cite sources and flag potential bias."""
    
    def curate_daily_briefing(self, date: str = "today") -> Dict:
        """
        Create a curated daily news briefing.
        
        Args:
            date: Date for the briefing (default: today)
            
        Returns:
            Dictionary containing curated news organized by topic
        """
        # Fetch news from sources
        raw_news = self._fetch_news(date)
        
        # Filter and rank by relevance
        ranked_news = self._rank_news(raw_news)
        
        # Generate summaries
        summaries = self._generate_summaries(ranked_news)
        
        # Organize by topic
        organized = self._organize_by_topic(summaries)
        
        return {
            "date": date,
            "sources": self.sources,
            "topics": self.topics,
            "news": organized,
            "total_articles": len(ranked_news)
        }
    
    def _fetch_news(self, date: str) -> List[Dict]:
        """Fetch news from configured sources."""
        # Simulated news fetching
        return [
            {"title": "AI Breakthrough in Healthcare", "source": "reuters", "topic": "technology"},
            {"title": "Markets Rally on Economic Data", "source": "bloomberg", "topic": "business"},
            {"title": "Climate Science Discovery", "source": "nature", "topic": "science"}
        ]
    
    def _rank_news(self, news_list: List[Dict]) -> List[Dict]:
        """Rank news by relevance and importance."""
        # Simple ranking - in production, use ML scoring
        for i, article in enumerate(news_list):
            article["relevance_score"] = 0.9 - (i * 0.1)
        return sorted(news_list, key=lambda x: x["relevance_score"], reverse=True)
    
    def _generate_summaries(self, news_list: List[Dict]) -> List[Dict]:
        """Generate concise summaries for each article."""
        for article in news_list:
            article["summary"] = f"Summary of {article['title']} from {article['source']}"
            article["key_points"] = [
                "Key point 1",
                "Key point 2",
                "Key point 3"
            ]
        return news_list
    
    def _organize_by_topic(self, news_list: List[Dict]) -> Dict[str, List[Dict]]:
        """Organize articles by topic."""
        organized = {}
        for article in news_list:
            topic = article["topic"]
            if topic not in organized:
                organized[topic] = []
            organized[topic].append(article)
        return organized
    
    def get_topic_briefing(self, topic: str, limit: int = 5) -> Dict:
        """
        Get a curated briefing for a specific topic.
        
        Args:
            topic: Topic to focus on
            limit: Maximum number of articles
            
        Returns:
            Curated briefing for the topic
        """
        daily = self.curate_daily_briefing()
        topic_news = daily["news"].get(topic, [])
        
        return {
            "topic": topic,
            "date": daily["date"],
            "articles": topic_news[:limit],
            "total": len(topic_news)
        }


# Convenience function
def curate_news(topics: List[str] = None) -> Dict:
    """Quick function to get daily news curation."""
    agent = NewsCuratorAgent(topics=topics)
    return agent.curate_daily_briefing()
