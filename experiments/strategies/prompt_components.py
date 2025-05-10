ENUM_DEFINITION = """
According with the following enum:

1: Classification
2: Regression
3: Clustering
"""

OUTPUT_FORMAT = lambda: '''Respond with a json format like:

"reasoning": "",
"classification": "",

where reasoning is the explanation related with your classification and classification is only the number related with your final machine learning problem classification according with the enum.'''
