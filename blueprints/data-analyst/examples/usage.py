"""
Data Analyst Agent - Example usage
"""

from agent import DataAnalystAgent, analyze_data

# Example 1: Quick analysis
print("=" * 50)
print("Example 1: Quick Analysis")
print("=" * 50)

result = analyze_data("sales_data.csv", model="gpt-4")

print(f"\nFile: {result.file_path}")
print(f"Shape: {result.summary['shape']}")
print(f"\nKey Insights:")
for insight in result.insights:
    print(f"  - {insight}")

print(f"\nAnomalies Detected: {len(result.anomalies)}")
print(f"Top Correlations: {result.correlations}")


# Example 2: Detailed analysis
print("\n" + "=" * 50)
print("Example 2: Step-by-Step Analysis")
print("=" * 50)

analyst = DataAnalystAgent(model="gpt-4", verbose=True)

# Get summary stats
summary = analyst.get_summary_stats("customers.xlsx")
print(f"\nSummary: {summary}")

# Find correlations
correlations = analyst.find_correlations("customers.xlsx")
print(f"\nCorrelations: {correlations}")

# Detect anomalies
anomalies = analyst.detect_anomalies("customers.xlsx")
print(f"\nAnomalies: {anomalies}")

# Full analysis
result = analyst.analyze("customers.xlsx")
print(f"\nFull Analysis Complete!")
