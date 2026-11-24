"""Tkinter desktop application for beam analysis and preliminary design."""

from __future__ import annotations

import tkinter as tk
from math import isfinite
from pathlib import Path
from tkinter import filedialog, messagebox, ttk
from typing import Literal

from beam_analysis import (
    MATERIALS,
    Analysis,
    BeamLoad,
    BeamState,
    Extrema,
    Sample,
    analyze,
    recommend_section,
    validate_state,
)
from beam_files import read_beam_file, write_beam_file, write_results_csv
from beam_report import create_calculation_sheet


BACKGROUND = "#f1f5f9"
CARD = "#ffffff"
INK = "#172033"
MUTED = "#64748b"
BLUE = "#2563eb"
GREEN = "#15803d"
AMBER = "#b45309"
RED = "#b91c1c"


class LoadRow:
    def __init__(
        self,
        kind: str,
        frame: ttk.LabelFrame,
        variables: dict[str, tk.StringVar],
        spins: list[ttk.Spinbox],
    ) -> None:
        self.kind = kind
        self.frame = frame
        self.variables = variables
        self.spins = spins
        self.trace_tokens: list[tuple[tk.Variable, str]] = []


class Tooltip:
    def __init__(self, widget: tk.Widget, text: str) -> None:
        self.widget = widget
        self.text = text
        self.window: tk.Toplevel | None = None
        self.pending: str | None = None
        self._bind_tree(widget)

    def _bind_tree(self, widget: tk.Widget) -> None:
        widget.bind("<Enter>", self._show, add="+")
        widget.bind("<Leave>", self._schedule_hide, add="+")
        for child in widget.winfo_children():
            self._bind_tree(child)

    def _show(self, event: tk.Event) -> None:
        if self.pending is not None:
            self.widget.after_cancel(self.pending)
            self.pending = None
        if self.window is not None:
            return
        self.window = tk.Toplevel(self.widget)
        self.window.wm_overrideredirect(True)
        self.window.wm_geometry(f"+{event.x_root + 12}+{event.y_root + 12}")
        ttk.Label(
            self.window,
            text=self.text,
            padding=(8, 5),
            background="#fffbe6",
            relief="solid",
            borderwidth=1,
        ).pack()

    def _schedule_hide(self, event: tk.Event) -> None:
        _ = event
        if self.pending is not None:
            self.widget.after_cancel(self.pending)
        self.pending = self.widget.after(120, self._hide)

    def _hide(self) -> None:
        self.pending = None
        if self.window is not None:
            self.window.destroy()
            self.window = None


