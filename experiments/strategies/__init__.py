from .standard import STANDARD_PROMPT
from .zero_shot import ZERO_SHOT_PROMPT
from .one_shot import ONE_SHOT_PROMPT
from .few_shot import FEW_SHOT_PROMPT
from .chain_of_thought import CHAIN_OF_THOUGHT_PROMPT
from .direct_definition import DIRECT_DEFINITION_PROMPT
from .simple_question import SIMPLE_QUESTION_PROMPT
from .template_matching import TEMPLATE_MATCHING_PROMPT
from .basic_checklist import BASIC_CHECKLIST_PROMPT
from .keyword_analysis import KEYWORD_ANALYSIS_PROMPT

PROMPT_STRATEGIES = {
    "standard": STANDARD_PROMPT,
    "zero_shot": ZERO_SHOT_PROMPT,
    "one_shot": ONE_SHOT_PROMPT,
    "few_shot": FEW_SHOT_PROMPT,
    "chain_of_thought": CHAIN_OF_THOUGHT_PROMPT,
    "direct_definition": DIRECT_DEFINITION_PROMPT,
    "simple_question": SIMPLE_QUESTION_PROMPT,
    "template_matching": TEMPLATE_MATCHING_PROMPT,
    "basic_checklist": BASIC_CHECKLIST_PROMPT,
    "keyword_analysis": KEYWORD_ANALYSIS_PROMPT
} 