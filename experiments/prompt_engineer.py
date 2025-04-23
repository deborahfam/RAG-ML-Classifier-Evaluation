from pipelines.standard import StandardPipeline
from pipelines.zero_shot import ZeroShotPipeline
from pipelines.one_shot import OneShotPipeline
from pipelines.few_shot import FewShotPipeline
from pipelines.chain_of_thought import ChainOfThoughtPipeline
from pipelines.direct_definition import DirectDefinitionPipeline
from pipelines.simple_question import SimpleQuestionPipeline
from pipelines.template_matching import TemplateMatchingPipeline
from pipelines.basic_checklist import BasicChecklistPipeline
from pipelines.keyword_analysis import KeywordAnalysisPipeline

PIPELINE_CLASSES = [
    StandardPipeline,
    ZeroShotPipeline,
    OneShotPipeline,
    FewShotPipeline,
    ChainOfThoughtPipeline,
    DirectDefinitionPipeline,
    SimpleQuestionPipeline,
    TemplateMatchingPipeline,
    BasicChecklistPipeline,
    KeywordAnalysisPipeline,
]
