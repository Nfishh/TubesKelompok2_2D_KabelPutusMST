from typing import Dict, List, Type

from core.base_algorithm import BaseGraphAlgorithm


class AlgorithmRegistry:
    _algorithms: Dict[str, Type[BaseGraphAlgorithm]] = {}
    _aliases: Dict[str, str] = {}

    @classmethod
    def register(cls, algorithm_id: str, algorithm_cls: Type[BaseGraphAlgorithm]) -> None:
        cls._algorithms[algorithm_id] = algorithm_cls

    @classmethod
    def register_alias(cls, alias: str, algorithm_id: str) -> None:
        cls._aliases[alias] = algorithm_id

    @classmethod
    def resolve(cls, key: str) -> str:
        if key in cls._algorithms:
            return key
        if key in cls._aliases:
            return cls._aliases[key]
        raise KeyError(
            f"Algorithm '{key}' tidak terdaftar di registry. "
            f"Available algorithms: {cls.available()} | Aliases: {sorted(cls._aliases)}"
        )

    @classmethod
    def create(cls, key: str, graph_model) -> BaseGraphAlgorithm:
        algorithm_id = cls.resolve(key)
        return cls._algorithms[algorithm_id](graph_model)

    @classmethod
    def available(cls) -> List[str]:
        return sorted(cls._algorithms.keys())


def resolve_algorithm_key(cli_override, plan, metadata, default) -> str:
    return cli_override or plan.get("algorithm") or metadata.get("algorithm") or default
