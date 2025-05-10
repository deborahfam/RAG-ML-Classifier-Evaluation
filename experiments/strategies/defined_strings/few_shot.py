FEW_SHOT_PROMPT = """You are an expert in Machine Learning. I'll show you several examples of ML problem classification, then you'll classify a new query. You may also use the context provided to aid your decision.

Examples:
1. Query: "Predict house prices based on square footage and location"
   Classification: Regression
   Reason: Predicting continuous numerical values

2. Query: "Group customers into similar segments based on purchasing behavior"
   Classification: Clustering
   Reason: Unsupervised grouping of similar data points

3. Query: "Detect fraudulent transactions in a banking system"
   Classification: Classification
   Reason: Binary outcome prediction with imbalanced classes

Context:
{context}

Now, classify this new query:
User Query: {query}

According with the following enum:

1: Classification
2: Regression
3: Clustering

Respond with a json format like:

"reasoning": "",
"classification": "",


where reasoning is the explanation related with your classification and classification is only the number related with your final machine learning problem classification according with the enum.
"""
