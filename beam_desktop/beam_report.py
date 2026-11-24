"""Printable PDF calculation sheets for analyzed beams."""

from __future__ import annotations

from datetime import datetime
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.pdfgen.canvas import Canvas
from reportlab.platypus import Flowable, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

from beam_analysis import Analysis, Extrema, Sample, recommend_section


INK = colors.HexColor("#172033")
MUTED = colors.HexColor("#64748b")
BLUE = colors.HexColor("#2563eb")
GRID = colors.HexColor("#d9e2ef")
PALE_BLUE = colors.HexColor("#dbeafe")
GREEN = colors.HexColor("#15803d")
AMBER = colors.HexColor("#b45309")
RED = colors.HexColor("#b91c1c")


class BeamDiagramFlowable(Flowable):
    def __init__(self, analysis: Analysis, kind: str, title: str) -> None:
        super().__init__()
        self.analysis = analysis
        self.kind = kind
        self.title = title
        self.height = 1.28 * inch if kind == "beam" else 1.14 * inch

    def wrap(self, available_width: float, available_height: float) -> tuple[float, float]:
        _ = available_height
        self.width = available_width
        return available_width, self.height

    def draw(self) -> None:
        canvas = self.canv
        canvas.saveState()
        canvas.setFillColor(colors.white)
        canvas.setStrokeColor(GRID)
        canvas.roundRect(0, 0, self.width, self.height, 5, stroke=1, fill=1)
        canvas.setFillColor(INK)
        canvas.setFont("Helvetica-Bold", 8)
        canvas.drawString(9, self.height - 13, self.title)
        if self.kind == "beam":
            self._draw_beam()
        else:
            self._draw_curve()
        canvas.restoreState()

    def _x(self, position: float, left: float, right: float) -> float:
        return left + position / self.analysis.state.span * (right - left)

    def _draw_beam(self) -> None:
        canvas = self.canv
        analysis = self.analysis
        left, right = 42.0, self.width - 12.0
        base_y = self.height * 0.48
        max_deflection = max(abs(sample.deflection) for sample in analysis.samples)
        deflection_scale = 21 / max_deflection if max_deflection > 1e-12 else 0.0
        max_moment = max(abs(sample.moment) for sample in analysis.samples)

        def beam_y(sample: Sample) -> float:
            return base_y - sample.deflection * deflection_scale

        for start, end in zip(analysis.samples, analysis.samples[1:]):
            ratio = (
                (abs(start.moment) + abs(end.moment)) / (2 * max_moment)
                if max_moment > 1e-12
                else 0.0
            )
            canvas.setStrokeColor(_stress_color(ratio))
            canvas.setLineWidth(5)
            canvas.line(
                self._x(start.x, left, right),
                beam_y(start),
                self._x(end.x, left, right),
                beam_y(end),
            )

        left_y, right_y = beam_y(analysis.value_at(0)), beam_y(
            analysis.value_at(analysis.state.span)
        )
        canvas.setStrokeColor(BLUE)
        canvas.setFillColor(PALE_BLUE)
        if analysis.state.support == "cantilever":
            canvas.setLineWidth(3)
            canvas.line(left - 4, left_y - 15, left - 4, left_y + 15)
            for offset in range(-12, 14, 6):
                canvas.line(left - 8, left_y + offset, left - 4, left_y + offset - 4)
        else:
            for x, y in ((left, left_y), (right, right_y)):
                path = canvas.beginPath()
                path.moveTo(x, y - 2)
                path.lineTo(x - 7, y - 12)
                path.lineTo(x + 7, y - 12)
                path.close()
                canvas.drawPath(path, stroke=1, fill=1)

        canvas.setStrokeColor(BLUE)
        canvas.setFillColor(INK)
        canvas.setLineWidth(0.8)
        canvas.setFont("Helvetica", 6)
        for load in analysis.state.loads:
            if load.kind == "point":
                x = self._x(load.position, left, right)
                y = beam_y(analysis.value_at(load.position))
                canvas.line(x, y + 22, x, y + 6)
                _draw_down_arrow(canvas, x, y + 6)
                canvas.drawCentredString(
                    x, y + 24, f"{load.magnitude:g} k @ {load.position:g} ft"
                )
            else:
                start = max(0.0, load.start)
                end = min(analysis.state.span, load.end)
                if end > start:
                    count = max(3, min(9, int((end - start) / max(1, analysis.state.span / 7)) + 1))
                    for index in range(count):
                        position = start + (end - start) * index / (count - 1)
                        x = self._x(position, left, right)
                        y = beam_y(analysis.value_at(position))
                        canvas.line(x, y + 17, x, y + 5)
                        _draw_down_arrow(canvas, x, y + 5)
                    canvas.drawCentredString(
                        (self._x(start, left, right) + self._x(end, left, right)) / 2,
                        self.height - 25,
                        f"{load.magnitude:g} kip/ft, {start:g}-{end:g} ft",
                    )

        canvas.setStrokeColor(GREEN)
        canvas.setFillColor(INK)
        canvas.setFont("Helvetica", 6)
        if analysis.state.support == "cantilever":
            canvas.drawString(
                left,
                7,
                f"Ay {analysis.reactions.left:.2f} k up   "
                f"MA {abs(analysis.reactions.fixed_moment):.2f} kip-ft",
            )
        else:
            canvas.drawString(
                left,
                7,
                f"RA {analysis.reactions.left:.2f} k up   "
                f"RB {analysis.reactions.right:.2f} k up",
            )
        canvas.drawRightString(right, 7, f"0 - {analysis.state.span:g} ft")

    def _draw_curve(self) -> None:
        canvas = self.canv
        analysis = self.analysis
        field = {
            "shear": "shear",
            "moment": "moment",
            "deflection": "deflection",
        }[self.kind]
        units = {"shear": "kips", "moment": "kip-ft", "deflection": "in"}[self.kind]
        samples = (
            analysis.shear_plot_samples
            if self.kind == "shear"
            else analysis.samples
        )
        values = [getattr(sample, field) for sample in samples]
        amplitude = max([0.0, *values], default=0.0)
        amplitude = max(amplitude, abs(min([0.0, *values], default=0.0)), 1e-12)
        left, right = 42.0, self.width - 12.0
        baseline = self.height * 0.42
        graph_height = self.height * 0.46
        scale = graph_height / amplitude
        self._draw_extrema(field, units, right)
        canvas.setStrokeColor(MUTED)
        canvas.setLineWidth(0.45)
        canvas.line(left, baseline, right, baseline)

        points = [
            (
                self._x(sample.x, left, right),
                baseline
                + (-1 if self.kind == "deflection" else 1)
                * getattr(sample, field)
                * scale,
            )
            for sample in samples
        ]
        if not points:
            return
        area = canvas.beginPath()
        area.moveTo(points[0][0], baseline)
        for x, y in points:
            area.lineTo(x, y)
        area.lineTo(points[-1][0], baseline)
        area.close()
        canvas.setFillColor(PALE_BLUE)
        canvas.drawPath(area, stroke=0, fill=1)
        curve = canvas.beginPath()
        curve.moveTo(*points[0])
        for point in points[1:]:
            curve.lineTo(*point)
        canvas.setStrokeColor(BLUE)
        canvas.setLineWidth(1.2)
        canvas.drawPath(curve, stroke=1, fill=0)
        canvas.setFillColor(MUTED)
        canvas.setFont("Helvetica", 5.5)
        canvas.drawString(left, 5, "0 ft")
        canvas.drawRightString(right, 5, f"{analysis.state.span:g} ft")
        if self.kind == "deflection":
            canvas.drawRightString(
                right, 12, "Downward positive; vertical scale exaggerated"
            )

    def _draw_extrema(
        self, field: str, units: str, right: float
    ) -> None:
        extrema: Extrema = getattr(self.analysis, self.kind)
        max_value = getattr(extrema.maximum, field)
        min_value = getattr(extrema.minimum, field)
        max_abs = abs(getattr(extrema.absolute, field))
        canvas = self.canv
        canvas.setFillColor(MUTED)
        canvas.setFont("Helvetica", 5.8)
        canvas.drawRightString(
            right,
            self.height - 13,
            f"max {max_value:.3g} @ {extrema.maximum.x:.2f} ft | "
            f"min {min_value:.3g} @ {extrema.minimum.x:.2f} ft | "
            f"max abs {max_abs:.3g} {units}",
        )


