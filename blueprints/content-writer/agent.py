"""Content Writer Agent - Blog post and article generation using CrewAI."""

from typing import Dict, List, Optional
from crewai import Agent, Task, Crew
import os


class ContentWriterAgent:
    """Agent for generating blog posts and articles."""
    
    def __init__(self,
                 model: str = "gpt-4",
                 tone: str = "professional",
                 api_key: Optional[str] = None):
        """
        Initialize Content Writer agent.
        
        Args:
            model: LLM model
            tone: Writing tone
            api_key: Optional API key
        """
        self.model = model
        self.tone = tone
        self.api_key = api_key or os.getenv('OPENAI_API_KEY')
        
        self.writer = self._create_writer_agent()
        self.editor = self._create_editor_agent()
    
    def _create_writer_agent(self) -> Agent:
        """Create writer agent."""
        return Agent(
            role='Content Writer',
            goal='Write engaging, well-researched content',
            backstory='Expert writer with years of experience',
            verbose=True,
            allow_delegation=False
        )
    
    def _create_editor_agent(self) -> Agent:
        """Create editor agent."""
        return Agent(
            role='Editor',
            goal='Polish and improve content quality',
            backstory='Professional editor with keen eye for detail',
            verbose=True
        )
    
    def write_article(self, topic: str, outline: List[str] = None, word_count: int = 1000) -> Dict:
        """
        Write a complete article.
        
        Args:
            topic: Article topic
            outline: Optional outline
            word_count: Target word count
            
        Returns:
            Generated article
        """
        writing_task = Task(
            description=f'Write a {word_count}-word article about {topic}',
            agent=self.writer,
            expected_output='Complete article'
        )
        
        editing_task = Task(
            description='Edit and polish the article',
            agent=self.editor,
            expected_output='Polished article'
        )
        
        crew = Crew(
            agents=[self.writer, self.editor],
            tasks=[writing_task, editing_task],
            verbose=True
        )
        
        result = crew.kickoff()
        
        return {
            "topic": topic,
            "content": str(result),
            "word_count": word_count,
            "tone": self.tone
        }
    
    def generate_outline(self, topic: str) -> List[str]:
        """Generate article outline."""
        return ["Introduction", "Main Point 1", "Main Point 2", "Conclusion"]


def write_content(topic: str, word_count: int = 1000) -> str:
    """Quick function to write content."""
    agent = ContentWriterAgent()
    result = agent.write_article(topic, word_count=word_count)
    return result["content"]
