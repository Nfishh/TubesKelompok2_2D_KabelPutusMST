from pathlib import Path
import pytest
from cases.scenario_loader import ScenarioLoader
from config.settings import DEFAULT_YAML_SCENARIO
from core.graph_model import SpatialGraphModel


def test_scenario_loader_file_not_found():
    """Memastikan loader melempar FileNotFoundError jika path YAML tidak valid."""
    with pytest.raises(FileNotFoundError):
        ScenarioLoader("invalid/path/non_existent.yaml")


def test_scenario_loader_structure():
    """Memastikan loader membaca metadata, topologi, dan execution_plan dengan benar."""
    loader = ScenarioLoader(DEFAULT_YAML_SCENARIO)

    metadata = loader.get_metadata()
    assert "case_id" in metadata
    assert "title" in metadata

    plan = loader.get_execution_plan()
    assert "start_node" in plan
    assert "goal_node" in plan
    assert "events" in plan
    assert isinstance(plan["events"], list)


def test_build_graph_model_integrity():
    """Memastikan loader berhasil mengonversi YAML menjadi objek SpatialGraphModel."""
    loader = ScenarioLoader(DEFAULT_YAML_SCENARIO)
    model = loader.build_graph_model()

    assert isinstance(model, SpatialGraphModel)
    
    # Audit Node & Edge Count dari N=5 Prototype
    G = model.nx_graph
    assert len(G.nodes) == 5, f"Diharapkan 5 nodes, tetapi didapat {len(G.nodes)}"
    assert len(G.edges) == 6, f"Diharapkan 6 edges, tetapi didapat {len(G.edges)}"

    # Audit Atribut Spasial & Label Node
    assert G.nodes[0]["label"] == "Titik Kumpul Pemukiman (Start)"
    assert "pos" in G.nodes[0]
    assert G[0][1]["weight"] == 2