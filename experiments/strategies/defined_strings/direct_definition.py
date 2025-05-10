DIRECT_DEFINITION_PROMPT = """You are an expert in Machine Learning. Let's classify this problem using the standard definitions of ML problem types:

- Classification: Predicting discrete categories or labels
- Regression: Predicting continuous numerical values
- Clustering: Grouping similar data points without predefined labels
- Dimensionality Reduction: Reducing the number of features while preserving important information
- Anomaly Detection: Identifying unusual patterns or outliers
- Reinforcement Learning: Learning through interaction with an environment

Given these definitions, analyze this query:
User Query: {query}

Which type of ML problem does this best match? Explain why.""" 