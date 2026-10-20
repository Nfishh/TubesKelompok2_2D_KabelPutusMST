# Starter Kit Matematika Diskrit Lanjut: Baseline Architecture & Semantic Logging

Proyek ini adalah *starter kit* pembelajaran dan eksperimen algoritma graf berbasis **SOLID Principles**, **Data-Driven Testing (YAML)**, dan **Quantitative-First Semantic Logging**.

Tujuan utama dari arsitektur ini adalah menyediakan fondasi kode yang modular, efisien, dan siap digunakan oleh mahasiswa untuk analisis *white-box trace* algoritma graf dasar (Baseline) hingga State-of-the-Art (SOTA).

---

## 📐 Arsitektur & Prinsip Desain (SOLID)

Arsitektur proyek memisahkan tanggung jawab modul secara tegas sesuai prinsip rekayasa perangkat lunak:

1. **Single Responsibility Principle (SRP):**
   - `core/base_algorithm.py`: Hanya mengurus abstraksi algoritma dan pencatatan log kuantitatif murni.
   - `core/graph_model.py`: Menyediakan wrapper spasial untuk NetworkX `DiGraph`.
   - `cases/scenario_loader.py`: Hanya mengurus pembacaan YAML dan rekonstruksi model graf.
   - `scripts/`: Khusus untuk eksekusi simulasi, visualisasi, dan pengujian performa.
   - `tests/`: Khusus untuk pengujian unit otomatis (*headless*) dan diagnostik *scaffolding*.

2. **Open/Closed Principle (OCP) & Inheritance:**
   - Semua algoritma pencarian harus menuruni (*inherit*) `BaseGraphAlgorithm`.
   - Algoritma SOTA wajib menuruni kelas Baseline Parent-nya dan melakukan *override* pada metode spesifik (misalnya `handle_dynamic_event`).

3. **Separation of Execution & Testing:**
   - Folder `tests/` berjalan secara *headless* (tanpa memunculkan popup jendela GUI) agar kompatibel dengan *test runner* otomatis seperti `pytest`.
   - Folder `scripts/` menyediakan *entry point* interaktif untuk menampilkan grafik spasial (`SimpleGraphVisualizer`) dan mengekspor log JSON.

---

## 📁 Struktur Direktori Terstandar (Strict Layout)

```text
matdis-sota-starterkit/
├── README.md                      # Dokumentasi & Panduan Utama
├── TUTORIAL.md                    # Tutorial Data-Driven Simulation Runner
├── GLOSSARY.md                    # Panduan Kosa Kata Semantic Logging
├── CASESS.md                      # Daftar 28 Kasus & Pemetaan Algoritma
├── requirements.txt               # Dependencies (networkx, pyyaml, matplotlib)
│
├── config/
│   └── settings.py                # Konfigurasi Path, Batch, & Parameter Global
│
├── core/                          # Core Abstract Infrastructure
│   ├── base_algorithm.py          # Abstract Parent Class + Quantitative Logger
│   ├── graph_model.py             # SpatialGraphModel Wrapper
│   ├── simulation_runner.py       # Orkestrasi Fase Simulasi + Timer
│   ├── simulation_observers.py    # Observer Konsol, Visualizer, & Trace Export
│   └── visualizer.py              # SimpleGraphVisualizer (Matplotlib)
│
├── cases/                         # Data-Driven Scenario Management
│   ├── scenario_loader.py         # YAML Parser to SpatialGraphModel
│   └── scenarios/                 # Naskah Kasus YAML (28 Kasus)
│
├── algorithms/                    # Algorithm Implementations
│   ├── registry.py                # AlgorithmRegistry (Factory + Alias Kategori)
│   └── pathfinding/
│       └── static_dijkstra.py     # Baseline Dijkstra Parent Implementation
│
├── tests/                         # AUTOMATED TESTING & SCAFFOLDING (PyTest Ready)
│   ├── test_scenario_loader.py    # Unit Test YAML Loader & Graph Builder
│   ├── test_dijkstra.py           # Unit Test Kebenaran Algoritma Dijkstra
│   ├── test_scaffolding.py        # Framework Auditor Diagnostik untuk SOTA
│   └── test_all_scenarios.py      # Audit Parametrized Kontrak 28 Skenario
│
└── scripts/                       # EXECUTION RUNNERS (Simulations & Benchmarks)
    ├── cli_utils.py               # Resolver Path Skenario (file/folder/--all)
    ├── run_simulation.py          # Entry Point Utama: Visualisasi + Export JSON
    └── run_benchmark.py           # Entry Point Benchmark: Runtime & Step Count
```

