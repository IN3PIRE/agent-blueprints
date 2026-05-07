# 📊 Data Analyst Agent

> **Automated CSV/Excel analysis and insights using AI**

[![Framework: CrewAI](https://img.shields.io/badge/Framework-CrewAI-red)](https://github.com/joaomdmoura/crewAI)
[![Python: 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](../../LICENSE)

---

## 📋 Overview

Data Analyst Agent automatically analyzes structured data (CSV, Excel) and provides:

- 📈 Statistical summaries and insights
- 🔍 Pattern detection and anomalies
- 📊 Visualization suggestions
- 💡 Actionable recommendations
- 📉 Trend analysis
- 🎯 Correlation discovery

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Environment

```bash
OPENAI_API_KEY=your_key_here
```

### 3. Basic Usage

```python
from data_analyst.agent import DataAnalystAgent

analyst = DataAnalystAgent(model="gpt-4")

# Analyze CSV
result = analyst.analyze("sales_data.csv")
print(result.insights)

# Get specific analysis
result = analyst.get_summary_stats("customers.xlsx")
print(result)
```

## 📖 API Reference

### `DataAnalystAgent`

- `analyze(file_path)` - Full data analysis
- `get_summary_stats(file_path)` - Statistical summary
- `find_correlations(file_path)` - Correlation matrix
- `detect_anomalies(file_path)` - Find outliers
- `generate_report(file_path)` - Complete report

## 📦 Requirements

```
crewai>=0.20.0
pandas>=2.0.0
numpy>=1.24.0
openpyxl>=3.1.0
scipy>=1.10.0
```

## 📄 License

MIT License