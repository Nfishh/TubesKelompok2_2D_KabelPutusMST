import pytest
from algorithms.pathfinding.static_dijkstra import StaticDijkstra
from cases.scenario_loader import ScenarioLoader
from config.settings import DEFAULT_YAML_SCENARIO


@pytest.fixture
def loaded_scenario():
    """Fixture untuk menyiapkan model graf dan execution plan dari YAML."""
    loader = ScenarioLoader(DEFAULT_YAML_SCENARIO)
    model = loader.build_graph_model()
    plan = loader.get_execution_plan()
    return model, plan


def test_dijkstra_initial_run(loaded_scenario):
    """Memastikan Dijkstra menemukan rute terpendek awal [0, 1, 3, 4] dengan cost 6."""
    model, plan = loaded_scenario
    solver = StaticDijkstra(model)

    start = plan["start_node"]
    goal = plan["goal_node"]

    path, cost = solver.run(start, goal)

    # Ground Truth Kasus 8 Normal: 0 -> 1 (2m) -> 3 (2m) -> 4 (2m) = Total 6
    assert path == [0, 1, 3, 4], f"Rute awal salah: {path}"
    assert cost == 6, f"Cost awal salah: {cost}"


def test_dijkstra_dynamic_event_rerouting(loaded_scenario):
    """Memastikan Dijkstra berhasil menghitung ulang rute memutar [0, 1, 2, 3, 4] dengan cost 8 pasca event."""
    model, plan = loaded_scenario
    solver = StaticDijkstra(model)

    start = plan["start_node"]
    goal = plan["goal_node"]

    # Run Phase 1
    solver.run(start, goal)

    # Run Phase 2 (Injeksi Event Kerumunan Warga di Edge 1 -> 3)
    event = plan["events"][0]
    event_data = {
        "edge": tuple(event["target_edge"]),
        "new_weight": event["new_weight"],
        "start": start,
        "goal": goal,
    }

    new_path, new_cost = solver.handle_dynamic_event(event_data)

    # Ground Truth Pasca Event: Edge (1, 3) jadi 99.
    # Rute memutar via Gang Mawar: 0 -> 1 (2m) -> 2 (1m) -> 3 (3m) -> 4 (2m) = Total 8
    assert new_path == [0, 1, 2, 3, 4], f"Rute baru pasca-event salah: {new_path}"
    assert new_cost == 8, f"Cost baru pasca-event salah: {new_cost}"


def test_dijkstra_tracing_logs(loaded_scenario):
    """Memastikan logging kuantitatif (step count & delta logs) terekam secara otomatis."""
    model, plan = loaded_scenario
    solver = StaticDijkstra(model)

    solver.run(plan["start_node"], plan["goal_node"])

    assert solver.step_count > 0, "Step count tidak bertambah"
    assert len(solver.delta_logs) > 0, "Delta logs kosong"
    
    # Audit struktur log pertama
    first_log = solver.delta_logs[0]
    assert "step" in first_log
    assert "event_type" in first_log
    assert "mutations" in first_log
    assert first_log["event_type"] == "INITIALIZATION"