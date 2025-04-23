TEMPLATE_MATCHING_PROMPT = """You are an expert in Machine Learning. Compare this query against these common ML problem templates:

TEMPLATES:
- "Predict [continuous value] based on [features]" → Regression
- "Classify [items] into [categories]" → Classification
- "Group similar [items] together" → Clustering
- "Find unusual patterns in [data]" → Anomaly Detection
- "Reduce dimensions of [data]" → Dimensionality Reduction
- "Learn to [action] through [interaction]" → Reinforcement Learning

User Query: {query}

Which template best matches this query? What type of ML problem is it?""" 