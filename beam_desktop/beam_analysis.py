"""Beam reactions, diagrams, deflection, and section checks."""

from __future__ import annotations

from dataclasses import dataclass, replace
from math import isclose, isfinite
from typing import Callable, Literal


@dataclass(frozen=True)
class Section:
    ix: float
    sx: float
    weight: float | None = None


@dataclass(frozen=True)
class Material:
    elastic_modulus: float
    allowable_stress: float
    sections: dict[str, Section]


MATERIALS: dict[str, Material] = {
    "steel": Material(
        elastic_modulus=29_000,
        allowable_stress=30,
        sections={
            "W8x10": Section(30.8, 7.81, 10),
            "W10x12": Section(53.8, 10.9, 12),
            "W12x26": Section(204, 33.4, 26),
            "W14x22": Section(199, 29.0, 22),
            "W16x26": Section(301, 38.4, 26),
            "W18x35": Section(510, 57.6, 35),
            "W21x44": Section(843, 81.6, 44),
            "W24x55": Section(1350, 114, 55),
        },
    ),
    "lumber": Material(
        elastic_modulus=1_600,
        allowable_stress=0.900,
        sections={
            "2x8": Section(47.63, 13.14),
            "2x10": Section(98.93, 21.39),
            "2x12": Section(177.98, 31.64),
        },
    ),
}

PROJECT_FORMAT = "beam-designer"
PROJECT_VERSION = 1


@dataclass(frozen=True)
class BeamLoad:
    kind: Literal["point", "uniform"]
    magnitude: float
    position: float = 0.0
    start: float = 0.0
    end: float = 0.0


@dataclass(frozen=True)
class BeamState:
    support: Literal["simply-supported", "cantilever"]
    span: float
    loads: tuple[BeamLoad, ...]
    material: str
    section: str
    deflection_limit: int


@dataclass(frozen=True)
class Sample:
    x: float
    shear: float
    moment: float
    deflection: float


@dataclass(frozen=True)
class Extrema:
    maximum: Sample
    minimum: Sample
    absolute: Sample
    absolute_locations: tuple[float, ...]


@dataclass(frozen=True)
class Reactions:
    left: float
    right: float
    fixed_moment: float


@dataclass(frozen=True)
class Analysis:
    state: BeamState
    section: Section
    reactions: Reactions
    samples: tuple[Sample, ...]
    shear_plot_samples: tuple[Sample, ...]
    shear: Extrema
    moment: Extrema
    deflection: Extrema
    allowable_deflection: float
    bending_stress: float
    allowable_stress: float
    bending_utilization: float
    deflection_utilization: float

    def value_at(self, x: float) -> Sample:
        """Return the exact calculated values at a beam position."""
        return _sample_at(self.state, self.reactions, self.section, x)


@dataclass(frozen=True)
class Recommendation:
    section_name: str
    passes: bool
    governing_utilization: float


def validate_state(state: BeamState) -> list[str]:
    errors: list[str] = []
    if state.support not in ("simply-supported", "cantilever"):
        errors.append("Choose a supported beam type.")
    if not isfinite(state.span) or not 4 <= state.span <= 40:
        errors.append("Span must be from 4 to 40 ft.")
    if state.material not in MATERIALS:
        errors.append("Choose a material.")
    elif state.section not in MATERIALS[state.material].sections:
        errors.append("Choose a section available for the selected material.")
    if state.deflection_limit not in (240, 360):
        errors.append("Choose a deflection limit of L/240 or L/360.")

    for index, load in enumerate(state.loads, start=1):
        if not isfinite(load.magnitude):
            errors.append(f"Load {index} magnitude must be a number.")
        elif load.kind == "point":
            if not 0 <= load.magnitude <= 100:
                errors.append(f"Point load {index} magnitude must be from 0 to 100 kips.")
            if not isfinite(load.position) or not 0 <= load.position <= state.span:
                errors.append(f"Point load {index} position must be within the beam span.")
        elif load.kind == "uniform":
            if not 0 <= load.magnitude <= 10:
                errors.append(f"Uniform load {index} magnitude must be from 0 to 10 kips/ft.")
            if not isfinite(load.start) or not 0 <= load.start <= state.span:
                errors.append(f"Uniform load {index} start must be within the beam span.")
            if not isfinite(load.end) or not 0 <= load.end <= state.span:
                errors.append(f"Uniform load {index} end must be within the beam span.")
            if load.start > load.end:
                errors.append(f"Uniform load {index} start must be at or before its end.")
        else:
            errors.append(f"Load {index} has an unsupported load type.")
    return errors


