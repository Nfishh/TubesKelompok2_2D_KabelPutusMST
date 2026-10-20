from core.base_algorithm import BaseGraphAlgorithm
from core.graph_model import SpatialGraphModel


class StaticKruskal(BaseGraphAlgorithm):
    """Algoritma Dasar Minimum Spanning Tree (Kruskal's Algorithm)."""

    def __init__(self, model: SpatialGraphModel):
        super().__init__(model)
        self.parent = {}
        self.rank = {}

    def _find(self, i):
        if self.parent[i] == i:
            return i
        self.parent[i] = self._find(self.parent[i])
        return self.parent[i]

    def _union(self, i, j):
        root_i = self._find(i)
        root_j = self._find(j)
        if root_i != root_j:
            if self.rank[root_i] < self.rank[root_j]:
                self.parent[root_i] = root_j
            elif self.rank[root_i] > self.rank[root_j]:
                self.parent[root_j] = root_i
            else:
                self.parent[root_j] = root_i
                self.rank[root_i] += 1
            return True
        return False

    def run(self) -> tuple[list, float]:
        mst_edges = []
        total_cost = 0.0

        # Kruskal membutuhkan graf tak berarah (Undirected)
        undirected_graph = self.graph.to_undirected()

        for node in undirected_graph.nodes():
            self.parent[node] = node
            self.rank[node] = 0

        # Ekstraksi dan sorting edge berdasarkan weight
        edges = []
        for u, v, data in undirected_graph.edges(data=True):
            weight = float(data.get("weight", 1.0))
            edges.append((weight, u, v))

        edges.sort(key=lambda x: x[0])

        self.log_step(
            event_type="INITIALIZATION",
            state_mutations={
                "total_edges": len(edges),
                "sorted_edges": [[u, v, w] for w, u, v in edges],
            },
        )

        for weight, u, v in edges:
            if self._find(u) != self._find(v):
                self._union(u, v)
                mst_edges.append((u, v, weight))
                total_cost += weight

                self.log_step(
                    event_type="EDGE_ADDED",
                    state_mutations={
                        "added_edge": [u, v],
                        "weight": weight,
                        "current_mst_count": len(mst_edges),
                        "total_cost": total_cost,
                    },
                )

        return mst_edges, total_cost