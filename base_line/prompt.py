BASELINE_TEMPLATE = """
The following query is a Machine Learning problem.

##QUERY
{query}

You task is: classify the machine learning problem of the query.

Answer only with a JSON object with the following schema:

{{
    "explanation": "..." # your explanation for the classification.
    "classification": "..." # the classification of the machine learning problem.
}}

"""