def beam_state_to_project(state: BeamState) -> dict[str, object]:
    errors = validate_state(state)
    if errors:
        raise ValueError("Cannot save invalid beam: " + " ".join(errors))

    loads: list[dict[str, object]] = []
    for load in state.loads:
        if load.kind == "point":
            loads.append({
                "type": "point",
                "magnitude_kips": load.magnitude,
                "position_ft": load.position,
            })
        else:
            loads.append({
                "type": "uniform",
                "magnitude_kips_per_ft": load.magnitude,
                "start_ft": load.start,
                "end_ft": load.end,
            })
    return {
        "format": PROJECT_FORMAT,
        "version": PROJECT_VERSION,
        "beam": {
            "support": state.support,
            "span_ft": state.span,
            "material": state.material,
            "section": state.section,
            "deflection_limit": state.deflection_limit,
            "loads": loads,
        },
    }


def beam_state_from_project(data: object) -> BeamState:
    project = _project_mapping(data, "Project")
    if project.get("format") != PROJECT_FORMAT:
        raise ValueError("This is not a Beam Designer project file.")
    version = project.get("version")
    if type(version) is not int or version != PROJECT_VERSION:
        raise ValueError("Unsupported Beam Designer project version.")

    beam = _project_mapping(project.get("beam"), "Beam")
    support = _project_string(beam.get("support"), "Support")
    material = _project_string(beam.get("material"), "Material")
    section = _project_string(beam.get("section"), "Section")
    span = _project_number(beam.get("span_ft"), "Span")
    deflection_limit = beam.get("deflection_limit")
    if type(deflection_limit) is not int:
        raise ValueError("Deflection limit must be an integer.")
    serialized_loads = beam.get("loads")
    if not isinstance(serialized_loads, list):
        raise ValueError("Loads must be a list.")

    loads: list[BeamLoad] = []
    for index, serialized_load in enumerate(serialized_loads, start=1):
        load = _project_mapping(serialized_load, f"Load {index}")
        kind = _project_string(load.get("type"), f"Load {index} type")
        if kind == "point":
            loads.append(
                BeamLoad(
                    kind="point",
                    magnitude=_project_number(
                        load.get("magnitude_kips"), f"Point load {index} magnitude"
                    ),
                    position=_project_number(
                        load.get("position_ft"), f"Point load {index} position"
                    ),
                )
            )
        elif kind == "uniform":
            loads.append(
                BeamLoad(
                    kind="uniform",
                    magnitude=_project_number(
                        load.get("magnitude_kips_per_ft"),
                        f"Uniform load {index} magnitude",
                    ),
                    start=_project_number(
                        load.get("start_ft"), f"Uniform load {index} start"
                    ),
                    end=_project_number(
                        load.get("end_ft"), f"Uniform load {index} end"
                    ),
                )
            )
        else:
            raise ValueError(f"Load {index} has an unsupported type.")

    if support == "simply-supported":
        support_type: Literal["simply-supported", "cantilever"] = "simply-supported"
    elif support == "cantilever":
        support_type = "cantilever"
    else:
        raise ValueError("Unsupported support type.")
    state = BeamState(
        support=support_type,
        span=span,
        loads=tuple(loads),
        material=material,
        section=section,
        deflection_limit=deflection_limit,
    )
    errors = validate_state(state)
    if errors:
        raise ValueError("Invalid beam project: " + " ".join(errors))
    return state


def _project_mapping(value: object, label: str) -> dict[str, object]:
    if not isinstance(value, dict):
        raise ValueError(f"{label} must be an object.")
    result: dict[str, object] = {}
    for key, item in value.items():
        if not isinstance(key, str):
            raise ValueError(f"{label} contains a non-text key.")
        result[key] = item
    return result


def _project_string(value: object, label: str) -> str:
    if not isinstance(value, str):
        raise ValueError(f"{label} must be text.")
    return value


