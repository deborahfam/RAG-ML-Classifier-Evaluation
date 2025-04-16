GENERATE_QUESTIONS = """
    Generate 10 questions related with the following query 
    ##QUERY
    {query}
    And return the answer in a text format
"""

GENERATE_SUMMARIZE = """
    Generate a summary of the following text
    ##TEXT
    {query}
    And return the answer in a text format
"""

GENERATE_IDEAS = """
    Generate 5 principal ideas from the following text
    ##TEXT
    {query}
    And return the answer in a text format
"""

CLASSIFICATION_PROMPT = """
You will be given a question. Your task is to provide a 'total score' that represents how context-independent this question is.
Give your answer on a scale from general to specific, where general means that the question is very general like a greeting or questions without technical content from any branch of knowledge.
The questions may contain obscure technical nouns or acronyms such as SORBA, AutoML, automation or content considered technical in the field of Artificial Intelligence, IoT or automation, in this case the value is considered to be specific. Also be aware of some context related words that will be considered to be specific to.

Answer only with a JSON object with the following schema:

{{
    "explanation": "..." # your explanation for the classification
    "classification": "..." # the classification of the question, either general or specific
}}

Question: {query}
"""

SIMILITUDE_PROMPT = """
"You will be given 2 information texts. Give your answer on Yes or No where Yes means that the texts are in the same context and are talking about the same theme and No means that the text are different
 and are no talking about the same theme. The following texts are the information that you will be given: \n\n"

Answer only with a JSON object with the following schema:

{{
    "explanation": "..." # your explanation for the classification
    "classification": "..." # the classification of the question, either general or specific
}}

Text 1: {context}
Text 2: {transcription}

"""

GENERAL_TEMPLATE = """
The user made this query: {query}

Reply to the user, politely, that you are not designed to answer general-purpose questions,
such as topics related with the query. Inform the user that your purpose is to
answer general questions in the domain of automation and industrial applications
as well as questions regarding SORBA, its services and products,
and how to use the SORBA platform.
"""

RAG_TEMPLATE = """
The following is an extract of information that may be relevant for the user query
##EXTRACT
{context}

Given the previous context, you will answer the following query. Reply concisely in a formal and technical language.
##QUERY
{query}
"""

CHATBOT_TEMPLATE = """
You are a customer service bot implemented by the company SORBA-AI. Your purpose is to answer general questions in the domain of automation and industrial applications 
as well as questions regarding SORBA, its services and products, and how to use the SORBA platform.
"""

RAG_WITH_FEEDBACK_TEMPLATE = """
The following text is a response for a query made by the user
##TEXT
{text}

##QUERY
{query}

You task is, given the response and the query, fix the response to be more accurate with the query.
You also have to improve the answer keeping in mind that the response need to be in a technical language and
Modify your answer and keep it in a format where you are an assistant to return only the answers for the question, avoid frases like:
"In the provided extract"
"Based on the user query"
"In the previous context"
"""