CHAIN_OF_THOUGHT_PROMPT = """You are an expert in Machine Learning. Let's think through how to classify this ML problem step by step. You may also use the context provided.

Context:
{context}

1. First, let's identify the key components of the query:
   User Query: {query}

2. What is the main goal or outcome being sought?

3. What type of data would be involved?

4. What are the possible ML problem types that could apply?

5. Based on these considerations, what is the most appropriate classification?

Please walk through your reasoning and according with the following enum:

1: Classification
2: Regression
3: Clustering

Respond with a json format like:

"reasoning": "",
"classification": "",

where reasoning is the explanation related with your classification and classification is only the number related with your final machine learning problem classification according with the enum.
"""
