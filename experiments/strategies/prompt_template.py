from typing import Callable, Dict

class PromptTemplate:
    def __init__(
        self,
        name: str,
        instruction: str,
        guidance: str,
        format_output: Callable[[], str]
    ):
        self.name = name
        self.instruction = instruction
        self.guidance = guidance
        self.format_output = format_output

    def render(self, query: str, context: str) -> str:
        return self.instruction.format(context=context, query=query) + "\n\n" + self.guidance + "\n\n" + self.format_output()
