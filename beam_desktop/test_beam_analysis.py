import unittest
from typing import Literal

from beam_analysis import BeamLoad, BeamState, analyze, recommend_section, validate_state


class BeamAnalysisTests(unittest.TestCase):
    def make_state(
        self,
        *,
        support: Literal["simply-supported", "cantilever"] = "simply-supported",
        span: float = 20,
        loads: tuple[BeamLoad, ...] = (BeamLoad("uniform", 1, start=0, end=20),),
        material: str = "steel",
        section: str = "W12x26",
        deflection_limit: int = 360,
    ) -> BeamState:
        return BeamState(
            support=support,
            span=span,
            loads=loads,
            material=material,
            section=section,
            deflection_limit=deflection_limit,
        )

    def test_simply_supported_full_span_uniform_load(self) -> None:
        result = analyze(self.make_state())

        self.assertAlmostEqual(result.reactions.left, 10.0, places=8)
        self.assertAlmostEqual(result.reactions.right, 10.0, places=8)
        self.assertAlmostEqual(result.shear.absolute.shear, 10.0, places=8)
        self.assertEqual(result.shear.absolute_locations, (0.0, 20))
        self.assertAlmostEqual(result.moment.absolute.moment, 50.0, places=8)
        self.assertAlmostEqual(result.moment.absolute.x, 10.0, places=8)
        self.assertAlmostEqual(result.bending_stress, 17.9640718563, places=8)
        self.assertAlmostEqual(result.deflection.absolute.deflection, 0.609, delta=0.001)
        self.assertTrue(result.bending_utilization <= 1)
        self.assertTrue(result.deflection_utilization <= 1)

    def test_simply_supported_off_center_point_load(self) -> None:
        state = self.make_state(
            loads=(BeamLoad("point", 10, position=5),),
        )
        result = analyze(state)

        self.assertAlmostEqual(result.reactions.left, 7.5, places=8)
        self.assertAlmostEqual(result.reactions.right, 2.5, places=8)
        self.assertAlmostEqual(result.moment.absolute.moment, 37.5, places=8)
        self.assertAlmostEqual(result.moment.absolute.x, 5, places=8)
        self.assertAlmostEqual(result.bending_stress, 13.4730538922, places=8)
        self.assertAlmostEqual(result.deflection.absolute.deflection, 0.340, delta=0.002)
        self.assertAlmostEqual(result.deflection.absolute.x, 8.82, delta=0.03)
        self.assertAlmostEqual(result.value_at(5).shear, -2.5, places=8)

    def test_cantilever_free_end_point_load(self) -> None:
        result = analyze(
            self.make_state(
                support="cantilever",
                span=10,
                loads=(BeamLoad("point", 5, position=10),),
            )
        )

        self.assertAlmostEqual(result.reactions.left, 5.0, places=8)
        self.assertAlmostEqual(result.reactions.fixed_moment, -50.0, places=8)
        self.assertAlmostEqual(result.moment.absolute.moment, -50.0, places=8)
        self.assertAlmostEqual(result.bending_stress, 17.9640718563, places=8)
        self.assertAlmostEqual(result.deflection.absolute.deflection, 0.487, delta=0.002)
        self.assertAlmostEqual(result.deflection.absolute.x, 10.0, places=8)
        self.assertTrue(result.bending_utilization <= 1)
        self.assertTrue(result.deflection_utilization > 1)

    def test_lumber_joist_case(self) -> None:
        result = analyze(
            self.make_state(
                span=12,
                loads=(BeamLoad("uniform", 0.05, start=0, end=12),),
                material="lumber",
                section="2x10",
            )
        )

        self.assertAlmostEqual(result.reactions.left, 0.3, places=8)
        self.assertAlmostEqual(result.reactions.right, 0.3, places=8)
        self.assertAlmostEqual(result.moment.absolute.moment, 0.9, places=8)
        self.assertAlmostEqual(result.moment.absolute.x, 6, places=8)
        self.assertAlmostEqual(result.bending_stress, 0.5049088359, places=8)
        self.assertAlmostEqual(result.deflection.absolute.deflection, 0.147, delta=0.002)
        self.assertTrue(result.bending_utilization <= 1)
        self.assertTrue(result.deflection_utilization <= 1)

    def test_zero_load_has_zero_deflection_and_recommendation_is_valid(self) -> None:
        state = self.make_state(
            loads=(BeamLoad("uniform", 0, start=0, end=20),),
        )
        result = analyze(state)
        recommendation = recommend_section(result)

        self.assertEqual(result.deflection.absolute.deflection, 0)
        self.assertTrue(recommendation.passes)
        self.assertEqual(recommendation.section_name, "W8x10")

    def test_no_passing_section_returns_closest_option(self) -> None:
        result = analyze(
            self.make_state(loads=(BeamLoad("point", 100, position=10),))
        )
        recommendation = recommend_section(result)

        self.assertFalse(recommendation.passes)
        self.assertGreater(recommendation.governing_utilization, 1)

    def test_invalid_load_bounds_are_reported(self) -> None:
        state = self.make_state(
            loads=(BeamLoad("uniform", 1, start=8, end=4),),
        )

        self.assertTrue(any("start must be at or before" in error for error in validate_state(state)))
        with self.assertRaises(ValueError):
            analyze(state)


if __name__ == "__main__":
    unittest.main()
