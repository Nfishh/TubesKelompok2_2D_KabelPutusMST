from collections import deque
import networkx as nx
from core.base_algorithm import BaseGraphAlgorithm
from core.graph_model import SpatialGraphModel


class FordFulkerson(BaseGraphAlgorithm):
    """Algoritma Dasar Maximum Flow (Edmonds-Karp / BFS Variant)."""

    def __init__(self, model: SpatialGraphModel):
        super().__init__(model)
        self.residual = nx.DiGraph()

    def _bfs(self, source, sink, parent) -> bool:
        visited = {source}
        queue = deque([source])

        while queue:
            u = queue.popleft()
            for v in self.residual.neighbors(u):
                capacity = self.residual[u][v].get("capacity", 0.0)
                if v not in visited and capacity > 0:
                    queue.append(v)
                    visited.add(v)
                    parent[v] = u
                    if v == sink:
                        return True
        return False

    def run(self, source_node: int, sink_node: int) -> float:
        # Inisialisasi Residual Graph
        self.residual.clear()
        self.residual.add_nodes_from(self.graph.nodes())

        for u, v, data in self.graph.edges(data=True):
            cap = float(data.get("capacity", data.get("weight", 1.0)))
            self.residual.add_edge(u, v, capacity=cap)
            if not self.residual.has_edge(v, u):
                self.residual.add_edge(v, u, capacity=0.0)

        max_flow = 0.0
        parent = {}

        self.log_step(
            event_type="INITIALIZATION",
            state_mutations={"source": source_node, "sink": sink_node, "max_flow": 0.0},
        )

        while self._bfs(source_node, sink_node, parent):
            path_flow = float("inf")
            s = sink_node

            # Cari bottleneck capacity sepanjang augmenting path
            while s != source_node:
                path_flow = min(path_flow, self.residual[parent[s]][s]["capacity"])
                s = parent[s]

            # Rekonstruksi jalur
            s = sink_node
            path = []
            while s != source_node:
                path.append(s)
                s = parent[s]
            path.append(source_node)
            path.reverse()

            # Update kapasitas residual
            v = sink_node
            while v != source_node:
                u = parent[v]
                self.residual[u][v]["capacity"] -= path_flow
                self.residual[v][u]["capacity"] += path_flow
                v = parent[v]

            max_flow += path_flow

            self.log_step(
                event_type="AUGMENTING_PATH_FOUND",
                state_mutations={
                    "path": path,
                    "flow_added": path_flow,
                    "current_max_flow": max_flow,
                },
            )

        return max_flow