def create_calculation_sheet(path: str | Path, analysis: Analysis) -> None:
    output = Path(path)
    document = SimpleDocTemplate(
        str(output),
        pagesize=letter,
        leftMargin=0.55 * inch,
        rightMargin=0.55 * inch,
        topMargin=0.45 * inch,
        bottomMargin=0.45 * inch,
        title="Beam Designer Calculation Sheet",
        author="Beam Designer",
    )
    styles = getSampleStyleSheet()
    styles.add(
        ParagraphStyle(
            name="BeamSheetTitle",
            parent=styles["Title"],
            fontName="Helvetica-Bold",
            fontSize=17,
            leading=20,
            textColor=INK,
            alignment=TA_CENTER,
            spaceAfter=2,
        )
    )
    styles.add(
        ParagraphStyle(
            name="BeamSection",
            parent=styles["Heading2"],
            fontName="Helvetica-Bold",
            fontSize=9,
            leading=11,
            textColor=INK,
            spaceBefore=5,
            spaceAfter=3,
        )
    )
    styles.add(
        ParagraphStyle(
            name="BeamSmall",
            parent=styles["BodyText"],
            fontName="Helvetica",
            fontSize=7,
            leading=9,
            textColor=MUTED,
            spaceAfter=3,
        )
    )

    state = analysis.state
    material_name = (
        "Steel"
        if state.material == "steel"
        else "Douglas Fir-Larch No. 2 lumber"
    )
    story: list[Flowable] = [
        Paragraph("Beam Calculation Sheet", styles["BeamSheetTitle"]),
        Paragraph(
            f"Generated {datetime.now().astimezone().strftime('%Y-%m-%d %H:%M %Z')}",
            styles["BeamSmall"],
        ),
        Paragraph("Design inputs", styles["BeamSection"]),
    ]
    inputs = Table(
        [
            ["Span", "Support", "Material", "Section", "Deflection limit"],
            [
                f"{state.span:g} ft",
                "Cantilever" if state.support == "cantilever" else "Simply supported",
                material_name,
                state.section,
                f"L/{state.deflection_limit}",
            ],
        ],
        colWidths=[0.78 * inch, 1.25 * inch, 1.8 * inch, 1.0 * inch, 1.1 * inch],
    )
    inputs.setStyle(_table_style())
    story.append(inputs)
    story.append(Spacer(1, 4))

    load_rows: list[list[str]] = [
        ["#", "Load type", "Magnitude", "Position / start", "End"]
    ]
    for index, load in enumerate(state.loads, start=1):
        if load.kind == "point":
            load_rows.append(
                [
                    str(index),
                    "Point",
                    f"{load.magnitude:g} kips",
                    f"{load.position:g} ft",
                    "-",
                ]
            )
        else:
            load_rows.append(
                [
                    str(index),
                    "Uniform",
                    f"{load.magnitude:g} kips/ft",
                    f"{load.start:g} ft",
                    f"{load.end:g} ft",
                ]
            )
    loads = Table(
        load_rows,
        colWidths=[0.35 * inch, 1.0 * inch, 1.2 * inch, 1.55 * inch, 1.35 * inch],
        repeatRows=1,
        hAlign="LEFT",
    )
    loads.setStyle(_table_style())
    story.extend(
        (
            Paragraph("Applied loads", styles["BeamSection"]),
            loads,
            Paragraph("Reactions and design checks", styles["BeamSection"]),
        )
    )

    recommendation = recommend_section(analysis)
    recommendation_text = (
        f"{recommendation.section_name} is the lightest passing section."
        if recommendation.passes
        else (
            f"No section passes. Closest option: {recommendation.section_name} "
            f"({recommendation.governing_utilization * 100:.1f}% governing utilization)."
        )
    )
    check_rows = [
        ["Check", "Actual", "Allowable", "Utilization", "Result"],
        [
            "Bending",
            f"{analysis.bending_stress:.2f} ksi",
            f"{analysis.allowable_stress:.2f} ksi",
            f"{analysis.bending_utilization * 100:.2f}%",
            "PASS" if analysis.bending_utilization <= 1 else "FAIL",
        ],
        [
            "Deflection",
            f"{abs(analysis.deflection.absolute.deflection):.3f} in",
            f"{analysis.allowable_deflection:.3f} in",
            f"{analysis.deflection_utilization * 100:.2f}%",
            "PASS" if analysis.deflection_utilization <= 1 else "FAIL",
        ],
    ]
    checks = Table(
        check_rows,
        colWidths=[1.0 * inch, 1.15 * inch, 1.2 * inch, 1.2 * inch, 0.9 * inch],
        hAlign="LEFT",
    )
    checks.setStyle(_table_style())
    story.extend(
        (
            checks,
            Spacer(1, 4),
            Paragraph(recommendation_text, styles["BeamSmall"]),
            Paragraph("Analysis diagrams", styles["BeamSection"]),
            BeamDiagramFlowable(analysis, "beam", "Beam, supports, and loads"),
            Spacer(1, 5),
            BeamDiagramFlowable(analysis, "shear", "Shear diagram, V (kips)"),
            Spacer(1, 5),
            BeamDiagramFlowable(analysis, "moment", "Moment diagram, M (kip-ft)"),
            Spacer(1, 5),
            BeamDiagramFlowable(analysis, "deflection", "Deflected shape, y (in)"),
        )
    )
    document.build(story, onFirstPage=_draw_page_number, onLaterPages=_draw_page_number)