---

## 🛠️ Cara Menggunakan Scripts & Tests

### 1. Menjalankan Simulasi Spasial & Ekspor JSON (`scripts/`)

Untuk mengeksekusi simulasi kasus, melihat grafik rute di Matplotlib, dan mengekspor log kuantitatif ke folder `output/`:

```bash
# Menjalankan skenario default (case_08_warga_nonton.yaml)
python -m scripts.run_simulation

# Memilih file YAML skenario spesifik (bisa lebih dari satu)
python -m scripts.run_simulation cases/scenarios/case_01_kobra_banjir.yaml
python -m scripts.run_simulation cases/scenarios/case_01_kobra_banjir.yaml cases/scenarios/case_04_pasar_tumpah.yaml

# Menjalankan seluruh 28 skenario sekaligus
python -m scripts.run_simulation --all

# Memilih algoritma dari registry secara eksplisit
python -m scripts.run_simulation --all --algorithm pathfinding
```

> **Ekstensi Algoritma (Open/Closed):** Runner tidak pernah hardcode kelas solver.
> Algoritma dipilih via `AlgorithmRegistry` (`algorithms/registry.py`) dengan urutan:
> argumen CLI `--algorithm` → key `algorithm:` di YAML → `DEFAULT_ALGORITHM` di `config/settings.py`.
> Algoritma baru (mis. `spanning_tree`, `maxflow`, `coloring`) cukup mewarisi
> `BaseGraphAlgorithm`, lalu mendaftar diri dengan
> `AlgorithmRegistry.register("nama_algoritma", KelasAlgoritma)` di akhir modulnya.
> Panduan lengkap: lihat [TUTORIAL.md](TUTORIAL.md).

### 2. Analisis Performa & Trade-off (`scripts/`)

Untuk mengukur waktu eksekusi dalam milidetik (ms) dan total *step count* dari algoritma:

```bash
python -m scripts.run_benchmark
```

### 3. Pengujian Otomatis & Scaffolding Diagnostik (`tests/`)

Gunakan `pytest` untuk memastikan seluruh unit tes dan kontrak interface algoritma berjalan valid 100% tanpa bug:

```bash
# Menjalankan seluruh unit test otomatis
pytest

# Jalankan pengujian spesifik dengan output terperinci
pytest -v tests/test_dijkstra.py
```

---

## 🧪 Contoh Penggunaan & Contoh Output

### 1. Contoh Script Simulasi (`scripts/run_simulation.py`)

```python
import sys
from algorithms.pathfinding.static_dijkstra import StaticDijkstra
from cases.scenario_loader import ScenarioLoader
from config.settings import DEFAULT_YAML_SCENARIO
from core.visualizer import SimpleGraphVisualizer


def run_simulation(yaml_path: str):
    # 1. Load Scenario & Build Spatial Graph Model
    loader = ScenarioLoader(yaml_path)
    metadata = loader.get_metadata()
    graph_model = loader.build_graph_model()
    plan = loader.get_execution_plan()

    start_node = plan["start_node"]
    goal_node = plan["goal_node"]

    # 2. Inisialisasi Visualizer & Solver
    viz = SimpleGraphVisualizer(graph_model.nx_graph)
    solver = StaticDijkstra(graph_model)

    print(f"=== RUNNING SIMULATION: {metadata['title']} ===")

    # 3. Phase 1: Initial Route
    path_1, cost_1 = solver.run(start_node, goal_node)
    print(f"-> Rute Awal  : {path_1} (Cost: {cost_1})")
    viz.draw_snapshot(
        title=f"Kondisi Normal - Rute: {path_1} (Cost: {cost_1})", active_path=path_1
    )

    # 4. Phase 2: Dynamic Event Injection
    for event in plan.get("events", []):
        target_edge = tuple(event["target_edge"])
        event_data = {
            "edge": target_edge,
            "new_weight": event["new_weight"],
            "start": start_node,
            "goal": goal_node,
        }

        path_2, cost_2 = solver.handle_dynamic_event(event_data)
        print(f"-> Rute Baru  : {path_2} (Cost: {cost_2})")
        viz.draw_snapshot(
            title=f"Event Injected - Rute Baru: {path_2} (Cost: {cost_2})",
            active_path=path_2,
            highlighted_edge=target_edge,
        )

    # 5. Export Quantitative Trace JSON
    output_filename = f"output_{metadata['case_id']}.json"
    saved_path = solver.export_trace_json(
        output_filename, metadata={**metadata, "algorithm": solver.__class__.__name__}
    )
    print(f"\n[SUCCESS] Quantitative Trace Log exported to: {saved_path}")


if __name__ == "__main__":
    yaml_file = sys.argv[1] if len(sys.argv) > 1 else str(DEFAULT_YAML_SCENARIO)
    run_simulation(yaml_file)
```

