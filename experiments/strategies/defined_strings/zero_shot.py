ZERO_SHOT_PROMPT = """You are an expert in Machine Learning. Given the following user query and additional context, determine what type of machine learning problem it represents.
Consider the key characteristics of different ML problem types (classification, regression, clustering, etc.) and classify accordingly.

Context:
{context}

User Query: {query}

Classify this as a specific type of ML problem
According with the following enum:

1: Classification
2: Regression
3: Clustering

Respond with a json format like:

"reasoning": "",
"classification": "",


where reasoning is the explanation related with your classification and classification is only the number related with your final machine learning problem classification according with the enum.
"""
