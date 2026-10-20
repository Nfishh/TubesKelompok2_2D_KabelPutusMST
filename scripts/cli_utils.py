from pathlib import Path
from typing import Iterable, List, Union

from config.settings import (
    CASES_DIR,
    DEFAULT_SCENARIO_BATCH,
    DEFAULT_YAML_SCENARIO,
    SCENARIO_FILE_PATTERNS,
)


def collect_scenario_paths(
    entries: Iterable[Union[str, Path]], include_all: bool = False
) -> List[Path]:
    if include_all:
        return _glob_yaml(CASES_DIR)

    paths: List[Path] = []
    for entry in entries or []:
        path = Path(entry)
        if path.is_dir():
            paths.extend(_glob_yaml(path))
        else:
            paths.append(path)

    if not paths:
        if DEFAULT_SCENARIO_BATCH:
            paths.extend(Path(item) for item in DEFAULT_SCENARIO_BATCH)
        else:
            paths.append(Path(DEFAULT_YAML_SCENARIO))

    return list(dict.fromkeys(paths))


def _glob_yaml(directory: Path) -> List[Path]:
    files: List[Path] = []
    for pattern in SCENARIO_FILE_PATTERNS:
        files.extend(directory.glob(pattern))
    return sorted(set(files))
