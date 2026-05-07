"""
Data Analyst Agent - Automated data analysis and insights

Analyzes CSV/Excel files and provides statistical summaries, 
pattern detection, and actionable recommendations.
"""

from crewai import Agent, Task, Crew, Process
from langchain_openai import ChatOpenAI
import pandas as pd
import numpy as np
from typing import Dict, Any, Optional
from dataclasses import dataclass
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class AnalysisResult:
    """Data analysis result"""
    file_path: str
    summary: Dict[str, Any]
    insights: list[str]
    anomalies: list[Dict[str, Any]]
    correlations: Dict[str, float]
    recommendations: list[str]


class DataAnalystAgent:
    """AI-powered data analyst agent"""
    
    def __init__(
        self,
        model: str = "gpt-4",
        temperature: float = 0.0,
        verbose: bool = False,
    ):
        self.llm = ChatOpenAI(model=model, temperature=temperature)
        self.verbose = verbose
        
        self._create_agents()
    
    def _create_agents(self):
        """Create analysis agents"""
        
        self.statistician = Agent(
            role="Statistician",
            goal="Extract statistical insights from data",
            backstory="Expert in statistical analysis with 15+ years experience",
            tools=[],
            llm=self.llm,
            verbose=self.verbose,
            allow_delegation=False,
        )
        
        self.pattern_finder = Agent(
            role="Pattern Recognition Specialist",
            goal="Identify trends, patterns, and anomalies",
            backstory="Specializes in finding hidden patterns in complex datasets",
            llm=self.llm,
            verbose=self.verbose,
            allow_delegation=False,
        )
        
        self.insight_generator = Agent(
            role="Business Intelligence Analyst",
            goal="Generate actionable recommendations from data",
            backstory="Transforms data insights into business recommendations",
            llm=self.llm,
            verbose=self.verbose,
            allow_delegation=False,
        )
    
    def _load_data(self, file_path: str) -> pd.DataFrame:
        """Load data from CSV or Excel"""
        try:
            if file_path.endswith('.csv'):
                return pd.read_csv(file_path)
            elif file_path.endswith(('.xlsx', '.xls')):
                return pd.read_excel(file_path)
            else:
                raise ValueError("Unsupported file format. Use CSV or Excel.")
        except Exception as e:
            logger.error(f"Error loading data: {e}")
            raise
    
    def analyze(self, file_path: str) -> AnalysisResult:
        """Complete data analysis"""
        df = self._load_data(file_path)
        
        summary = self._get_summary(df)
        anomalies = self._detect_anomalies(df)
        correlations = self._find_correlations(df)
        
        insights_task = Task(
            description=f"""
            Analyze this dataset and provide key insights:
            
            Data Shape: {df.shape[0]} rows, {df.shape[1]} columns
            Columns: {', '.join(df.columns.tolist())}
            
            Summary Statistics:
            {summary}
            
            Detected Anomalies: {len(anomalies)}
            Top Correlations: {correlations}
            
            Provide 5-7 key insights about the data.
            Focus on business-relevant findings.
            """,
            agent=self.statistician,
            expected_output="List of 5-7 key insights with explanations"
        )
        
        recommendation_task = Task(
            description="""
            Based on the data analysis, provide 3-5 actionable recommendations.
            Consider:
            - Business opportunities
            - Areas of concern
            - Optimization suggestions
            - Next steps for deeper analysis
            """,
            agent=self.insight_generator,
            expected_output="List of 3-5 actionable recommendations"
        )
        
        crew = Crew(
            agents=[self.statistician, self.pattern_finder, self.insight_generator],
            tasks=[insights_task, recommendation_task],
            process=Process.sequential,
            verbose=self.verbose,
        )
        
        result = crew.kickoff()
        
        return AnalysisResult(
            file_path=file_path,
            summary=summary,
            insights=result.raw.split('\n') if result else [],
            anomalies=anomalies,
            correlations=correlations,
            recommendations=[],
        )
    
    def _get_summary(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Get statistical summary"""
        summary = {
            'shape': df.shape,
            'columns': df.columns.tolist(),
            'dtypes': df.dtypes.to_dict(),
            'numeric_summary': df.describe().to_dict(),
            'missing_values': df.isnull().sum().to_dict(),
        }
        return summary
    
    def _detect_anomalies(self, df: pd.DataFrame) -> list[Dict[str, Any]]:
        """Detect anomalies in numeric columns"""
        anomalies = []
        
        for col in df.select_dtypes(include=[np.number]).columns:
            if df[col].notnull().sum() > 0:
                mean = df[col].mean()
                std = df[col].std()
                
                outliers = df[abs(df[col] - mean) > 3 * std]
                if len(outliers) > 0:
                    anomalies.append({
                        'column': col,
                        'count': len(outliers),
                        'indices': outliers.index.tolist()[:5]
                    })
        
        return anomalies
    
    def _find_correlations(self, df: pd.DataFrame) -> Dict[str, float]:
        """Find top correlations"""
        corr_matrix = df.select_dtypes(include=[np.number]).corr()
        
        correlations = {}
        for col in corr_matrix.columns:
            for idx in corr_matrix.index:
                if col != idx:
                    key = f"{col}_vs_{idx}"
                    correlations[key] = corr_matrix.loc[idx, col]
        
        sorted_corr = dict(sorted(
            correlations.items(),
            key=lambda x: abs(x[1]),
            reverse=True
        )[:10])
        
        return sorted_corr
    
    def get_summary_stats(self, file_path: str) -> Dict[str, Any]:
        """Quick summary statistics"""
        df = self._load_data(file_path)
        return self._get_summary(df)
    
    def find_correlations(self, file_path: str) -> Dict[str, float]:
        """Find correlations in data"""
        df = self._load_data(file_path)
        return self._find_correlations(df)
    
    def detect_anomalies(self, file_path: str) -> list[Dict[str, Any]]:
        """Detect anomalies"""
        df = self._load_data(file_path)
        return self._detect_anomalies(df)


def analyze_data(file_path: str, model: str = "gpt-4") -> AnalysisResult:
    """Quick analysis function"""
    analyst = DataAnalystAgent(model=model)
    return analyst.analyze(file_path)
