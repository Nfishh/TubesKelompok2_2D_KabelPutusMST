from pathlib import Path

# --- DIRECTORY PATHS ---
BASE_DIR = Path(__file__).resolve().parent.parent
CASES_DIR = BASE_DIR / "cases" / "scenarios"
OUTPUT_DIR = BASE_DIR / "output"
TESTS_DIR = BASE_DIR / "tests"
SCRIPTS_DIR = BASE_DIR / "scripts"

# Pastikan folder output otomatis dibuat jika belum ada
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# --- LOGGING & TRACE CONFIGURATION ---
DEFAULT_INFINITY_REPRESENTATION = "inf"
JSON_INDENT = 2
ENSURE_ASCII = False

# --- DEFAULT SCENARIO ---
DEFAULT_YAML_SCENARIO = CASES_DIR / "case_08_warga_nonton.yaml"

# --- DEFAULT ALGORITHM (registry key atau alias kategori) ---
DEFAULT_ALGORITHM = "pathfinding"

# --- MULTI-SCENARIO BATCH ---
SCENARIO_FILE_PATTERNS = ("*.yaml", "*.yml")
DEFAULT_SCENARIO_BATCH = []