from typing import Any, Dict

from core.base_algorithm import BaseGraphAlgorithm
from core.simulation_runner import RerouteResult, SimulationObserver, SimulationResult
from core.visualizer import SimpleGraphVisualizer


class ConsoleReportObserver(SimulationObserver):

    def on_initial_route(self, result: SimulationResult) -> None:
        print(f"=== RUNNING SIMULATION: {result.metadata['title']} ===")
        print(f"Algorithm: {result.algorithm_name}")
        print(f"-> Rute Awal  : {result.initial_path} (Cost: {result.initial_cost})")

    def on_reroute(self, result: SimulationResult, reroute: RerouteResult) -> None:
        print(f"\n[EVENT INJECTED] {reroute.description}")
        print(f"-> Rute Baru  : {reroute.path} (Cost: {reroute.cost})")

    def on_event_skipped(self, result: SimulationResult, event: Dict[str, Any]) -> None:
        print(
            f"\n[EVENT SKIPPED] {event.get('type')} "
            f"tidak didukung oleh {result.algorithm_name} (butuh algoritma kategori lain)."
        )


class VisualizerSnapshotObserver(SimulationObserver):

    def __init__(self, graph: Any):
        self.visualizer = SimpleGraphVisualizer(graph)

    def on_initial_route(self, result: SimulationResult) -> None:
        self.visualizer.draw_snapshot(
            title=(
                f"Kondisi Normal - {result.metadata['title']}\n"
                f"Rute Awal: {result.initial_path} (Cost: {result.initial_cost})"
            ),
            active_path=result.initial_path,
        )

    def on_reroute(self, result: SimulationResult, reroute: RerouteResult) -> None:
        self.visualizer.draw_snapshot(
            title=(
                f"Event: {reroute.description}\n"
                f"Rute Baru: {reroute.path} (Cost: {reroute.cost})"
            ),
            active_path=reroute.path,
            highlighted_edge=reroute.target_edge,
        )


class TraceExportObserver(SimulationObserver):

    def __init__(self, solver: BaseGraphAlgorithm):
        self.solver = solver

    def on_complete(self, result: SimulationResult) -> None:
        filename = f"output_{result.metadata['case_id']}.json"
        saved_path = self.solver.export_trace_json(
            filename,
            metadata={**result.metadata, "algorithm": result.algorithm_name},
        )
        print(f"\n[SUCCESS] Quantitative Trace Log exported to: {saved_path}")