def _draw_page_number(canvas: Canvas, document: SimpleDocTemplate) -> None:
    canvas.saveState()
    canvas.setStrokeColor(GRID)
    canvas.line(
        document.leftMargin,
        0.32 * inch,
        letter[0] - document.rightMargin,
        0.32 * inch,
    )
    canvas.setFillColor(MUTED)
    canvas.setFont("Helvetica", 7)
    canvas.drawRightString(
        letter[0] - document.rightMargin,
        0.18 * inch,
        f"Beam Designer | Page {document.page}",
    )
    canvas.restoreState()


def _table_style() -> TableStyle:
    return TableStyle(
        [
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#eaf1f8")),
            ("TEXTCOLOR", (0, 0), (-1, 0), INK),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
            ("FONTSIZE", (0, 0), (-1, -1), 7),
            ("TEXTCOLOR", (0, 1), (-1, -1), INK),
            ("GRID", (0, 0), (-1, -1), 0.4, GRID),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("LEFTPADDING", (0, 0), (-1, -1), 5),
            ("RIGHTPADDING", (0, 0), (-1, -1), 5),
            ("TOPPADDING", (0, 0), (-1, -1), 3),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
        ]
    )


def _draw_down_arrow(canvas: Canvas, x: float, y: float) -> None:
    canvas.line(x, y + 3, x, y)
    path = canvas.beginPath()
    path.moveTo(x, y)
    path.lineTo(x - 2.2, y + 3.5)
    path.lineTo(x + 2.2, y + 3.5)
    path.close()
    canvas.drawPath(path, stroke=0, fill=1)


def _stress_color(ratio: float) -> colors.Color:
    position = min(1.0, max(0.0, ratio))
    stops = ((0.0, (22, 163, 74)), (0.5, (245, 158, 11)), (1.0, (220, 38, 38)))
    for (start, color_a), (end, color_b) in zip(stops, stops[1:]):
        if position <= end:
            fraction = (position - start) / (end - start)
            return colors.Color(
                *(
                    (a + (b - a) * fraction) / 255
                    for a, b in zip(color_a, color_b)
                )
            )
    return RED
