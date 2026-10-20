import argparse
import sys
from pathlib import Path
from typing import List, Optional

from algorithms.registry import AlgorithmRegistry, resolve_algorithm_key
from cases.scenario_loader import ScenarioLoader
from config.settings import DEFAULT_ALGORITHM
from core.simulation_runner import SimulationResult, SimulationRunner
from scripts.cli_utils import collect_scenario_paths


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="scripts.run_benchmark",
        description="Benchmark runtime & step count untuk satu, beberapa, atau seluruh skenario.",
    )
    parser.add_argument(
        "scenarios",
        nargs="*",
        help="Path file YAML dan/atau folder skenario. Kosongkan untuk memakai default/batch.",
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Benchmark seluruh skenario di folder cases/scenarios.",
    )
    parser.add_argument(
        "-a",
        "--algorithm",
        default=None,
        help="Registry key/alias algoritma (mis. pathfinding, spanning_tree).",
    )
    return parser


def run_single(
    yaml_path: Path, algorithm_override: Optional[str] = None
):
    loader = ScenarioLoader(yaml_path)
    metadata = loader.get_metadata()
    plan = loader.get_execution_plan()
    graph_model = loader.build_graph_model()

    algorithm_key = resolve_algorithm_key(
        algorithm_override, plan, metadata, DEFAULT_ALGORITHM
    )
    solver = AlgorithmRegistry.create(algorithm_key, graph_model)

    result = SimulationRunner(solver=solver, plan=plan, metadata=metadata).execute()
    return algorithm_key, solver, result


def main(argv: Optional[List[str]] = None) -> None:
    args = build_parser().parse_args(argv)
    scenario_paths = collect_scenario_paths(args.scenarios, include_all=args.all)

    rows = []
    for yaml_path in scenario_paths:
        algorithm_key, solver, result = run_single(
            yaml_path, algorithm_override=args.algorithm
        )
        rows.append(
            {
                "case": result.metadata.get("case_id", yaml_path.stem),
                "algorithm": result.algorithm_name,
                "steps": solver.step_count,
                "initial_ms": result.initial_elapsed_ms,
                "reroute_ms": sum(r.elapsed_ms for r in result.reroutes),
            }
        )

    print("\n------------------------- BENCHMARK RESULTS -------------------------")
    print(f" {'Case':<30} {'Algorithm':<18} {'Steps':>6} {'Init (ms)':>12} {'Reroute (ms)':>14}")
    print(" " + "-" * 83)
    for row in rows:
        print(
            f" {row['case']:<30} {row['algorithm']:<18} {row['steps']:>6} "
            f"{row['initial_ms']:>12.4f} {row['reroute_ms']:>14.4f}"
        )
    print(" " + "-" * 83)
    print(f" Total scenario: {len(rows)}")
    print("----------------------------------------------------------------------")


if __name__ == "__main__":
    main(sys.argv[1:])
