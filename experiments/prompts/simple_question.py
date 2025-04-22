SIMPLE_QUESTION_PROMPT = """You are an expert in Machine Learning. Answer these key questions to classify the ML problem:

1. What is the main goal of this task?
2. What type of output is needed?
3. Is there a target variable?
4. Are we predicting categories or continuous values?
5. Is this a supervised or unsupervised task?

User Query: {query}

Based on your answers, what type of ML problem is this?""" 