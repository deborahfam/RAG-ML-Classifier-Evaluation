ONE_SHOT_PROMPT = """You are an expert in Machine Learning. Let me show you an example of how to classify ML problems, then you'll do the same for a new query. You may also use the additional context provided to help in your classification.

Example:
Query: "I need to predict whether an email is spam or not based on its content"
Classification: Binary Classification
Reason: The task involves predicting a binary outcome (spam/not spam) from text data

Context:
{context}

Now, classify this new query:
User Query: {query}
"""
