import pkgutil, importlib
from pipelines.base import BasePromptPipeline


def discover_pipelines() -> dict[str, BasePromptPipeline]:
    registry: dict[str, BasePromptPipeline] = {}
    for finder, module_name, _ in pkgutil.iter_modules(__path__):
        module = importlib.import_module(f"pipelines.{module_name}")
        for attr in dir(module):
            cls = getattr(module, attr)
            if isinstance(cls, type) and issubclass(cls, BasePromptPipeline) and cls is not BasePromptPipeline:
                inst = cls()
                registry[inst.name] = inst
    return registry