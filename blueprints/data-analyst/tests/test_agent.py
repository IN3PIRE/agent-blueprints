"""
Test Data Analyst Agent
"""

import pytest
import pandas as pd
import numpy as np
from pathlib import Path
from agent import DataAnalystAgent, analyze_data


@pytest.fixture
def sample_csv(tmp_path):
    """Create sample CSV for testing"""
    df = pd.DataFrame({
        'A': [1, 2, 3, 4, 5],
        'B': [2, 4, 6, 8, 10],
        'C': ['x', 'y', 'z', 'w', 'v']
    })
    path = tmp_path / "test.csv"
    df.to_csv(path, index=False)
    return str(path)


@pytest.fixture
def analyst():
    """Create analyst agent"""
    return DataAnalystAgent(model="gpt-3.5-turbo", verbose=False)


def test_load_data(sample_csv):
    """Test data loading"""
    analyst = DataAnalystAgent()
    df = analyst._load_data(sample_csv)
    
    assert df.shape == (5, 3)
    assert list(df.columns) == ['A', 'B', 'C']


def test_summary_stats(sample_csv):
    """Test summary statistics"""
    analyst = DataAnalystAgent()
    summary = analyst.get_summary_stats(sample_csv)
    
    assert summary['shape'] == (5, 3)
    assert 'numeric_summary' in summary
    assert 'missing_values' in summary


def test_correlations(sample_csv):
    """Test correlation detection"""
    analyst = DataAnalystAgent()
    correlations = analyst.find_correlations(sample_csv)
    
    assert isinstance(correlations, dict)
    # A and B should be highly correlated
    assert any(abs(v) > 0.9 for v in correlations.values())


def test_anomaly_detection():
    """Test anomaly detection"""
    df = pd.DataFrame({
        'A': [1, 2, 3, 4, 1000],  # 1000 is outlier
        'B': [1, 2, 3, 4, 5]
    })
    
    analyst = DataAnalystAgent()
    anomalies = analyst._detect_anomalies(df)
    
    assert len(anomalies) >= 1
    assert anomalies[0]['column'] == 'A'


def test_full_analysis(sample_csv):
    """Test complete analysis pipeline"""
    analyst = DataAnalystAgent(model="gpt-3.5-turbo")
    result = analyst.analyze(sample_csv)
    
    assert result.file_path == sample_csv
    assert result.summary is not None
    assert isinstance(result.insights, list)
    assert isinstance(result.anomalies, list)
    assert isinstance(result.correlations, dict)


def test_quick_analyze(sample_csv):
    """Test quick analyze function"""
    result = analyze_data(sample_csv, model="gpt-3.5-turbo")
    
    assert result is not None
    assert result.file_path == sample_csv


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
