from experiments.strategies.prompts import PROMPT_TEMPLATES


def build_prompt(strategy: str, query: str, context: str) -> str:
    template = PROMPT_TEMPLATES[strategy]
    return template.render(query=query, context=context)
