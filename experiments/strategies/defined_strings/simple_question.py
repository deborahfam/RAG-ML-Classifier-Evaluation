SIMPLE_QUESTION_PROMPT = """You are an expert in Machine Learning. Use the context provided and answer these key questions to classify the ML problem:

Context:
{context}

1. What is the main goal of this task?
2. What type of output is needed?
3. Is there a target variable?
4. Are we predicting categories or continuous values?
5. Is this a supervised or unsupervised task?

User Query: {query}

Based on your answers, what type of ML problem is this?
According with the following enum:

1: Classification
2: Regression
3: Clustering

Respond with a json format like:

"reasoning": "",
"classification": "",

where reasoning is the explanation related with your classification and classification is only the number related with your final machine learning problem classification according with the enum.
"""
