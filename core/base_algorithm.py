from abc import ABC, abstractmethod
import json
from pathlib import Path
from typing import Any, Dict, Optional

from config.settings import (
    DEFAULT_INFINITY_REPRESENTATION,
    ENSURE_ASCII,
    JSON_INDENT,
    OUTPUT_DIR,
)
from core.graph_model import SpatialGraphModel


class BaseGraphAlgorithm(ABC):

    SUPPORTED_EVENT_TYPES: Optional[frozenset] = None

    def __init__(self, graph_model: SpatialGraphModel):
        self.model = graph_model
        self.graph = graph_model.nx_graph  # Backwards compatibility dengan NetworkX
        self.step_count = 0
        self.delta_logs = []

    @abstractmethod
    def run(self, start_node: int, goal_node: int):
        pass

    @abstractmethod
    def handle_dynamic_event(self, event_data: Dict[str, Any]):
        pass

    def log_step(self, event_type: str, state_mutations: Dict[str, Any]):
        self.step_count += 1
        cleaned_mutations = self._sanitize_for_json(state_mutations)

        self.delta_logs.append({
            "step": self.step_count,
            "event_type": event_type,
            "mutations": cleaned_mutations,
        })

    def _sanitize_for_json(self, data: Any) -> Any:
        if isinstance(data, dict):
            return {k: self._sanitize_for_json(v) for k, v in data.items()}
        elif isinstance(data, list):
            return [self._sanitize_for_json(v) for v in data]
        elif data == float("inf"):
            return DEFAULT_INFINITY_REPRESENTATION
        return data

    def export_trace_json(self, filename: str, metadata: Dict[str, Any] = None) -> Path:
        target_path = OUTPUT_DIR / filename

        export_data = {
            "metadata": metadata or {},
            "total_steps": self.step_count,
            "initial_topology": self.model.get_topology_dict(),
            "raw_quantitative_trace": self.delta_logs,
        }

        with open(target_path, "w", encoding="utf-8") as f:
            json.dump(
                export_data,
                f,
                indent=JSON_INDENT,
                ensure_ascii=ENSURE_ASCII,
            )

        return target_path