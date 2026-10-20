from pathlib import Path

import pytest

from algorithms.registry import AlgorithmRegistry
from cases.scenario_loader import ScenarioLoader
from config.settings import CASES_DIR, DEFAULT_ALGORITHM, SCENARIO_FILE_PATTERNS


def _discover_scenario_files() -> list:
    files = []
    for pattern in SCENARIO_FILE_PATTERNS:
        files.extend(CASES_DIR.glob(pattern))
    return sorted(set(files))


SCENARIO_FILES = _discover_scenario_files()


@pytest.mark.parametrize("yaml_path", SCENARIO_FILES, ids=lambda p: p.stem)
def test_scenario_pipeline_contract(yaml_path: Path):
    """Audit kontrak data-driven untuk setiap skenario: load, build, run, event, trace."""
    loader = ScenarioLoader(yaml_path)

    metadata = loader.get_metadata()
    assert metadata.get("case_id"), f"{yaml_path.name}: case_id tidak ditemukan"
    assert metadata.get("title"), f"{yaml_path.name}: title tidak ditemukan"

    plan = loader.get_execution_plan()
    assert "start_node" in plan, f"{yaml_path.name}: start_node tidak ditemukan"
    assert "goal_node" in plan, f"{yaml_path.name}: goal_node tidak ditemukan"

    model = loader.build_graph_model()
    G = model.nx_graph
    assert len(G.nodes) > 0, f"{yaml_path.name}: graf tanpa node"
    assert len(G.edges) > 0, f"{yaml_path.name}: graf tanpa edge"
    assert plan["start_node"] in G.nodes, f"{yaml_path.name}: start_node tidak ada di graf"
    assert plan["goal_node"] in G.nodes, f"{yaml_path.name}: goal_node tidak ada di graf"

    solver = AlgorithmRegistry.create(DEFAULT_ALGORITHM, model)
    path, cost = solver.run(plan["start_node"], plan["goal_node"])
    assert isinstance(path, list) and len(path) >= 2, (
        f"{yaml_path.name}: rute awal tidak valid: {path}"
    )
    assert path[0] == plan["start_node"], f"{yaml_path.name}: rute tidak mulai dari start"
    assert path[-1] == plan["goal_node"], f"{yaml_path.name}: rute tidak berakhir di goal"

    supported_types = getattr(solver, "SUPPORTED_EVENT_TYPES", None)
    for idx, event in enumerate(plan.get("events", []), 1):
        assert event.get("type"), f"{yaml_path.name}: event #{idx} tanpa 'type'"
        assert event.get("description"), f"{yaml_path.name}: event #{idx} tanpa 'description'"

        if supported_types is not None and event["type"] not in supported_types:
            if "target_edge" in event:
                u, v = event["target_edge"]
                assert G.has_edge(u, v), (
                    f"{yaml_path.name}: event #{idx} menunjuk edge ({u}, {v}) yang tidak ada"
                )
            if "target_node" in event:
                assert event["target_node"] in G.nodes, (
                    f"{yaml_path.name}: event #{idx} menunjuk node {event['target_node']} yang tidak ada"
                )
            continue

        event_data = {
            "edge": tuple(event["target_edge"]),
            "new_weight": event["new_weight"],
            "start": plan["start_node"],
            "goal": plan["goal_node"],
        }
        new_path, new_cost = solver.handle_dynamic_event(event_data)
        assert isinstance(new_path, list) and len(new_path) >= 2, (
            f"{yaml_path.name}: rute pasca-event #{idx} tidak valid: {new_path}"
        )
        assert new_path[0] == plan["start_node"], (
            f"{yaml_path.name}: rute pasca-event #{idx} tidak mulai dari start"
        )
        assert new_path[-1] == plan["goal_node"], (
            f"{yaml_path.name}: rute pasca-event #{idx} tidak berakhir di goal"
        )

    assert solver.step_count > 0, f"{yaml_path.name}: delta log kosong"
    assert len(solver.delta_logs) == solver.step_count, (
        f"{yaml_path.name}: jumlah log tidak sinkron dengan step_count"
    )