def _project_number(value: object, label: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(f"{label} must be a number.")
    number = float(value)
    if not isfinite(number):
        raise ValueError(f"{label} must be finite.")
    return number


def _uniform_extent(load: BeamLoad, span: float) -> tuple[float, float]:
    return max(0.0, load.start), min(span, load.end)


def _positive_part(value: float) -> float:
    return max(0.0, value)


def _sample_at(
    state: BeamState,
    reactions: Reactions,
    section: Section,
    x: float,
    *,
    before_point_load: bool = False,
) -> Sample:
    x = min(state.span, max(0.0, x))
    shear = reactions.left
    moment = reactions.fixed_moment + reactions.left * x
    for load in state.loads:
        if load.kind == "point":
            passed = load.position < x or (
                not before_point_load and isclose(load.position, x, abs_tol=1e-10)
            )
            if passed:
                shear -= load.magnitude
                moment -= load.magnitude * _positive_part(x - load.position)
        else:
            start, end = _uniform_extent(load, state.span)
            loaded_length = max(0.0, min(end, x) - start)
            shear -= load.magnitude * loaded_length
            moment -= load.magnitude * (
                _positive_part(x - start) ** 2 - _positive_part(x - end) ** 2
            ) / 2

    material = MATERIALS[state.material]
    ei = material.elastic_modulus * section.ix
    _, second_integral = _moment_integrals(state, reactions, x)
    if state.support == "simply-supported":
        end_integral = _moment_integrals(state, reactions, state.span)[1]
        second_integral -= (x / state.span) * end_integral
    deflection = -1728 * second_integral / ei
    return Sample(x, shear, moment, deflection)


def _moment_integrals(
    state: BeamState,
    reactions: Reactions,
    x: float,
) -> tuple[float, float]:
    """Integrate M and (x-t)M(t) exactly, with x and loads in feet."""
    first = reactions.fixed_moment * x + reactions.left * x**2 / 2
    second = reactions.fixed_moment * x**2 / 2 + reactions.left * x**3 / 6
    for load in state.loads:
        if load.kind == "point":
            distance = _positive_part(x - load.position)
            first -= load.magnitude * distance**2 / 2
            second -= load.magnitude * distance**3 / 6
        else:
            start, end = _uniform_extent(load, state.span)
            start_distance = _positive_part(x - start)
            end_distance = _positive_part(x - end)
            first -= load.magnitude * (start_distance**3 - end_distance**3) / 6
            second -= load.magnitude * (start_distance**4 - end_distance**4) / 24
    return first, second


def _bisect_zero(function: Callable[[float], float], left: float, right: float) -> float:
    left_value = function(left)
    for _ in range(60):
        middle = (left + right) / 2
        middle_value = function(middle)
        if abs(middle_value) < 1e-12 or right - left < 1e-10:
            return middle
        if (left_value < 0) == (middle_value < 0):
            left = middle
            left_value = middle_value
        else:
            right = middle
    return (left + right) / 2


def _unique_positions(values: list[float], tolerance: float = 1e-8) -> list[float]:
    result: list[float] = []
    for value in sorted(values):
        if not result or abs(value - result[-1]) > tolerance:
            result.append(value)
    return result


def _extrema(values: list[Sample], field: Literal["shear", "moment", "deflection"]) -> Extrema:
    maximum = max(values, key=lambda sample: getattr(sample, field))
    minimum = min(values, key=lambda sample: getattr(sample, field))
    magnitude = max(abs(getattr(sample, field)) for sample in values)
    tied = tuple(
        _unique_positions(
            [
                sample.x
                for sample in values
                if isclose(abs(getattr(sample, field)), magnitude, rel_tol=1e-8, abs_tol=1e-9)
            ]
        )
    )
    absolute = next(
        sample
        for sample in values
        if isclose(abs(getattr(sample, field)), magnitude, rel_tol=1e-8, abs_tol=1e-9)
    )
    return Extrema(maximum, minimum, absolute, tied)


def analyze(state: BeamState) -> Analysis:
    errors = validate_state(state)
    if errors:
        raise ValueError(" ".join(errors))

    material = MATERIALS[state.material]
    section = material.sections[state.section]
    total_load = 0.0
    total_moment = 0.0
    for load in state.loads:
        if load.kind == "point":
            total_load += load.magnitude
            total_moment += load.magnitude * load.position
        else:
            start, end = _uniform_extent(load, state.span)
            resultant = load.magnitude * max(0.0, end - start)
            total_load += resultant
            total_moment += resultant * (start + end) / 2

    if state.support == "cantilever":
        reactions = Reactions(total_load, 0.0, -total_moment)
    else:
        right = total_moment / state.span
        reactions = Reactions(total_load - right, right, 0.0)

    event_positions = [0.0, state.span]
    for load in state.loads:
        if load.kind == "point":
            event_positions.append(load.position)
        else:
            start, end = _uniform_extent(load, state.span)
            event_positions.extend((start, end))
    events = _unique_positions(event_positions)

    def shear_at(x: float, before: bool = False) -> float:
        return _sample_at(
            state,
            reactions,
            section,
            x,
            before_point_load=before,
        ).shear

    shear_candidates: list[Sample] = []
    for x in events:
        shear_candidates.append(
            _sample_at(state, reactions, section, x, before_point_load=True)
        )
        shear_candidates.append(_sample_at(state, reactions, section, x))
    shear_extrema = _extrema(shear_candidates, "shear")

    moment_positions = list(events)
    for left, right in zip(events, events[1:]):
        if right - left <= 1e-10:
            continue
        left_shear = shear_at(left)
        right_shear = shear_at(right, before=True)
        if abs(left_shear) <= 1e-10:
            moment_positions.append(left)
        if abs(right_shear) <= 1e-10:
            moment_positions.append(right)
        if left_shear * right_shear < 0:
            moment_positions.append(
                _bisect_zero(lambda x: shear_at(x), left, right)
            )
    moment_samples = [
        _sample_at(state, reactions, section, x)
        for x in _unique_positions(moment_positions)
    ]
    moment_extrema = _extrema(moment_samples, "moment")

    end_integral = _moment_integrals(state, reactions, state.span)[1]

    def deflection_slope(x: float) -> float:
        first_integral = _moment_integrals(state, reactions, x)[0]
        if state.support == "simply-supported":
            first_integral -= end_integral / state.span
        return first_integral

    slope_positions = [index * 0.1 for index in range(int(state.span * 10) + 1)]
    slope_positions.extend(events)
    slope_positions = _unique_positions(slope_positions)
    deflection_positions = [0.0, state.span]
    for left, right in zip(slope_positions, slope_positions[1:]):
        left_slope = deflection_slope(left)
        right_slope = deflection_slope(right)
        if abs(left_slope) <= 1e-10:
            deflection_positions.append(left)
        if abs(right_slope) <= 1e-10:
            deflection_positions.append(right)
        if left_slope * right_slope < 0:
            deflection_positions.append(
                _bisect_zero(deflection_slope, left, right)
            )
    deflection_samples = [
        _sample_at(state, reactions, section, x)
        for x in _unique_positions(deflection_positions)
    ]
    deflection_extrema = _extrema(deflection_samples, "deflection")

    plot_positions = [index * 0.05 for index in range(int(state.span * 20) + 1)]
    plot_positions.extend([state.span, *events, *moment_positions, *deflection_positions])
    plot_positions = _unique_positions(plot_positions)
    samples: list[Sample] = []
    shear_plot_samples: list[Sample] = []
    point_positions = {
        load.position
        for load in state.loads
        if load.kind == "point"
    }
    for x in plot_positions:
        sample = _sample_at(state, reactions, section, x)
        samples.append(sample)
        if any(isclose(x, point, abs_tol=1e-8) for point in point_positions):
            shear_plot_samples.append(
                _sample_at(state, reactions, section, x, before_point_load=True)
            )
        shear_plot_samples.append(sample)

    bending_stress = abs(moment_extrema.absolute.moment) * 12 / section.sx
    allowable_deflection = state.span * 12 / state.deflection_limit
    bending_utilization = bending_stress / material.allowable_stress
    deflection_utilization = (
        abs(deflection_extrema.absolute.deflection) / allowable_deflection
    )
    return Analysis(
        state=state,
        section=section,
        reactions=reactions,
        samples=tuple(samples),
        shear_plot_samples=tuple(shear_plot_samples),
        shear=shear_extrema,
        moment=moment_extrema,
        deflection=deflection_extrema,
        allowable_deflection=allowable_deflection,
        bending_stress=bending_stress,
        allowable_stress=material.allowable_stress,
        bending_utilization=bending_utilization,
        deflection_utilization=deflection_utilization,
    )


def recommend_section(analysis: Analysis) -> Recommendation:
    material = MATERIALS[analysis.state.material]
    candidates: list[tuple[str, Analysis, float]] = []
    for name in material.sections:
        candidate = analyze(replace(analysis.state, section=name))
        governing = max(
            candidate.bending_utilization,
            candidate.deflection_utilization,
        )
        candidates.append((name, candidate, governing))

    passing = [candidate for candidate in candidates if candidate[2] <= 1]
    if passing:
        if analysis.state.material == "steel":
            name, _, governing = min(
                passing,
                key=lambda candidate: (
                    candidate[1].section.weight
                    if candidate[1].section.weight is not None
                    else float("inf"),
                    -candidate[1].section.ix,
                ),
            )
        else:
            name, _, governing = passing[0]
        return Recommendation(name, True, governing)
    name, _, governing = min(candidates, key=lambda candidate: candidate[2])
    return Recommendation(name, False, governing)
