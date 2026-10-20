from core.base_algorithm import BaseGraphAlgorithm
from core.graph_model import SpatialGraphModel


class GreedyColoring(BaseGraphAlgorithm):
    """Algoritma Dasar Pewarnaan Graf (Greedy Approach)."""

    def __init__(self, model: SpatialGraphModel):
        super().__init__(model)
        self.colors = {}

    def run(self) -> dict:
        nodes = sorted(list(self.graph.nodes()))
        self.colors = {node: None for node in nodes}

        self.log_step(
            event_type="INITIALIZATION",
            state_mutations={
                "total_nodes": len(nodes),
                "colors": self.colors.copy(),
            },
        )

        for node in nodes:
            # Cari warna tetangga yang sudah di-assign
            neighbor_colors = {
                self.colors[neighbor]
                for neighbor in self.graph.neighbors(node)
                if self.colors.get(neighbor) is not None
            }

            # Cari warna terkecil yang belum terpakai (0, 1, 2, ...)
            color = 0
            while color in neighbor_colors:
                color += 1

            self.colors[node] = color

            self.log_step(
                event_type="COLOR_ASSIGNED",
                state_mutations={
                    "current_node": node,
                    "assigned_color": color,
                    "neighbor_colors": sorted(list(neighbor_colors)),
                    "colors": self.colors.copy(),
                },
            )

        return self.colors