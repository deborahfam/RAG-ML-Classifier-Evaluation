KEYWORD_ANALYSIS_PROMPT = """You are an expert in Machine Learning. Analyze these keywords and their implications for ML problem classification:

KEYWORDS AND THEIR MEANINGS:
- "predict", "forecast" → Likely supervised learning
- "classify", "categorize" → Classification
- "estimate", "value" → Regression
- "group", "cluster", "segment" → Clustering
- "detect", "find", "identify" → Could be classification or anomaly detection
- "reduce", "simplify" → Dimensionality reduction

User Query: {query}

What keywords do you see? What type of ML problem does this suggest?""" 