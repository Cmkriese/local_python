"""Earthquake Shaker: a small Tkinter tower editor and shake-test demonstrator.

Run with ``python gui.py``. The response model is an educational simplified
shear-building approximation and is not a structural design tool.
"""
import json
import math
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog, filedialog


BG = "#f3f6f8"
INK = "#203342"
BLUE = "#176b87"


class EarthquakeShaker:
    def __init__(self, root):
        self.root = root
        root.title("Earthquake Shaker | Desktop Studio")
        root.geometry("1260x820")
        root.minsize(940, 650)
        root.configure(bg=BG)
        self.members = []
        self.undo_stack = []
        self.saved = {}
        self.project_path = None
        self.dirty = False
        self.selected = None
        self.start_node = None
        self.preview_node = None
        self.running = False
        self.paused = False
        self.time = 0.0
        self.timer = None
        self.max_disp = 0.0
        self.collapse = 0.0
        self.collapse_triggered = False
        self.mode = tk.StringVar(value="Select")
        self.floors = tk.IntVar(value=5)
        self.bays = tk.IntVar(value=3)
        self.height = tk.DoubleVar(value=10)
        self.spacing = tk.DoubleVar(value=15)
        self.material = tk.StringVar(value="Steel")
        self.motion = tk.StringVar(value="Sine")
        self.frequency = tk.DoubleVar(value=1.0)
        self.pga = tk.DoubleVar(value=.25)
        self.duration = tk.DoubleVar(value=10)
        self.damping = tk.DoubleVar(value=5)
        self.speed = tk.DoubleVar(value=1)
        self.status = tk.StringVar(value="Ready • Select a tool, then click grid points to place members")
        self._build()
        self.root.protocol("WM_DELETE_WINDOW", self.close_app)
        for variable in (self.floors, self.bays, self.height, self.spacing,
                         self.material, self.motion, self.frequency, self.pga, self.duration):
            variable.trace_add("write", self.mark_dirty)
        self.update_title()
        self.draw()

    def _build(self):
        menubar = tk.Menu(self.root)
        file_menu = tk.Menu(menubar, tearoff=False)
        file_menu.add_command(label="New", accelerator="Ctrl+N", command=self.new_project)
        file_menu.add_command(label="Open…", accelerator="Ctrl+O", command=self.open_project)
        file_menu.add_separator()
        file_menu.add_command(label="Save", accelerator="Ctrl+S", command=self.save_project)
        file_menu.add_command(label="Save As…", accelerator="Ctrl+Shift+S", command=self.save_project_as)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.close_app)
        menubar.add_cascade(label="File", menu=file_menu)
        self.root.config(menu=menubar)
        self.root.bind("<Control-n>", lambda e: self.new_project())
        self.root.bind("<Control-o>", lambda e: self.open_project())
        self.root.bind("<Control-s>", lambda e: self.save_project())
        self.root.bind("<Control-Shift-S>", lambda e: self.save_project_as())
        header = tk.Frame(self.root, bg=INK, height=58)
        header.pack(fill="x")
        tk.Label(header, text="EARTHQUAKE SHAKER", bg=INK, fg="white", font=("Segoe UI", 16, "bold")).pack(side="left", padx=20, pady=14)
        tk.Label(header, text="DESKTOP STUDIO", bg=INK, fg="#a9d8e6", font=("Segoe UI", 9, "bold")).pack(side="left", pady=18)
        tk.Button(header, text="Save tower", command=self.save_tower, bg=BLUE, fg="white", relief="flat", padx=14).pack(side="right", padx=18, pady=12)

        body = tk.Frame(self.root, bg=BG)
        body.pack(fill="both", expand=True, padx=12, pady=10)
        left = tk.Frame(body, bg="white", width=240, padx=12, pady=10)
        left.pack(side="left", fill="y", padx=(0, 10)); left.pack_propagate(False)
        center = tk.Frame(body, bg="white", padx=10, pady=10)
        center.pack(side="left", fill="both", expand=True, padx=(0, 10))
        right = tk.Frame(body, bg="white", width=270, padx=12, pady=10)
        right.pack(side="right", fill="y"); right.pack_propagate(False)
        self._label(left, "TOWER GEOMETRY")
        self._spin(left, "Stories", self.floors, 1, 30)
        self._spin(left, "Bays", self.bays, 1, 8)
        self._spin(left, "Story height (ft)", self.height, 8, 30)
        self._spin(left, "Bay spacing (ft)", self.spacing, 5, 30)
        ttk.Button(left, text="Apply geometry", command=self.geometry_changed).pack(fill="x", pady=5)
        self._label(left, "PLACEMENT TOOLS")
        for name in ("Select", "Column", "Beam", "Brace", "Joint", "Floor"):
            ttk.Radiobutton(left, text=name, value=name, variable=self.mode, command=self._tool).pack(anchor="w", pady=2)
        ttk.Label(left, text="Material preset").pack(anchor="w", pady=(10, 2))
        ttk.Combobox(left, textvariable=self.material, values=("Steel", "Concrete", "Timber", "Masonry"), state="readonly").pack(fill="x")
        row = tk.Frame(left, bg="white"); row.pack(fill="x", pady=8)
        ttk.Button(row, text="Undo", command=self.undo).pack(side="left", expand=True, fill="x")
        ttk.Button(row, text="Delete", command=self.delete_selected).pack(side="left", expand=True, fill="x", padx=(4, 0))
        ttk.Button(left, text="Clear members", command=self.clear).pack(fill="x")
        ttk.Button(left, text="Cancel placement (Esc)", command=self.cancel_placement).pack(fill="x", pady=(5, 0))
        self.hint = tk.Label(left, text="Select a tool to begin.", bg="white", fg="#607481", wraplength=210, justify="left")
        self.hint.pack(anchor="w", pady=10)

        top = tk.Frame(center, bg="white"); top.pack(fill="x")
        tk.Label(top, text="MODEL EDITOR", bg="white", fg=INK, font=("Segoe UI", 11, "bold")).pack(side="left")
        self.model_badge = tk.Label(top, text="2D FRAME • X DIRECTION", bg="#e7f2f5", fg=BLUE, padx=8, pady=4)
        self.model_badge.pack(side="right")
        self.canvas = tk.Canvas(center, bg="#f8fbfc", highlightthickness=1, highlightbackground="#d6e1e6")
        self.canvas.pack(fill="both", expand=True, pady=8)
        self.canvas.bind("<Configure>", lambda e: self.draw())
        self.canvas.bind("<Button-1>", self.click_canvas)
        self.canvas.bind("<Motion>", self.move_canvas)
        self.root.bind("<Escape>", lambda e: self.cancel_placement())
        self._label(center, "GROUND MOTION")
        controls = tk.Frame(center, bg="white"); controls.pack(fill="x")
        ttk.Label(controls, text="Profile").pack(side="left")
        ttk.Combobox(controls, textvariable=self.motion, values=("Sine", "Pulse", "White noise"), width=12, state="readonly").pack(side="left", padx=4)
        for label, var, width in (("Frequency (Hz)", self.frequency, 6), ("PGA (g)", self.pga, 6), ("Duration (s)", self.duration, 6)):
            ttk.Label(controls, text=label).pack(side="left", padx=(8, 2))
            ttk.Entry(controls, textvariable=var, width=width).pack(side="left")
        runrow = tk.Frame(center, bg="white"); runrow.pack(fill="x", pady=(8, 0))
        ttk.Button(runrow, text="▶  Run test", command=self.start_test).pack(side="left")
        ttk.Button(runrow, text="Ⅱ  Pause / Resume", command=self.pause_test).pack(side="left", padx=5)
        ttk.Button(runrow, text="↻  Reset", command=self.reset_test).pack(side="left")
        ttk.Label(runrow, text="Speed").pack(side="left", padx=(14, 3))
        ttk.Combobox(runrow, textvariable=self.speed, values=(.25, .5, 1, 2, 5), width=5, state="readonly").pack(side="left")

        self._label(right, "LIVE RESULTS")
        self.result_text = tk.StringVar(value="Run a shake test to calculate response.")
        tk.Label(right, textvariable=self.result_text, bg="white", fg=INK, justify="left", anchor="nw", wraplength=235, font=("Segoe UI", 10)).pack(fill="x", pady=5)
        self.progress = ttk.Progressbar(right, maximum=100)
        self.progress.pack(fill="x", pady=5)
        ttk.Separator(right).pack(fill="x", pady=8)
        self._label(right, "COST SUMMARY")
        self.cost_text = tk.StringVar()
        tk.Label(right, textvariable=self.cost_text, bg="white", fg=INK, justify="left", anchor="nw", font=("Segoe UI", 10)).pack(fill="x")
        ttk.Separator(right).pack(fill="x", pady=8)
        self._label(right, "SAVED DESIGNS")
        self.saved_list = tk.Listbox(right, height=8, font=("Segoe UI", 9), activestyle="dotbox")
        self.saved_list.pack(fill="x", pady=4)
        ttk.Button(right, text="Compare selected", command=self.compare).pack(fill="x")
        ttk.Button(right, text="Export design JSON", command=self.export_design).pack(fill="x", pady=4)
        tk.Label(self.root, textvariable=self.status, bg="#e6eef1", fg="#405765", anchor="w", padx=12, pady=5).pack(fill="x")
        self.update_cost()

    def mark_dirty(self, *_):
        self.dirty = True
        self.update_title()

    def update_title(self):
        name = self.project_path or "Untitled project"
        marker = "*" if self.dirty else ""
        self.root.title(f"{marker}{name} — Earthquake Shaker | Desktop Studio")

    def project_data(self):
        return {
            "format": "earthquake-shaker-project",
            "version": 1,
            "geometry": {"floors": self.floors.get(), "bays": self.bays.get(),
                         "height": self.height.get(), "spacing": self.spacing.get()},
            "material": self.material.get(),
            "ground_motion": {"profile": self.motion.get(), "frequency": self.frequency.get(),
                              "pga": self.pga.get(), "duration": self.duration.get()},
            "members": self.members,
            "saved_designs": self.saved,
        }

    def save_project(self):
        if not self.project_path:
            return self.save_project_as()
        return self.write_project(self.project_path)

    def save_project_as(self):
        path = filedialog.asksaveasfilename(
            title="Save Earthquake Shaker project", defaultextension=".eqs",
            filetypes=(("Earthquake Shaker project", "*.eqs"), ("JSON files", "*.json")))
        if not path:
            return False
        return self.write_project(path)

    def write_project(self, path):
        try:
            with open(path, "w", encoding="utf-8") as project_file:
                json.dump(self.project_data(), project_file, indent=2)
        except (OSError, TypeError, ValueError) as exc:
            messagebox.showerror("Could not save project", str(exc))
            return False
        self.project_path = path
        self.dirty = False
        self.update_title()
        self.status.set(f"Project saved: {path}")
        return True

    def open_project(self):
        path = filedialog.askopenfilename(
            title="Open Earthquake Shaker project",
            filetypes=(("Earthquake Shaker project", "*.eqs"), ("JSON files", "*.json"), ("All files", "*.*")))
        if not path:
            return
        if not self.confirm_discard():
            return
        try:
            with open(path, "r", encoding="utf-8") as project_file:
                data = json.load(project_file)
            geometry = data["geometry"]
            floors = int(geometry["floors"]); bays = int(geometry["bays"])
            height = float(geometry["height"]); spacing = float(geometry["spacing"])
            if not 1 <= floors <= 30 or not 1 <= bays <= 8 or not 8 <= height <= 30 or not 5 <= spacing <= 30:
                raise ValueError("Project geometry is outside the supported ranges.")
            members = data["members"]
            if not isinstance(members, list):
                raise ValueError("The project member list is invalid.")
            for member in members:
                if member.get("type") not in ("Column", "Beam", "Brace", "Floor", "Joint"):
                    raise ValueError("Project contains an unknown member type.")
                member["a"] = tuple(map(int, member["a"])); member["b"] = tuple(map(int, member["b"]))
                for point in (member["a"], member["b"]):
                    if len(point) != 2 or not 0 <= int(point[0]) <= bays or not 0 <= int(point[1]) <= floors:
                        raise ValueError("Project contains a point outside its grid.")
            ground = data.get("ground_motion", {})
            frequency = float(ground.get("frequency", 1.0))
            pga = float(ground.get("pga", .25)); duration = float(ground.get("duration", 10))
            if not .1 <= frequency <= 20 or not 0 <= pga <= 2 or not 1 <= duration <= 10:
                raise ValueError("Project ground-motion settings are outside the supported ranges.")
            material = data.get("material", "Steel")
            if material not in ("Steel", "Concrete", "Timber", "Masonry"):
                raise ValueError("Project material preset is not recognized.")
            profile = ground.get("profile", "Sine")
            if profile not in ("Sine", "Pulse", "White noise"):
                raise ValueError("Project ground-motion profile is not recognized.")
        except (OSError, json.JSONDecodeError, KeyError, TypeError, ValueError) as exc:
            messagebox.showerror("Could not open project", str(exc))
            return
        self.reset_test()
        self.floors.set(floors); self.bays.set(bays)
        self.height.set(height); self.spacing.set(spacing)
        self.members = members; self.material.set(material)
        self.frequency.set(frequency); self.pga.set(pga); self.duration.set(duration)
        self.motion.set(profile); self.saved = data.get("saved_designs", {})
        self.saved_list.delete(0, "end")
        for name in self.saved: self.saved_list.insert("end", name)
        self.project_path = path; self.dirty = False
        self.undo_stack.clear(); self.selected = None; self.cancel_placement(redraw=False)
        self.update_title(); self.draw()
        self.status.set(f"Opened project: {path}")

    def confirm_discard(self):
        if not self.dirty:
            return True
        answer = messagebox.askyesnocancel("Unsaved project", "Save changes before continuing?")
        if answer is None:
            return False
        if answer:
            return self.save_project()
        return True

    def new_project(self):
        if not self.confirm_discard():
            return
        self.reset_test()
        self.floors.set(5); self.bays.set(3); self.height.set(10); self.spacing.set(15)
        self.members = []; self.saved = {}; self.saved_list.delete(0, "end")
        self.material.set("Steel"); self.motion.set("Sine")
        self.frequency.set(1.0); self.pga.set(.25); self.duration.set(10)
        self.project_path = None; self.dirty = False; self.undo_stack.clear()
        self.selected = None; self.cancel_placement(redraw=False)
        self.update_title(); self.draw(); self.status.set("New project")

    def close_app(self):
        if self.confirm_discard():
            self.root.destroy()

    def _label(self, parent, text):
        tk.Label(parent, text=text, bg="white", fg=BLUE, font=("Segoe UI", 9, "bold")).pack(anchor="w", pady=(5, 7))

    def _spin(self, parent, label, var, low, high):
        ttk.Label(parent, text=label).pack(anchor="w")
        ttk.Spinbox(parent, from_=low, to=high, textvariable=var, width=10).pack(anchor="w", fill="x", pady=(1, 6))

    def geometry_changed(self):
        self.floors.set(max(1, min(30, int(self.floors.get()))))
        self.bays.set(max(1, min(8, int(self.bays.get()))))
        self.selected = None; self.draw(); self.update_cost()

    def _tool(self):
        self.cancel_placement(redraw=False)
        tool = self.mode.get()
        if tool == "Select":
            msg = "Click a member to select it."
        elif tool == "Joint":
            msg = "Click a grid node to add a joint."
        else:
            msg = f"{tool}: click Point A, then Point B. Press Esc to cancel."
        self.hint.config(text=msg)
        self.status.set(msg)
        self.draw()

    def _coords(self):
        w, h = max(300, self.canvas.winfo_width()), max(250, self.canvas.winfo_height())
        floors, bays = self.floors.get(), self.bays.get()
        dx = min((w-100)/max(1,bays), 74)
        dy = min((h-70)/max(1,floors), 54)
        ox = (w-bays*dx)/2; oy = h-34
        return ox, oy, dx, dy

    def draw(self, shift=0):
        if not hasattr(self, "canvas"): return
        c=self.canvas; c.delete("all"); ox,oy,dx,dy=self._coords(); floors=self.floors.get(); bays=self.bays.get()
        c.create_text(14, 14, text=f"{floors} stories  •  {bays} bays  •  {self.height.get():g} ft/story", anchor="nw", fill="#607481", font=("Segoe UI",9))
        for b in range(bays+1):
            x=ox+b*dx
            c.create_line(x,oy-floors*dy,x,oy,fill="#d7e1e5",dash=(3,4))
            for s in range(floors+1):
                node_x=x + shift*(s/max(1,floors))**1.5
                y=oy-s*dy
                c.create_oval(node_x-3,y-3,node_x+3,y+3,fill=BLUE,outline="")
        c.create_line(ox-18,oy,ox+bays*dx+18,oy,fill="#8b9ca5",width=2)
        for i,m in enumerate(self.members):
            a=self.node_xy(m["a"],ox,oy,dx,dy,shift); b=self.node_xy(m["b"],ox,oy,dx,dy,shift)
            if self.collapse>0:
                a=self.falling_point(a,m["a"][1],i,0,oy,dy)
                b=self.falling_point(b,m["b"][1],i,1,oy,dy)
            if m["type"] == "Joint":
                c.create_oval(a[0]-6,a[1]-6,a[0]+6,a[1]+6,fill="#667c87",outline="white",width=1,tags=(f"member{i}",))
                continue
            if m["type"] == "Floor":
                c.create_line(*a,*b,fill="#6ca9ba",width=9,capstyle="round",tags=(f"member{i}",))
                c.create_line(*a,*b,fill="#d8edf2",width=5,capstyle="round")
                continue
            color="#1d6d87" if m.get("status")!="failed" else "#ce4545"
            if m["type"]=="Brace": color="#e19a39"
            c.create_line(*a,*b,fill=color,width=5,capstyle="round",tags=(f"member{i}",))
            if m.get("joint"): c.create_oval(a[0]-4,a[1]-4,a[0]+4,a[1]+4,fill="#697b86",outline="")
        if self.start_node is not None:
            a=self.node_xy(self.start_node,ox,oy,dx,dy,shift)
            c.create_oval(a[0]-10,a[1]-10,a[0]+10,a[1]+10,fill="#fff0c2",outline="#e69b25",width=3)
            c.create_text(a[0]+12,a[1]-14,text="A",fill="#a15d00",font=("Segoe UI",10,"bold"),anchor="sw")
            if self.preview_node is not None:
                b=self.node_xy(self.preview_node,ox,oy,dx,dy,shift)
                c.create_line(*a,*b,fill="#e69b25",width=4,dash=(6,3),arrow="last")
                c.create_oval(b[0]-8,b[1]-8,b[0]+8,b[1]+8,fill="#fff8e5",outline="#e69b25",width=2)
                c.create_text(b[0]+10,b[1]-12,text="B?",fill="#a15d00",font=("Segoe UI",9,"bold"),anchor="sw")
        self.update_cost()

    def node_xy(self,n,ox,oy,dx,dy,shift=0):
        b,s=n
        return ox+b*dx+shift*(s/max(1,self.floors.get()))**1.5, oy-s*dy

    def falling_point(self, point, story, index, end, ground_y, story_px):
        """Give each failed component its own falling and tumbling path."""
        progress=min(1.0,self.collapse)
        x,y=point
        drop=progress*(story_px*(1.0+index%4*.18)+max(0,ground_y-y)*.45)
        direction=-1 if index%2 else 1
        x += direction*progress*(18+(index*17)%55)
        y += drop
        angle=direction*progress*(.2+(index%5)*.11)
        # Rotate each member about its midpoint so beams and columns visibly break apart.
        return x + (end-.5)*math.sin(angle)*24, y + (end-.5)*math.cos(angle)*12

    def nearest_node(self,x,y):
        ox,oy,dx,dy=self._coords(); b=round((x-ox)/dx); s=round((oy-y)/dy)
        if 0<=b<=self.bays.get() and 0<=s<=self.floors.get(): return b,s
        return None

    def click_canvas(self,e):
        if self.running: return
        tool=self.mode.get(); node=self.nearest_node(e.x,e.y)
        if tool=="Select":
            ix=self.canvas.find_closest(e.x,e.y); tags=self.canvas.gettags(ix)
            for t in tags:
                if t.startswith("member"):
                    self.selected=int(t[6:]); self.status.set(f"Selected {self.members[self.selected]['type']} • {self.members[self.selected]['material']}"); return
            self.selected=None; return
        if tool in ("Column","Beam","Brace","Floor"):
            if node is None:return
            if self.start_node is None:
                self.start_node=node; self.preview_node=None
                self.status.set(f"Point A selected: grid {node[0]}, story {node[1]}. Now choose Point B.")
                self.hint.config(text=f"Point A is marked. Click the endpoint for {tool}; press Esc to cancel.")
                self.draw(); return
            if tool=="Column" and node[0]!=self.start_node[0]:
                self.status.set("Columns must stay on one grid line. Choose Point B above or below Point A."); return
            if tool in ("Beam","Floor") and node[1]!=self.start_node[1]:
                self.status.set(f"{tool}s must stay on one story. Choose Point B along the same floor line."); return
            if node!=self.start_node:
                self.undo_stack.append(json.dumps(self.members)); self.members.append({"type":tool,"a":self.start_node,"b":node,"material":self.material.get(),"status":"intact"})
                self.mark_dirty()
                self.status.set(f"{tool} created from {self.start_node} to {node}. Select another tool or continue placing.")
            else: self.status.set("Point B must differ from Point A."); return
            self.start_node=None; self.preview_node=None; self.draw()
        elif tool=="Joint" and node:
            self.undo_stack.append(json.dumps(self.members)); self.members.append({"type":"Joint","a":node,"b":node,"material":self.material.get(),"status":"intact"}); self.draw()
            self.mark_dirty()
            self.status.set(f"Joint added at grid node {node}")

    def move_canvas(self,e):
        if self.start_node is None:return
        node=self.nearest_node(e.x,e.y)
        if node is None:return
        tool=self.mode.get()
        if tool=="Column" and node[0]!=self.start_node[0]:return
        if tool in ("Beam","Floor") and node[1]!=self.start_node[1]:return
        if node!=self.preview_node:
            self.preview_node=node; self.draw()

    def cancel_placement(self, redraw=True):
        had_point=self.start_node is not None
        self.start_node=None; self.preview_node=None
        if had_point:self.status.set("Placement cancelled; no member was created.")
        if redraw and hasattr(self,"canvas"):self.draw()

    def update_cost(self):
        counts={k:sum(m['type']==k for m in self.members) for k in ("Column","Beam","Brace","Floor")}
        unit={"Steel":180,"Concrete":140,"Timber":95,"Masonry":125}[self.material.get()]
        member=sum(counts[k] for k in ("Column","Beam","Brace"))*unit; floor=self.floors.get()*self.bays.get()*350 + counts["Floor"]*350
        joint=(counts["Column"]+counts["Beam"]+counts["Brace"]+counts["Floor"])*45; total=member+floor+joint
        if hasattr(self,"cost_text"): self.cost_text.set(f"Members     ${member:,.0f}\nFloor system  ${floor:,.0f}\nConnections   ${joint:,.0f}\n\nEstimated total\n${total:,.0f}\n\n{sum(counts.values())} members  •  {self.material.get()} preset")

    def validate(self):
        try:
            f=float(self.frequency.get()); p=float(self.pga.get()); d=float(self.duration.get())
            if not (0.1<=f<=20 and 0<=p<=2 and 1<=d<=10): raise ValueError
            return f,p,d
        except (ValueError,tk.TclError):
            messagebox.showerror("Check ground motion", "Use frequency 0.1–20 Hz, PGA 0–2 g, and duration 1–10 seconds."); return None

    def start_test(self):
        values=self.validate()
        if not values:return
        self.frequency.set(values[0]); self.pga.set(values[1]); self.duration.set(values[2])
        self.running=True; self.paused=False; self.time=0; self.max_disp=0
        self.collapse=0; self.collapse_triggered=False
        for m in self.members:m["status"]="intact"
        self.status.set("Shake test running • simplified 2D response model")
        self.tick()

    def tick(self):
        if not self.running or self.paused:return
        f=float(self.frequency.get()); p=float(self.pga.get()); dur=float(self.duration.get()); dt=.04*float(self.speed.get())
        self.time=min(dur,self.time+dt)
        ground=math.sin(2*math.pi*f*self.time)
        amp=(p*32.174)/(2*math.pi*f)**2*12
        # Story displacements grow toward the roof and move laterally with the
        # input motion, rather than translating the whole frame vertically.
        shake=ground*min(amp*18,70)
        self.max_disp=max(self.max_disp,abs(shake)/12)
        if p >= .70 and self.time >= min(1.2,dur*.22):
            self.collapse_triggered=True
        if self.collapse_triggered:
            self.collapse=min(1.0,self.collapse+dt*.22)
        self.draw(shake)
        self.progress['value']=100*self.time/dur
        drift=self.max_disp/max(1,self.floors.get()*self.height.get())
        score=max(1,min(100,round(100-1200*drift-18*p)))
        cost=sum((180 if m['material']=="Steel" else 140) for m in self.members)+self.floors.get()*self.bays.get()*395
        collapse_line="\n\nSTRUCTURE COLLAPSING" if self.collapse_triggered else ""
        self.result_text.set(f"Elapsed       {self.time:4.1f} / {dur:g} s\nGround PGA    {p:.2f} g\nPeak roof move {self.max_disp:.2f} ft\nMax drift      {drift*100:.2f}%\n\nStrength score {score} / 100\nEst. cost      ${cost:,.0f}{collapse_line}\n\nEducational simplified response estimate")
        if self.time>=dur:
            self.running=False; self.draw(); self.status.set("Test complete • Results are a simplified educational estimate"); return
        self.timer=self.root.after(40,self.tick)

    def pause_test(self):
        if self.running: self.paused=not self.paused; self.status.set("Test paused" if self.paused else "Test resumed"); self.tick()

    def reset_test(self):
        self.running=False; self.paused=False
        if self.timer:self.root.after_cancel(self.timer); self.timer=None
        self.time=0; self.collapse=0; self.collapse_triggered=False; self.progress['value']=0; self.result_text.set("Run a shake test to calculate response."); self.status.set("Test reset • Ready"); self.draw()

    def undo(self):
        if self.undo_stack:self.members=json.loads(self.undo_stack.pop()); self.mark_dirty(); self.draw()

    def delete_selected(self):
        if self.selected is not None and 0<=self.selected<len(self.members):
            self.undo_stack.append(json.dumps(self.members)); self.members.pop(self.selected); self.selected=None; self.mark_dirty(); self.draw()

    def clear(self):
        if self.members and messagebox.askyesno("Clear model", "Remove all placed members?"):
            self.undo_stack.append(json.dumps(self.members)); self.members=[]; self.mark_dirty(); self.draw()

    def snapshot(self):
        return {"floors":self.floors.get(),"bays":self.bays.get(),"height":self.height.get(),"spacing":self.spacing.get(),"members":self.members.copy(),"frequency":self.frequency.get(),"pga":self.pga.get(),"duration":self.duration.get()}

    def save_tower(self):
        name=simpledialog.askstring("Save tower", "Design name:", initialvalue=f"Tower {len(self.saved)+1}")
        if not name:return
        self.saved[name]=self.snapshot(); self.saved_list.insert("end",name); self.status.set(f"Saved design: {name}")
        self.mark_dirty()

    def compare(self):
        selection=self.saved_list.curselection()
        if len(selection)<2:
            messagebox.showinfo("Compare designs", "Save at least two designs, then select them in the list (Ctrl-click for multiple).")
            return
        names=[self.saved_list.get(i) for i in selection[:2]]
        def price(d):return len(d['members'])*180+d['floors']*d['bays']*350
        messagebox.showinfo("Design comparison", "\n\n".join(f"{n}\n{d['floors']} stories • {len(d['members'])} members • estimated ${price(d):,.0f}" for n,d in ((x,self.saved[x]) for x in names)))

    def export_design(self):
        path=filedialog.asksaveasfilename(defaultextension=".json",filetypes=[("JSON design","*.json")])
        if path:
            with open(path,"w",encoding="utf-8") as f:json.dump(self.snapshot(),f,indent=2)
            self.status.set(f"Exported design to {path}")


if __name__ == "__main__":
    root=tk.Tk()
    app=EarthquakeShaker(root)
    root.mainloop()
