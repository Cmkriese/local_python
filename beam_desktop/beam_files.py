"""Beam project and tabular analysis file operations."""

from __future__ import annotations

import csv
import json
from pathlib import Path

from beam_analysis import (
    Analysis,
    BeamState,
    beam_state_from_project,
    beam_state_to_project,
)


def write_beam_file(path: str | Path, state: BeamState) -> None:
    project = beam_state_to_project(state)
    content = json.dumps(project, indent=2, allow_nan=False) + "\n"
    Path(path).write_text(content, encoding="utf-8")


def read_beam_file(path: str | Path) -> BeamState:
    try:
        content = Path(path).read_text(encoding="utf-8")
        project = json.loads(content)
    except json.JSONDecodeError as error:
        raise ValueError(f"Invalid JSON project file: {error.msg}") from error
    return beam_state_from_project(project)


def write_results_csv(path: str | Path, analysis: Analysis) -> None:
    with Path(path).open("w", encoding="utf-8-sig", newline="") as output:
        writer = csv.writer(output)
        writer.writerow(("x (ft)", "V (kips)", "M (kip-ft)", "Deflection (in)"))
        for sample in analysis.shear_plot_samples:
            writer.writerow(
                (sample.x, sample.shear, sample.moment, sample.deflection)
            )
