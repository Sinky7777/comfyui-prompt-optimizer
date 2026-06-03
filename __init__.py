from .prompt_optimizer import PromptOptimizer, MetaDataLoader

NODE_CLASS_MAPPINGS = {
    "PromptOptimizer": PromptOptimizer,
    "MetaDataLoader": MetaDataLoader
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "PromptOptimizer": "Prompt Optimizer (提示词优化器)",
    "MetaDataLoader": "Meta Data Loader (元数据加载器)"
}

__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS']
