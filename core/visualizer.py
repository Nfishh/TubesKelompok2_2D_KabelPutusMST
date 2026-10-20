import matplotlib.pyplot as plt
import networkx as nx


class SimpleGraphVisualizer:

    def __init__(self, graph: nx.DiGraph):
        self.graph = graph
        # Ambil posisi node dari attribute 'pos' di YAML
        self.pos = nx.get_node_attributes(graph, "pos")
        # Jika pos tidak didefinisikan, gunakan spring layout otomatis
        if not self.pos:
            self.pos = nx.spring_layout(graph)

    def draw_snapshot(
        self, title: str, active_path=None, highlighted_edge=None
    ):
        """Menggambar snapshot kondisi graf saat ini."""
        plt.figure(figsize=(8, 5))
        plt.title(title, fontsize=12, fontweight="bold")

        # 1. Gambar Semua Node
        nx.draw_networkx_nodes(
            self.graph,
            self.pos,
            node_size=700,
            node_color="lightblue",
            edgecolors="black",
        )

        # Label Nama Node (misal: "0: Pos Damkar")
        node_labels = {
            node: f"{node}\n({data.get('label', '')})"
            for node, data in self.graph.nodes(data=True)
        }
        nx.draw_networkx_labels(
            self.graph, self.pos, labels=node_labels, font_size=8
        )

        # 2. Gambar Semua Edge (Default: Hitam/Abu-abu)
        nx.draw_networkx_edges(
            self.graph,
            self.pos,
            edgelist=self.graph.edges(),
            edge_color="gray",
            arrows=True,
            arrowsize=15,
        )

        # Label Bobot Edge (Jarak/Waktu)
        edge_labels = nx.get_edge_attributes(self.graph, "weight")
        nx.draw_networkx_edge_labels(
            self.graph, self.pos, edge_labels=edge_labels, font_size=9
        )

        # 3. Highlight Edge Khusus (Misal: Edge yang tersumbat kerumunan -> Merah Tebal)
        if highlighted_edge:
            nx.draw_networkx_edges(
                self.graph,
                self.pos,
                edgelist=[highlighted_edge],
                edge_color="red",
                width=3,
                arrows=True,
                arrowsize=20,
            )

        # 4. Highlight Rute Hasil Algoritma (Warna Hijau Tebal)
        if active_path and len(active_path) > 1:
            path_edges = list(zip(active_path[:-1], active_path[1:]))
            nx.draw_networkx_edges(
                self.graph,
                self.pos,
                edgelist=path_edges,
                edge_color="green",
                width=4,
                arrows=True,
                arrowsize=20,
            )

        plt.axis("off")
        plt.tight_layout()
        plt.show()