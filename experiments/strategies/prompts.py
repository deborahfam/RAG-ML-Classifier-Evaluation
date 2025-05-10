from strategies.prompt_components import ENUM_DEFINITION, OUTPUT_FORMAT
from strategies.prompt_template import PromptTemplate


PROMPT_TEMPLATES = {
    "baseline": PromptTemplate(
        name="baseline",
        instruction="""The following is a user query.

User Query: {query}

Please classify it as one of the following types of machine learning problems:
""",
        guidance=ENUM_DEFINITION,
        format_output=OUTPUT_FORMAT
    ),
    "zero_shot": PromptTemplate(
        name="zero_shot",
        instruction="""You are an expert in Machine Learning. Given the following user query and additional context, determine what type of machine learning problem it represents.
Consider the key characteristics of different ML problem types (classification, regression, clustering, etc.) and classify accordingly.

Context:
{context}

User Query: {query}
""",
        guidance=ENUM_DEFINITION,
        format_output=OUTPUT_FORMAT
    ),
    "chain_of_thought": PromptTemplate(
        name="chain_of_thought",
        instruction="""You are an expert in Machine Learning. Let's think through how to classify this ML problem step by step. You may also use the context provided.

Context:
{context}

1. First, let's identify the key components of the query:
   User Query: {query}

2. What is the main goal or outcome being sought?

3. What type of data would be involved?

4. What are the possible ML problem types that could apply?

5. Based on these considerations, analize the classification of the problem based on the enum definition.
""",
        guidance=ENUM_DEFINITION,
        format_output=OUTPUT_FORMAT
    ),
    "few_shot": PromptTemplate(
        name="few_shot",
        instruction="""You are an expert in Machine Learning. I'll show you several examples of ML problem classification, then you'll classify a new query. You may also use the context provided to aid your decision.

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
""",
        guidance=ENUM_DEFINITION,
        format_output=OUTPUT_FORMAT
    ),
    "simple_question": PromptTemplate(
        name="simple_question",
        instruction="""You are an expert in Machine Learning. Use the context provided and answer these key questions to classify the ML problem:

Context:
{context}

1. What is the main goal of this task?
2. What type of output is needed?
3. Is there a target variable?
4. Are we predicting categories or continuous values?
5. Is this a supervised or unsupervised task?

User Query: {query}
""",
        guidance=ENUM_DEFINITION,
        format_output=OUTPUT_FORMAT
    )
}
