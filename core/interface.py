from typing import Any, Dict, List, Protocol, Tuple
import networkx as nx


class IGraphAlgorithm(Protocol):
    """Kontrak wajib untuk semua Algoritma Graf (Baseline & SOTA)."""

    def run(self, start_node: int, goal_node: int) -> Tuple[List[int], float]:
        ...

    def handle_dynamic_event(self, event_data: Dict[str, Any]) -> Tuple[List[int], float]:
        ...


class ITraceable(Protocol):
    """Kontrak untuk kelas yang mendukung pencatatan log jejak (Tracing)."""

    def log_step(self, event_type: str, state_mutations: Dict[str, Any]) -> None:
        ...

    def export_trace_json(self, filename: str, metadata: Dict[str, Any] = None) -> Any:
        ...


class IGraphVisualizer(Protocol):
    """Kontrak untuk modul Visualizer."""

    def draw_snapshot(
        self,
        title: str,
        active_path: List[int] = None,
        highlighted_edge: Tuple[int, int] = None,
    ) -> None:
        ...