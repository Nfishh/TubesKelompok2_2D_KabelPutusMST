import heapq
import networkx as nx
from algorithms.registry import AlgorithmRegistry
from core.base_algorithm import BaseGraphAlgorithm


class StaticDijkstra(BaseGraphAlgorithm):

    SUPPORTED_EVENT_TYPES = frozenset({"DYNAMIC_EDGE_WEIGHT"})

    def __init__(self, graph: nx.DiGraph):
        super().__init__(graph)
        self.dist = {}
        self.parent = {}

    def run(self, start_node: int, goal_node: int):
        self.dist = {node: float("inf") for node in self.graph.nodes}
        self.parent = {node: None for node in self.graph.nodes}

        self.dist[start_node] = 0
        pq = [(0, start_node)]

        # LOG 1: Initialization State
        self.log_step(
            event_type="INITIALIZATION",
            state_mutations={
                "start_node": start_node,
                "distance_table": self.dist.copy(),
                "priority_queue": pq.copy(),
            },
        )

        while pq:
            current_dist, u = heapq.heappop(pq)

            if current_dist > self.dist[u]:
                continue

            if u == goal_node:
                # Rekonstruksi Rute
                path = []
                curr = goal_node
                while curr is not None:
                    path.append(curr)
                    curr = self.parent[curr]
                path.reverse()

                # LOG 2: Path Found
                self.log_step(
                    event_type="PATH_FOUND",
                    state_mutations={
                        "target_node": u,
                        "active_path": path,
                        "total_cost": current_dist,
                        "distance_table": self.dist.copy(),
                    },
                )
                return path, current_dist

            for v, edge_data in self.graph[u].items():
                weight = edge_data.get("weight", 1)
                new_dist = current_dist + weight

                if new_dist < self.dist[v]:
                    old_dist = self.dist[v]
                    self.dist[v] = new_dist
                    self.parent[v] = u
                    heapq.heappush(pq, (new_dist, v))

                    # LOG 3: Relaxation (Murni Kuantitatif)
                    self.log_step(
                        event_type="RELAX_EDGE",
                        state_mutations={
                            "current_node": u,
                            "evaluated_edge": [u, v],
                            "edge_weight": weight,
                            "old_dist": old_dist,
                            "new_dist": new_dist,
                            "priority_queue": pq.copy(),
                            "distance_table": self.dist.copy(),
                            "parent_table": self.parent.copy(),
                        },
                    )

        return [], float("inf")

    def handle_dynamic_event(self, event_data: dict):
        edge = event_data["edge"]
        new_weight = event_data["new_weight"]
        old_weight = self.graph[edge[0]][edge[1]].get("weight", 1)

        # Mutation pada Graf
        self.graph[edge[0]][edge[1]]["weight"] = new_weight

        # LOG 4: Dynamic Event Injection
        self.log_step(
            event_type="UPDATE_WEIGHT_EVENT",
            state_mutations={
                "target_edge": list(edge),
                "old_weight": old_weight,
                "new_weight": new_weight,
            },
        )

        return self.run(event_data["start"], event_data["goal"])


AlgorithmRegistry.register("static_dijkstra", StaticDijkstra)
AlgorithmRegistry.register_alias("pathfinding", "static_dijkstra")