BASIC_CHECKLIST_PROMPT = """You are an expert in Machine Learning. Use this checklist to classify the ML problem:

□ Is there a specific target variable to predict?
□ Is the target variable continuous or categorical?
□ Are there predefined labels or categories?
□ Is the goal to group similar items?
□ Is the goal to find unusual patterns?
□ Is the goal to reduce data complexity?

User Query: {query}

Based on your checklist answers, what type of ML problem is this?""" 