### 2. Contoh Unit Test Algoritma (`tests/test_dijkstra.py`)

```python
import pytest
from algorithms.pathfinding.static_dijkstra import StaticDijkstra
from cases.scenario_loader import ScenarioLoader
from config.settings import DEFAULT_YAML_SCENARIO


@pytest.fixture
def loaded_scenario():
    loader = ScenarioLoader(DEFAULT_YAML_SCENARIO)
    model = loader.build_graph_model()
    plan = loader.get_execution_plan()
    return model, plan


def test_dijkstra_initial_run(loaded_scenario):
    """Memastikan Dijkstra menemukan rute terpendek awal [0, 2, 3, 4] dengan cost 5."""
    model, plan = loaded_scenario
    solver = StaticDijkstra(model)

    path, cost = solver.run(plan["start_node"], plan["goal_node"])

    assert path == [0, 2, 3, 4]
    assert cost == 5


def test_dijkstra_dynamic_event_rerouting(loaded_scenario):
    """Memastikan Dijkstra berhasil menghitung ulang rute memutar [0, 1, 3, 4] dengan cost 10 pasca event."""
    model, plan = loaded_scenario
    solver = StaticDijkstra(model)
    start, goal = plan["start_node"], plan["goal_node"]

    solver.run(start, goal)

    event = plan["events"][0]
    event_data = {
        "edge": tuple(event["target_edge"]),
        "new_weight": event["new_weight"],
        "start": start,
        "goal": goal,
    }

    new_path, new_cost = solver.handle_dynamic_event(event_data)

    assert new_path == [0, 1, 3, 4]
    assert new_cost == 10
```

### 3. Contoh Scaffolding Auditor SOTA (`tests/test_scaffolding.py`)

Ketika mahasiswa mengimplementasikan algoritma SOTA baru (misalnya D* Lite), mereka dapat mengaudit kodingan mereka sendiri menggunakan `SOTAScaffoldingAuditor` untuk mendeteksi *error breakdown*:

```python
from tests.test_scaffolding import SOTAScaffoldingAuditor
from config.settings import DEFAULT_YAML_SCENARIO
# Import kelas algoritma SOTA buatan mahasiswa
from algorithms.pathfinding.static_dijkstra import StaticDijkstra


def test_audit_sota_algorithm():
    auditor = SOTAScaffoldingAuditor(StaticDijkstra, str(DEFAULT_YAML_SCENARIO))
    # Menjalankan 4 Stage Audit: Class Structure, Initial Path, Dynamic Events, & Trace Integrity
    assert auditor.run_full_diagnostic() is True
```

---

## 📊 Workflow Alur Kerja Mahasiswa

```text
1. Modifikasi/Buat Algoritma Baru (algorithms/pathfinding/)
                        │
                        ▼
2. Jalankan Headless Unit Test & Scaffolding (pytest)
   -> Memastikan tidak ada bug / exception / logika rute salah
                        │
                        ▼
3. Menjalankan Simulasi Spasial (python -m scripts.run_simulation)
   -> Memeriksa pergerakan rute secara intuitif via Matplotlib
                        │
                        ▼
4. Analisis Performa & Trade-off (python -m scripts.run_benchmark)
   -> Mencatat runtime (ms) dan total steps untuk laporan/TA
```
