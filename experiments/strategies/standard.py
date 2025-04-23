STANDARD_PROMPT = """You are an expert in Machine Learning. Your task is to classify the following user query into a specific machine learning problem type.
You may use the additional context provided to help you understand the problem better.
Please analyze the query and determine if it's a classification, regression, clustering, or other type of ML problem.

Context:
{context}

User Query: {query}

Provide your classification and a brief explanation of why you chose that type."""