class BeamDesigner:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("Beam Designer")
        self.root.geometry("1480x960")
        self.root.minsize(1200, 720)
        self.root.configure(background=BACKGROUND)

        self.style = ttk.Style(root)
        self.style.configure("App.TFrame", background=BACKGROUND)
        self.style.configure("Card.TFrame", background=CARD)
        self.style.configure("Title.TLabel", font=("Segoe UI", 19, "bold"), foreground=INK)
        self.style.configure("Subtitle.TLabel", font=("Segoe UI", 9), foreground=MUTED)
        self.style.configure("Section.TLabel", font=("Segoe UI", 10, "bold"), foreground=INK)
        self.style.configure("Value.TLabel", font=("Segoe UI", 16, "bold"), foreground=INK)
        self.style.configure("Status.TLabel", font=("Segoe UI", 9, "bold"))
        self.style.configure("Green.Horizontal.TProgressbar", background=GREEN)
        self.style.configure("Amber.Horizontal.TProgressbar", background="#d97706")
        self.style.configure("Red.Horizontal.TProgressbar", background=RED)

        self.support_var = tk.StringVar(root, "simply-supported")
        self.span_var = tk.StringVar(root, "20")
        self.span_scale_var = tk.DoubleVar(root, 20)
        self.material_var = tk.StringVar(root, "steel")
        self.material_display_var = tk.StringVar(root, "Steel")
        self.section_var = tk.StringVar(root, "W12x26")
        self.deflection_limit_var = tk.IntVar(root, 360)
        self.status_var = tk.StringVar(root, "Example loaded")
        self.current_project_path: Path | None = None

        self.load_rows: list[LoadRow] = []
        self._trace_tokens: list[tuple[tk.Variable, str]] = []
        self._syncing = False
        self._has_changed = False
        self.current_analysis: Analysis | None = None
        self.pointer_x = 10.0
        self.pointer_visible = False
        self.dragging_load: int | None = None
        self._beam_plot: tuple[float, float, float, float] | None = None

        self._build_layout()
        self._add_load("uniform", {"magnitude": "1", "start": "0", "end": "20"})
        self._install_traces()
        self._on_span_changed()

    def _build_layout(self) -> None:
        self.root.columnconfigure(0, weight=0)
        self.root.columnconfigure(1, weight=1)
        self.root.rowconfigure(1, weight=1)
        self._build_file_menu()

        header = ttk.Frame(self.root, style="App.TFrame", padding=(18, 12))
        header.grid(row=0, column=0, columnspan=2, sticky="ew")
        header.columnconfigure(0, weight=1)
        ttk.Label(header, text="Beam Designer", style="Title.TLabel").grid(
            row=0, column=0, sticky="w"
        )
        ttk.Label(
            header,
            text="Reactions, diagrams, deflection, and preliminary section checks",
            style="Subtitle.TLabel",
        ).grid(row=1, column=0, sticky="w", pady=(2, 0))
        self.status_label = ttk.Label(
            header, textvariable=self.status_var, style="Status.TLabel"
        )
        self.status_label.grid(row=0, column=1, sticky="e", padx=(12, 4))
        file_buttons = ttk.Frame(header)
        file_buttons.grid(row=1, column=1, sticky="e", padx=(10, 0), pady=(4, 0))
        ttk.Button(file_buttons, text="Open", command=self._open_beam).grid(row=0, column=0)
        ttk.Button(file_buttons, text="Save", command=self._save_beam).grid(
            row=0, column=1, padx=(4, 0)
        )
        ttk.Button(file_buttons, text="Export CSV", command=self._export_results_csv).grid(
            row=0, column=2, padx=(4, 0)
        )
        ttk.Button(file_buttons, text="Calculation PDF", command=self._export_calculation_sheet).grid(
            row=0, column=3, padx=(4, 0)
        )

        self.sidebar = ttk.Frame(self.root, width=395, style="App.TFrame")
        self.sidebar.grid(row=1, column=0, sticky="nsew")
        self.sidebar.grid_propagate(False)
        self.sidebar.columnconfigure(0, weight=1)
        self.sidebar.rowconfigure(0, weight=1)

        self.sidebar_canvas = tk.Canvas(
            self.sidebar,
            width=378,
            background=BACKGROUND,
            highlightthickness=0,
            borderwidth=0,
        )
        self.sidebar_scrollbar = ttk.Scrollbar(
            self.sidebar, orient="vertical", command=self.sidebar_canvas.yview
        )
        self.sidebar_canvas.configure(yscrollcommand=self.sidebar_scrollbar.set)
        self.sidebar_canvas.grid(row=0, column=0, sticky="nsew")
        self.sidebar_scrollbar.grid(row=0, column=1, sticky="ns")
        self.sidebar_content = ttk.Frame(
            self.sidebar_canvas, style="App.TFrame", padding=(12, 4, 10, 14)
        )
        self.sidebar_window = self.sidebar_canvas.create_window(
            (0, 0), window=self.sidebar_content, anchor="nw"
        )
        self.sidebar_content.bind("<Configure>", self._resize_sidebar_scroll)
        self.sidebar_canvas.bind("<Configure>", self._resize_sidebar_content)

        self._build_inputs()
        self._build_results()

        plot_frame = ttk.Frame(self.root, style="App.TFrame", padding=(0, 0, 14, 14))
        plot_frame.grid(row=1, column=1, sticky="nsew")
        plot_frame.columnconfigure(0, weight=1)
        plot_frame.rowconfigure(1, weight=1)
        self.pointer_readout_var = tk.StringVar(self.root, "")
        self.pointer_readout = ttk.Label(
            plot_frame,
            textvariable=self.pointer_readout_var,
            anchor="e",
            padding=(8, 5),
            foreground=INK,
            font=("Segoe UI", 9, "bold"),
        )
        self.pointer_readout.grid(row=0, column=0, sticky="ew")
        self.pointer_readout.grid_remove()
        self.plot_canvas = tk.Canvas(
            plot_frame,
            background=CARD,
            highlightthickness=1,
            highlightbackground="#d9e2ef",
            borderwidth=0,
        )
        plot_scrollbar = ttk.Scrollbar(
            plot_frame, orient="vertical", command=self.plot_canvas.yview
        )
        self.plot_canvas.configure(yscrollcommand=plot_scrollbar.set)
        self.plot_canvas.grid(row=1, column=0, sticky="nsew")
        plot_scrollbar.grid(row=1, column=1, sticky="ns")
        self.plot_canvas.bind("<Configure>", self._on_plot_resize)
        self.plot_canvas.bind("<Motion>", self._on_plot_motion)
        self.plot_canvas.bind("<Leave>", self._on_plot_leave)
        self.plot_canvas.bind("<ButtonPress-1>", self._on_plot_press)
        self.plot_canvas.bind("<B1-Motion>", self._on_plot_drag)
        self.plot_canvas.bind("<ButtonRelease-1>", self._on_plot_release)

    def _build_file_menu(self) -> None:
        menu_bar = tk.Menu(self.root)
        file_menu = tk.Menu(menu_bar, tearoff=False)
        file_menu.add_command(label="Open...", command=self._open_beam)
        file_menu.add_command(label="Save", command=self._save_beam)
        file_menu.add_command(label="Save As...", command=lambda: self._save_beam(save_as=True))
        file_menu.add_separator()
        file_menu.add_command(label="Export Results as CSV...", command=self._export_results_csv)
        file_menu.add_command(label="Export Calculation Sheet as PDF...", command=self._export_calculation_sheet)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.destroy)
        menu_bar.add_cascade(label="File", menu=file_menu)
        self.root.configure(menu=menu_bar)

    def _resize_sidebar_scroll(self, event: tk.Event) -> None:
        self.sidebar_canvas.configure(scrollregion=(0, 0, event.width, event.height))

    def _resize_sidebar_content(self, event: tk.Event) -> None:
        self.sidebar_canvas.itemconfigure(self.sidebar_window, width=event.width)

    def _build_inputs(self) -> None:
        panel = ttk.LabelFrame(self.sidebar_content, text="Beam and loads", padding=10)
        panel.grid(row=0, column=0, sticky="ew", pady=(0, 10))
        panel.columnconfigure(0, weight=1)

        self.validation_message = ttk.Label(
            panel,
            text="",
            foreground=RED,
            wraplength=330,
            justify="left",
        )
        self.validation_message.grid(row=0, column=0, sticky="ew", pady=(0, 8))
        self.validation_message.grid_remove()

        support = ttk.Frame(panel)
        support.grid(row=1, column=0, sticky="ew", pady=(0, 8))
        ttk.Label(support, text="Support type").grid(row=0, column=0, sticky="w")
        support_options = ttk.Frame(support)
        support_options.grid(row=1, column=0, sticky="w", pady=(3, 0))
        ttk.Radiobutton(
            support_options,
            text="Simply supported",
            value="simply-supported",
            variable=self.support_var,
        ).grid(row=0, column=0, sticky="w")
        ttk.Radiobutton(
            support_options,
            text="Cantilever",
            value="cantilever",
            variable=self.support_var,
        ).grid(row=0, column=1, sticky="w", padx=(12, 0))

        span_frame = ttk.Frame(panel)
        span_frame.grid(row=2, column=0, sticky="ew", pady=(0, 8))
        span_frame.columnconfigure(0, weight=1)
        ttk.Label(span_frame, text="Span (ft)").grid(row=0, column=0, sticky="w")
        self.span_spin = ttk.Spinbox(
            span_frame,
            from_=4,
            to=40,
            increment=0.25,
            textvariable=self.span_var,
            width=9,
            justify="right",
        )
        self.span_spin.grid(row=0, column=1, sticky="e")
        ttk.Scale(
            span_frame,
            from_=4,
            to=40,
            variable=self.span_scale_var,
            command=self._on_span_scale,
        ).grid(row=1, column=0, columnspan=2, sticky="ew", pady=(3, 0))

        load_title = ttk.Label(panel, text="Loads (downward positive)", style="Section.TLabel")
        load_title.grid(row=3, column=0, sticky="w", pady=(4, 5))
        self.load_list_frame = ttk.Frame(panel)
        self.load_list_frame.grid(row=4, column=0, sticky="ew")
        self.load_list_frame.columnconfigure(0, weight=1)
        load_buttons = ttk.Frame(panel)
        load_buttons.grid(row=5, column=0, sticky="ew", pady=(7, 0))
        ttk.Button(
            load_buttons, text="+ Point load", command=self._add_point_load
        ).grid(row=0, column=0, sticky="ew")
        ttk.Button(
            load_buttons, text="+ Uniform load", command=self._add_uniform_load
        ).grid(row=0, column=1, sticky="ew", padx=(6, 0))
        load_buttons.columnconfigure(0, weight=1)
        load_buttons.columnconfigure(1, weight=1)

        material_frame = ttk.LabelFrame(
            self.sidebar_content, text="Material and section", padding=10
        )
        material_frame.grid(row=1, column=0, sticky="ew", pady=(0, 10))
        material_frame.columnconfigure(1, weight=1)
        ttk.Label(material_frame, text="Material").grid(row=0, column=0, sticky="w")
        self.material_combo = ttk.Combobox(
            material_frame,
            textvariable=self.material_display_var,
            values=("Steel", "Douglas Fir-Larch No. 2 lumber"),
            state="readonly",
            width=23,
        )
        self.material_combo.grid(row=0, column=1, sticky="ew", padx=(8, 0))
        self.material_combo.bind("<<ComboboxSelected>>", self._on_material_changed)
        ttk.Label(material_frame, text="Section").grid(
            row=1, column=0, sticky="w", pady=(8, 0)
        )
        self.section_combo = ttk.Combobox(
            material_frame,
            textvariable=self.section_var,
            state="readonly",
            width=23,
        )
        self.section_combo.grid(row=1, column=1, sticky="ew", padx=(8, 0), pady=(8, 0))
        self.section_info = ttk.Label(
            material_frame, foreground=MUTED, wraplength=310, justify="left"
        )
        self.section_info.grid(row=2, column=0, columnspan=2, sticky="w", pady=(8, 0))
        self._refresh_section_choices()

        limit_frame = ttk.LabelFrame(
            self.sidebar_content, text="Deflection limit", padding=10
        )
        limit_frame.grid(row=2, column=0, sticky="ew", pady=(0, 10))
        ttk.Radiobutton(
            limit_frame, text="L/240", value=240, variable=self.deflection_limit_var
        ).grid(row=0, column=0, sticky="w")
        ttk.Radiobutton(
            limit_frame, text="L/360", value=360, variable=self.deflection_limit_var
        ).grid(row=0, column=1, sticky="w", padx=(14, 0))

    def _build_results(self) -> None:
        self.results_frame = ttk.Frame(self.sidebar_content)
        self.results_frame.grid(row=3, column=0, sticky="ew")
        self.results_frame.columnconfigure(0, weight=1)

        self.bending_card, self.bending_labels = self._build_check_card(
            self.results_frame, 0, "Bending check"
        )
        self.deflection_card, self.deflection_labels = self._build_check_card(
            self.results_frame, 1, "Deflection check"
        )
        Tooltip(self.bending_card, "fb = |M|max × 12 / Sx")
        self.deflection_tooltip = Tooltip(
            self.deflection_card,
            "Deflection utilization = maximum absolute deflection / allowable deflection.",
        )

        self.recommendation_frame = ttk.LabelFrame(
            self.results_frame, text="Section recommendation", padding=10
        )
        self.recommendation_frame.grid(row=2, column=0, sticky="ew", pady=(0, 8))
        self.recommendation_text = ttk.Label(
            self.recommendation_frame, wraplength=320, justify="left"
        )
        self.recommendation_text.grid(row=0, column=0, sticky="ew")
        self.recommendation_button = ttk.Button(
            self.recommendation_frame, text="Use section", command=self._apply_recommendation
        )
        self.recommendation_button.grid(row=1, column=0, sticky="ew", pady=(8, 0))

    def _build_check_card(
        self, parent: ttk.Frame, row: int, title: str
    ) -> tuple[ttk.LabelFrame, dict[str, ttk.Widget]]:
        card = ttk.LabelFrame(parent, text=title, padding=10)
        card.grid(row=row, column=0, sticky="ew", pady=(0, 8))
        card.columnconfigure(0, weight=1)
        value = ttk.Label(card, text="—", style="Value.TLabel")
        value.grid(row=0, column=0, sticky="w")
        allowable = ttk.Label(card, text="Allowable: —", foreground=MUTED)
        allowable.grid(row=1, column=0, sticky="w", pady=(2, 5))
        bar = ttk.Progressbar(card, maximum=100, mode="determinate")
        bar.grid(row=2, column=0, sticky="ew", pady=(0, 4))
        utilization = ttk.Label(card, text="Utilization: —", foreground=MUTED)
        utilization.grid(row=3, column=0, sticky="w")
        status = ttk.Label(card, text="PASS", style="Status.TLabel")
        status.grid(row=3, column=1, sticky="e")
        return card, {
            "value": value,
            "allowable": allowable,
            "bar": bar,
            "utilization": utilization,
            "status": status,
        }

    def _install_traces(self) -> None:
        variables: list[tk.Variable] = [
            self.support_var,
            self.material_var,
            self.section_var,
            self.deflection_limit_var,
        ]
        for variable in variables:
            token = variable.trace_add("write", self._on_input_changed)
            self._trace_tokens.append((variable, token))
        self.span_var.trace_add("write", self._on_span_changed)
        for row in self.load_rows:
            self._watch_load_row(row)

    def _watch_load_row(self, row: LoadRow) -> None:
        for variable in row.variables.values():
            token = variable.trace_add("write", self._on_input_changed)
            row.trace_tokens.append((variable, token))

    def _add_load(
        self, kind: str, values: dict[str, str], *, refresh: bool = True
    ) -> None:
        index = len(self.load_rows) + 1
        title = "Point load" if kind == "point" else "Uniform load"
        frame = ttk.LabelFrame(self.load_list_frame, text=f"{title} {index}", padding=7)
        frame.grid(row=index - 1, column=0, sticky="ew", pady=(0, 6))
        frame.columnconfigure(0, weight=1)
        ttk.Button(
            frame,
            text="Remove",
            width=7,
            command=lambda target=frame: self._remove_load(target),
        ).grid(row=0, column=1, sticky="e")

        variables = {name: tk.StringVar(self.root, value) for name, value in values.items()}
        fields = ttk.Frame(frame)
        fields.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(4, 0))
        for column in range(len(values)):
            fields.columnconfigure(column, weight=1)
        labels = (
            {"magnitude": ("Magnitude", "kips"), "position": ("Position", "ft")}
            if kind == "point"
            else {
                "magnitude": ("Magnitude", "kip/ft"),
                "start": ("Start", "ft"),
                "end": ("End", "ft"),
            }
        )
        spins: list[ttk.Spinbox] = []
        for column, (name, variable) in enumerate(variables.items()):
            label, unit = labels[name]
            field = ttk.Frame(fields)
            field.grid(row=0, column=column, sticky="ew", padx=(0, 5))
            ttk.Label(field, text=f"{label} ({unit})").grid(row=0, column=0, sticky="w")
            maximum = 100 if kind == "point" and name == "magnitude" else (
                10 if kind == "uniform" and name == "magnitude" else self._current_span()
            )
            step = 0.1 if name == "magnitude" else 0.25
            spin = ttk.Spinbox(
                field,
                from_=0,
                to=maximum,
                increment=step,
                textvariable=variable,
                width=10,
            )
            spin.grid(row=1, column=0, sticky="ew")
            field.columnconfigure(0, weight=1)
            spins.append(spin)

        row = LoadRow(kind, frame, variables, spins)
        self.load_rows.append(row)
        if hasattr(self, "_trace_tokens"):
            self._watch_load_row(row)
        if self._trace_tokens:
            self._has_changed = True
        if refresh and hasattr(self, "current_analysis"):
            self._refresh()

    def _remove_load(self, frame: ttk.LabelFrame) -> None:
        for row in tuple(self.load_rows):
            if row.frame is frame:
                for variable, token in row.trace_tokens:
                    variable.trace_remove("write", token)
                self.load_rows.remove(row)
                row.frame.destroy()
                break
        for index, row in enumerate(self.load_rows, start=1):
            row.frame.configure(text=f"{'Point load' if row.kind == 'point' else 'Uniform load'} {index}")
            row.frame.grid_configure(row=index - 1)
        self._has_changed = True
        self._refresh()

    def _add_point_load(self) -> None:
        span = self._current_span()
        position = span if self.support_var.get() == "cantilever" else span / 2
        self._add_load(
            "point",
            {"magnitude": "10", "position": f"{position:.2f}"},
        )

    def _add_uniform_load(self) -> None:
        self._add_load(
            "uniform",
            {"magnitude": "1", "start": "0", "end": f"{self._current_span():.2f}"},
        )

    def _save_beam(self, *, save_as: bool = False) -> None:
        state, errors = self._read_state()
        if state is None:
            messagebox.showerror(
                "Cannot save beam",
                "Correct the following inputs before saving:\n\n" + "\n".join(errors),
                parent=self.root,
            )
            return

        path = self.current_project_path
        if path is None or save_as:
            selected = filedialog.asksaveasfilename(
                parent=self.root,
                title="Save Beam",
                defaultextension=".beam.json",
                initialfile=path.name if path is not None else "beam.beam.json",
                filetypes=(
                    ("Beam Designer projects", "*.beam.json"),
                    ("JSON files", "*.json"),
                ),
            )
            if not selected:
                return
            path = Path(selected)

        try:
            write_beam_file(path, state)
        except (OSError, ValueError) as error:
            messagebox.showerror(
                "Could not save beam",
                f"The beam file could not be saved:\n{error}",
                parent=self.root,
            )
            return

        self.current_project_path = path
        self._update_window_title()
        self.status_var.set(f"Saved {path.name}")

    def _open_beam(self) -> None:
        selected = filedialog.askopenfilename(
            parent=self.root,
            title="Open Beam",
            filetypes=(
                ("Beam Designer projects", "*.beam.json"),
                ("JSON files", "*.json"),
            ),
        )
        if not selected:
            return
        path = Path(selected)
        try:
            state = read_beam_file(path)
        except (OSError, ValueError) as error:
            messagebox.showerror(
                "Could not open beam",
                f"The selected file was not loaded:\n{error}",
                parent=self.root,
            )
            return

        self._load_project_state(state)
        self.current_project_path = path
        self._update_window_title()
        self.status_var.set(f"Opened {path.name}")

    def _load_project_state(self, state: BeamState) -> None:
        self._syncing = True
        self.support_var.set(state.support)
        self.span_var.set(repr(state.span))
        self.span_scale_var.set(state.span)
        self.material_var.set(state.material)
        self.material_display_var.set(
            "Steel" if state.material == "steel" else "Douglas Fir-Larch No. 2 lumber"
        )
        self.section_var.set(state.section)
        self.deflection_limit_var.set(state.deflection_limit)
        self._refresh_section_choices()

        for row in self.load_rows:
            for variable, token in row.trace_tokens:
                variable.trace_remove("write", token)
            row.frame.destroy()
        self.load_rows.clear()
        for load in state.loads:
            if load.kind == "point":
                self._add_load(
                    "point",
                    {
                        "magnitude": repr(load.magnitude),
                        "position": repr(load.position),
                    },
                    refresh=False,
                )
            else:
                self._add_load(
                    "uniform",
                    {
                        "magnitude": repr(load.magnitude),
                        "start": repr(load.start),
                        "end": repr(load.end),
                    },
                    refresh=False,
                )
        self._syncing = False
        self._sync_load_bounds(state.span)
        self._has_changed = False
        self.pointer_x = state.span / 2
        self.pointer_visible = False
        self.pointer_readout.grid_remove()
        self._refresh()

    def _update_window_title(self) -> None:
        name = self.current_project_path.name if self.current_project_path else None
        self.root.title(f"Beam Designer - {name}" if name else "Beam Designer")

    def _export_results_csv(self) -> None:
        state, errors = self._read_state()
        if state is None:
            messagebox.showerror(
                "Cannot export results",
                "Correct the following inputs before exporting:\n\n" + "\n".join(errors),
                parent=self.root,
            )
            return
        selected = filedialog.asksaveasfilename(
            parent=self.root,
            title="Export Results as CSV",
            defaultextension=".csv",
            initialfile="beam-results.csv",
            filetypes=(("CSV files", "*.csv"),),
        )
        if not selected:
            return
        try:
            write_results_csv(selected, analyze(state))
        except OSError as error:
            messagebox.showerror(
                "Could not export results",
                f"The CSV file could not be written:\n{error}",
                parent=self.root,
            )
            return
        self.status_var.set(f"Exported {Path(selected).name}")

    def _export_calculation_sheet(self) -> None:
        state, errors = self._read_state()
        if state is None:
            messagebox.showerror(
                "Cannot export calculation sheet",
                "Correct the following inputs before exporting:\n\n" + "\n".join(errors),
                parent=self.root,
            )
            return
        selected = filedialog.asksaveasfilename(
            parent=self.root,
            title="Export Calculation Sheet as PDF",
            defaultextension=".pdf",
            initialfile="beam-calculation-sheet.pdf",
            filetypes=(("PDF files", "*.pdf"),),
        )
        if not selected:
            return
        try:
            create_calculation_sheet(selected, analyze(state))
        except (OSError, ValueError) as error:
            messagebox.showerror(
                "Could not export calculation sheet",
                f"The PDF file could not be created:\n{error}",
                parent=self.root,
            )
            return
        self.status_var.set(f"Exported {Path(selected).name}")

    def _current_span(self) -> float:
        try:
            value = float(self.span_var.get())
        except ValueError:
            return 20.0
        return value if isfinite(value) and 4 <= value <= 40 else 20.0

    def _refresh_section_choices(self) -> None:
        sections = MATERIALS[self.material_var.get()].sections
        self.section_combo.configure(values=tuple(sections))
        if self.section_var.get() not in sections:
            self.section_var.set("2x10" if self.material_var.get() == "lumber" else "W12x26")
        self._refresh_section_info()

    def _refresh_section_info(self) -> None:
        material = MATERIALS[self.material_var.get()]
        section = material.sections[self.section_var.get()]
        weight = f"{section.weight:g} lb/ft" if section.weight is not None else "not specified"
        self.section_info.configure(
            text=(
                f"E {material.elastic_modulus:,.0f} ksi | Ix {section.ix:g} in^4 | "
                f"Sx {section.sx:g} in^3 | Fb {material.allowable_stress:g} ksi | "
                f"Weight {weight}"
            )
        )

    def _on_material_changed(self, event: tk.Event) -> None:
        if not isinstance(event.widget, ttk.Combobox):
            return
        self.material_var.set(
            "lumber" if event.widget.get().startswith("Douglas") else "steel"
        )
        default = "2x10" if self.material_var.get() == "lumber" else "W12x26"
        self.section_var.set(default)
        self._refresh_section_choices()
        self._refresh()

    def _on_input_changed(self, *args: str) -> None:
        _ = args
        if self._syncing:
            return
        if self.section_var.get() in MATERIALS[self.material_var.get()].sections:
            self._refresh_section_info()
        self._has_changed = True
        self._refresh()

    def _on_span_changed(self, *args: str) -> None:
        _ = args
        if self._syncing:
            return
        value = self._parse_number(self.span_var.get())
        if value is not None and 4 <= value <= 40:
            self._syncing = True
            self.span_scale_var.set(value)
            self._syncing = False
            self._sync_load_bounds(value)
        self._has_changed = True
        self._refresh()

    def _on_span_scale(self, value: str) -> None:
        if self._syncing:
            return
        span = float(value)
        self._syncing = True
        self.span_var.set(f"{span:.2f}".rstrip("0").rstrip("."))
        self._syncing = False
        self._sync_load_bounds(span)
        self._has_changed = True
        self._refresh()

    def _sync_load_bounds(self, span: float) -> None:
        self._syncing = True
        for row in self.load_rows:
            if row.kind == "point":
                row.spins[1].configure(to=span)
                position = self._parse_number(row.variables["position"].get())
                if position is not None and position > span:
                    row.variables["position"].set(f"{span:.2f}")
            else:
                row.spins[1].configure(to=span)
                row.spins[2].configure(to=span)
                start = self._parse_number(row.variables["start"].get())
                end = self._parse_number(row.variables["end"].get())
                if start is not None and start > span:
                    row.variables["start"].set(f"{span:.2f}")
                if end is not None and end > span:
                    row.variables["end"].set(f"{span:.2f}")
                start = self._parse_number(row.variables["start"].get())
                end = self._parse_number(row.variables["end"].get())
                if start is not None and end is not None and start > end:
                    row.variables["start"].set(f"{end:.2f}")
        self._syncing = False

    @staticmethod
    def _parse_number(raw: str) -> float | None:
        if not raw.strip():
            return None
        try:
            value = float(raw)
        except ValueError:
            return None
        return value if isfinite(value) else None

    def _read_state(self) -> tuple[BeamState | None, list[str]]:
        errors: list[str] = []

        def read_number(raw: str, label: str) -> float | None:
            value = self._parse_number(raw)
            if value is None:
                errors.append(f"{label} must be a number.")
            return value

        span = read_number(self.span_var.get(), "Span")
        loads: list[BeamLoad] = []
        for index, row in enumerate(self.load_rows, start=1):
            if row.kind == "point":
                magnitude = read_number(
                    row.variables["magnitude"].get(), f"Point load {index} magnitude"
                )
                position = read_number(
                    row.variables["position"].get(), f"Point load {index} position"
                )
                if magnitude is not None and position is not None:
                    loads.append(BeamLoad("point", magnitude, position=position))
            else:
                magnitude = read_number(
                    row.variables["magnitude"].get(), f"Uniform load {index} magnitude"
                )
                start = read_number(
                    row.variables["start"].get(), f"Uniform load {index} start"
                )
                end = read_number(
                    row.variables["end"].get(), f"Uniform load {index} end"
                )
                if magnitude is not None and start is not None and end is not None:
                    loads.append(BeamLoad("uniform", magnitude, start=start, end=end))

        if span is None or errors:
            return None, errors
        raw_support = self.support_var.get()
        if raw_support == "simply-supported":
            support: Literal["simply-supported", "cantilever"] = "simply-supported"
        elif raw_support == "cantilever":
            support = "cantilever"
        else:
            return None, ["Choose a supported beam type."]
        state = BeamState(
            support=support,
            span=span,
            loads=tuple(loads),
            material=self.material_var.get(),
            section=self.section_var.get(),
            deflection_limit=self.deflection_limit_var.get(),
        )
        errors.extend(validate_state(state))
        return (None, errors) if errors else (state, [])

    def _refresh(self) -> None:
        state, errors = self._read_state()
        if errors or state is None:
            self.current_analysis = None
            self.status_var.set("Check inputs")
            self.validation_message.configure(text=" ".join(errors))
            self.validation_message.grid()
            self.bending_card.grid_remove()
            self.deflection_card.grid_remove()
            self.recommendation_frame.grid_remove()
            self.pointer_visible = False
            self.pointer_readout.grid_remove()
            self.plot_canvas.delete("all")
            self.plot_canvas.configure(scrollregion=(0, 0, 700, 200))
            return

        self.validation_message.grid_remove()
        self.current_analysis = analyze(state)
        if self._has_changed:
            self.status_var.set("Updated")
        self.pointer_x = min(state.span, max(0.0, self.pointer_x))
        self._update_check_card(
            self.bending_labels,
            f"{self.current_analysis.bending_stress:.2f} ksi",
            f"{self.current_analysis.allowable_stress:.2f} ksi",
            self.current_analysis.bending_utilization,
        )
        self._update_check_card(
            self.deflection_labels,
            f"{abs(self.current_analysis.deflection.absolute.deflection):.3f} in",
            f"{self.current_analysis.allowable_deflection:.3f} in (L/{state.deflection_limit})",
            self.current_analysis.deflection_utilization,
        )
        self.deflection_tooltip.text = (
            f"Deflection utilization = actual maximum / (L/{state.deflection_limit}); "
            f"allowable = {self.current_analysis.allowable_deflection:.3f} in."
        )
        self.bending_card.grid()
        self.deflection_card.grid()
        self.recommendation_frame.grid()
        self._update_recommendation()
        self._draw_plot()

    @staticmethod
    def _update_check_card(
        labels: dict[str, ttk.Widget],
        actual: str,
        allowable: str,
        ratio: float,
    ) -> None:
        labels["value"].configure(text=actual)
        labels["allowable"].configure(text=f"Allowable: {allowable}")
        labels["utilization"].configure(text=f"Utilization: {ratio * 100:.2f}%")
        bar = labels["bar"]
        bar.configure(
            value=min(100.0, ratio * 100),
            style=(
                "Red.Horizontal.TProgressbar"
                if ratio > 1
                else "Amber.Horizontal.TProgressbar"
                if ratio >= 0.7
                else "Green.Horizontal.TProgressbar"
            ),
        )
        status = labels["status"]
        status.configure(
            text="PASS" if ratio <= 1 else "FAIL",
            foreground=GREEN if ratio <= 1 else RED,
        )

    def _update_recommendation(self) -> None:
        if self.current_analysis is None:
            return
        recommendation = recommend_section(self.current_analysis)
        if recommendation.passes:
            message = (
                f"{recommendation.section_name} passes both bending and deflection "
                "checks. This is the lightest passing section."
            )
        else:
            message = (
                "No section passes. Closest option: "
                f"{recommendation.section_name} "
                f"({recommendation.governing_utilization * 100:.1f}% governing utilization)."
            )
        self.recommendation_text.configure(text=message)
        self.recommendation_button.configure(
            text=f"Use {recommendation.section_name}",
            command=lambda name=recommendation.section_name: self._select_section(name),
        )

    def _select_section(self, name: str) -> None:
        self.section_var.set(name)

    def _apply_recommendation(self) -> None:
        if self.current_analysis is None:
            return
        recommendation = recommend_section(self.current_analysis)
        self._select_section(recommendation.section_name)

    def _on_plot_resize(self, event: tk.Event) -> None:
        if self.current_analysis is not None:
            self._draw_plot(event.width)

    def _draw_plot(self, requested_width: int | None = None) -> None:
        analysis = self.current_analysis
        if analysis is None:
            return
        canvas = self.plot_canvas
        canvas.delete("all")
        width = max(canvas.winfo_width(), requested_width or 0, 760)
        beam_left = 76.0
        beam_right = width - 34.0
        beam_y = 129.0
        diagram_top = 225.0
        diagram_height = 190.0
        canvas_height = diagram_top + 3 * diagram_height + 12
        canvas.configure(scrollregion=(0, 0, width, canvas_height))
        self._beam_plot = (beam_left, beam_right, beam_y, canvas_height)

        def x_pixel(x: float) -> float:
            return beam_left + (x / analysis.state.span) * (beam_right - beam_left)

        max_deflection = max(
            (abs(sample.deflection) for sample in analysis.samples), default=0.0
        )
        deflection_scale = 32 / max_deflection if max_deflection > 1e-12 else 0.0

        def beam_y_at(x: float) -> float:
            return beam_y + analysis.value_at(x).deflection * deflection_scale

        canvas.create_text(
            beam_left, 12, text="Beam and loading", anchor="w", font=("Segoe UI", 10, "bold"),
            fill=INK,
        )
        canvas.create_text(
            beam_right, 12, text="Stress: green = low, red = maximum", anchor="e",
            font=("Segoe UI", 8), fill=MUTED,
        )
        canvas.create_line(beam_left, 190, beam_right, 190, fill="#dbe3ee")

        points = analysis.samples
        max_moment = max((abs(sample.moment) for sample in points), default=0.0)
        beam_coordinates = [
            (x_pixel(sample.x), beam_y + sample.deflection * deflection_scale, sample.moment)
            for sample in points
        ]
        for start, end in zip(beam_coordinates, beam_coordinates[1:]):
            stress_ratio = (
                (abs(start[2]) + abs(end[2])) / (2 * max_moment)
                if max_moment > 1e-12
                else 0.0
            )
            canvas.create_line(
                start[0], start[1], end[0], end[1],
                fill=self._stress_color(stress_ratio),
                width=10,
                capstyle=tk.ROUND,
            )

        left_x, right_x = x_pixel(0), x_pixel(analysis.state.span)
        left_y, right_y = beam_y_at(0), beam_y_at(analysis.state.span)
        if analysis.state.support == "cantilever":
            canvas.create_line(left_x - 8, left_y - 32, left_x - 8, left_y + 38, fill=BLUE, width=5)
            for offset in range(-28, 35, 10):
                canvas.create_line(
                    left_x - 15, left_y + offset, left_x - 8, left_y + offset - 6, fill=BLUE
                )
        else:
            canvas.create_polygon(
                left_x - 13, left_y + 2, left_x + 13, left_y + 2, left_x, left_y + 20,
                fill="#dbeafe", outline=BLUE, width=2,
            )
            canvas.create_line(left_x - 19, left_y + 22, left_x + 19, left_y + 22, fill=BLUE)
            canvas.create_polygon(
                right_x - 13, right_y + 2, right_x + 13, right_y + 2, right_x, right_y + 20,
                fill="#dbeafe", outline=BLUE, width=2,
            )
            canvas.create_line(right_x - 19, right_y + 22, right_x + 19, right_y + 22, fill=BLUE)

        for load in analysis.state.loads:
            if load.kind == "point":
                position = load.position
                x = x_pixel(position)
                target_y = beam_y_at(position) - 7
                canvas.create_line(x, 54, x, target_y, fill=BLUE, width=2, arrow=tk.LAST)
                canvas.create_text(
                    x, 44,
                    text=f"{load.magnitude:.2f} k @ {position:.2f} ft",
                    anchor="s", fill=INK, font=("Segoe UI", 8),
                )
            else:
                start = max(0.0, load.start)
                end = min(analysis.state.span, load.end)
                if end > start:
                    count = max(2, min(10, int((end - start) / max(1, analysis.state.span / 8)) + 1))
                    for step in range(count):
                        position = start + (end - start) * step / (count - 1)
                        x = x_pixel(position)
                        canvas.create_line(
                            x, 64, x, beam_y_at(position) - 7,
                            fill=BLUE, width=1, arrow=tk.LAST,
                        )
                canvas.create_text(
                    x_pixel((start + end) / 2), 38,
                    text=f"{load.magnitude:.2f} kip/ft ({start:.2f}–{end:.2f} ft)",
                    anchor="s", fill=INK, font=("Segoe UI", 8),
                )

        if analysis.state.support == "cantilever":
            self._draw_reaction(canvas, left_x, left_y, analysis.reactions.left, "Ay")
            canvas.create_arc(
                left_x + 20, left_y + 20, left_x + 68, left_y + 68,
                start=45, extent=285, style=tk.ARC, outline=BLUE, width=2,
            )
            canvas.create_text(
                left_x + 75, left_y + 47,
                text=f"MA {abs(analysis.reactions.fixed_moment):.2f} kip-ft",
                anchor="w", fill=INK, font=("Segoe UI", 8),
            )
        else:
            self._draw_reaction(canvas, left_x, left_y, analysis.reactions.left, "RA")
            self._draw_reaction(canvas, right_x, right_y, analysis.reactions.right, "RB")
        canvas.create_text(beam_left, 199, text="0 ft", anchor="w", fill=MUTED, font=("Segoe UI", 8))
        canvas.create_text(
            beam_right, 199, text=f"{analysis.state.span:.2f} ft", anchor="e",
            fill=MUTED, font=("Segoe UI", 8),
        )
        self._draw_diagram(
            analysis, "shear", "Shear diagram", "kips", diagram_top,
            beam_left, beam_right, diagram_height,
        )
        self._draw_diagram(
            analysis, "moment", "Moment diagram", "kip-ft", diagram_top + diagram_height,
            beam_left, beam_right, diagram_height,
        )
        self._draw_diagram(
            analysis, "deflection", "Deflected shape", "in", diagram_top + 2 * diagram_height,
            beam_left, beam_right, diagram_height,
        )
        self._draw_guides()

    @staticmethod
    def _stress_color(ratio: float) -> str:
        stops = ((0.0, (22, 163, 74)), (0.5, (245, 158, 11)), (1.0, (220, 38, 38)))
        position = min(1.0, max(0.0, ratio))
        for (start, color_a), (end, color_b) in zip(stops, stops[1:]):
            if position <= end:
                fraction = (position - start) / (end - start)
                color = tuple(
                    round(a + (b - a) * fraction)
                    for a, b in zip(color_a, color_b)
                )
                return f"#{color[0]:02x}{color[1]:02x}{color[2]:02x}"
        return "#dc2626"

    @staticmethod
    def _draw_reaction(
        canvas: tk.Canvas, x: float, y: float, magnitude: float, label: str
    ) -> None:
        canvas.create_line(x, y + 45, x, y + 9, fill=GREEN, width=2, arrow=tk.LAST)
        canvas.create_text(
            x, y + 49, text=f"{label} {magnitude:.2f} k ↑",
            anchor="n", fill=INK, font=("Segoe UI", 8),
        )

    def _draw_diagram(
        self,
        analysis: Analysis,
        key: str,
        title: str,
        units: str,
        top: float,
        left: float,
        right: float,
        height: float,
    ) -> None:
        canvas = self.plot_canvas
        bottom = top + height - 8
        canvas.create_rectangle(left - 24, top + 2, right + 12, bottom, fill="#ffffff", outline="#e2e8f0")
        canvas.create_text(
            left - 12, top + 18, text=title, anchor="w",
            fill=INK, font=("Segoe UI", 10, "bold"),
        )
        extrema = getattr(analysis, key)
        self._draw_extrema_text(canvas, extrema, key, units, right - 4, top + 18)

        sample_values: list[Sample]
        if key == "shear":
            sample_values = list(analysis.shear_plot_samples)
        else:
            sample_values = list(analysis.samples)
        value_name = {"shear": "shear", "moment": "moment", "deflection": "deflection"}[key]
        values = [getattr(sample, value_name) for sample in sample_values]
        max_positive = max([0.0, *values])
        max_negative = min([0.0, *values])
        amplitude = max(max_positive, abs(max_negative), 1e-9)
        baseline = top + 101
        graph_top = top + 36
        graph_bottom = top + 157
        scale = min((baseline - graph_top), (graph_bottom - baseline)) / amplitude
        canvas.create_line(left, baseline, right, baseline, fill="#64748b", width=1)

        def y_pixel(value: float) -> float:
            if key == "deflection":
                return baseline + value * scale
            return baseline - value * scale

        coordinates = [
            (left + sample.x / analysis.state.span * (right - left), y_pixel(getattr(sample, value_name)))
            for sample in sample_values
        ]
        if coordinates:
            fill_points: list[float] = [coordinates[0][0], baseline]
            for x, y in coordinates:
                fill_points.extend((x, y))
            fill_points.extend((coordinates[-1][0], baseline))
            canvas.create_polygon(
                *fill_points, fill="#dbeafe", outline="", stipple="gray25"
            )
            if len(coordinates) > 1:
                canvas.create_line(
                    *(coordinate for point in coordinates for coordinate in point),
                    fill=BLUE, width=2,
                )
        canvas.create_text(left, graph_bottom + 10, text="0 ft", anchor="w", fill=MUTED, font=("Segoe UI", 8))
        canvas.create_text(
            right, graph_bottom + 10, text=f"{analysis.state.span:.2f} ft",
            anchor="e", fill=MUTED, font=("Segoe UI", 8),
        )
        if key == "deflection":
            canvas.create_text(
                right - 4, bottom - 4,
                text="Downward positive; vertical scale exaggerated",
                anchor="se", fill=MUTED, font=("Segoe UI", 7),
            )

    @staticmethod
    def _draw_extrema_text(
        canvas: tk.Canvas,
        extrema: Extrema,
        key: str,
        units: str,
        x: float,
        y: float,
    ) -> None:
        field = "shear" if key == "shear" else "moment" if key == "moment" else "deflection"

        def value(sample: Sample) -> float:
            return getattr(sample, field)

        max_locations = ", ".join(f"{location:.2f}" for location in extrema.absolute_locations)
        text = (
            f"max {value(extrema.maximum):.3g} @ {extrema.maximum.x:.2f} ft   "
            f"min {value(extrema.minimum):.3g} @ {extrema.minimum.x:.2f} ft   "
            f"|max| {abs(value(extrema.absolute)):.3g} {units} @ {max_locations} ft"
        )
        canvas.create_text(
            x, y, text=text, anchor="e", fill=MUTED, font=("Segoe UI", 7)
        )

    def _on_plot_press(self, event: tk.Event) -> None:
        if self.current_analysis is None or self._beam_plot is None:
            return
        left, right, beam_y = self._beam_plot[:3]
        if not left <= event.x <= right:
            return
        self.dragging_load = None
        y = self.plot_canvas.canvasy(event.y)
        point_index = 0
        for load in self.current_analysis.state.loads:
            if load.kind != "point":
                continue
            point_x = left + load.position / self.current_analysis.state.span * (right - left)
            expected_y = beam_y + self.current_analysis.value_at(load.position).deflection * (
                32 / max(
                    max(abs(sample.deflection) for sample in self.current_analysis.samples),
                    1e-12,
                )
            )
            if abs(event.x - point_x) <= 14 and abs(y - expected_y) <= 35:
                self.dragging_load = point_index
                break
            point_index += 1

    def _on_plot_drag(self, event: tk.Event) -> None:
        if self.dragging_load is None or self.current_analysis is None or self._beam_plot is None:
            return
        left, right = self._beam_plot[:2]
        x = (event.x - left) / (right - left) * self.current_analysis.state.span
        span = self.current_analysis.state.span
        position = min(span, max(0.0, round(x * 4) / 4))
        point_rows = [row for row in self.load_rows if row.kind == "point"]
        if self.dragging_load < len(point_rows):
            self.pointer_x = position
            point_rows[self.dragging_load].variables["position"].set(f"{position:.2f}")
            self.pointer_visible = True
            self._draw_guides()

    def _on_plot_release(self, event: tk.Event) -> None:
        _ = event
        self.dragging_load = None

    def _on_plot_motion(self, event: tk.Event) -> None:
        if self.current_analysis is None or self._beam_plot is None:
            return
        left, right = self._beam_plot[:2]
        if left <= event.x <= right:
            self.pointer_x = min(
                self.current_analysis.state.span,
                max(0.0, (event.x - left) / (right - left) * self.current_analysis.state.span),
            )
            self.pointer_visible = True
            self._draw_guides()

    def _on_plot_leave(self, event: tk.Event) -> None:
        _ = event
        if self.dragging_load is None:
            self.pointer_visible = False
            self.pointer_readout.grid_remove()
            self.plot_canvas.delete("guide")

    def _draw_guides(self) -> None:
        analysis = self.current_analysis
        if analysis is None or self._beam_plot is None:
            return
        canvas = self.plot_canvas
        canvas.delete("guide")
        if not self.pointer_visible:
            self.pointer_readout.grid_remove()
            return
        left, right = self._beam_plot[:2]
        x = left + self.pointer_x / analysis.state.span * (right - left)
        canvas.create_line(x, 23, x, 213, fill="#0f172a", dash=(3, 3), tags="guide")
        for index in range(3):
            top = 225 + index * 190
            canvas.create_line(x, top + 24, x, top + 164, fill="#0f172a", dash=(3, 3), tags="guide")
        value = analysis.value_at(self.pointer_x)
        self.pointer_readout_var.set(
            f"x = {self.pointer_x:.2f} ft   V = {value.shear:.3g} kips   "
            f"M = {value.moment:.3g} kip-ft   y = {value.deflection:.3f} in"
        )
        self.pointer_readout.grid()


def main() -> None:
    root = tk.Tk()
    BeamDesigner(root)
    root.mainloop()


if __name__ == "__main__":
    main()
