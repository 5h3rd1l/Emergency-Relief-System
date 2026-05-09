"""
================================================================================
    Emergency Relief System - Professional Dashboard
    
    Modern card-based interface with real-time analytics
================================================================================
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import subprocess
import os
import threading
import time

class EmergencyApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🚨 Emergency Operations System")
        self.root.geometry("1200x850")
        self.root.configure(bg="#0a0a0a")
        self.setup_styles()
        
        # Backend Connection
        self.backend_executable = "ReliefSystem.exe"
        self.process = None
        self.running = True
        self.start_backend()
        
        # Layout Container
        self.container = tk.Frame(self.root, bg="#0a0a0a")
        self.container.pack(fill=tk.BOTH, expand=True)
        
        # Show Login Screen
        self.show_login()

    def setup_styles(self):
        style = ttk.Style()
        style.theme_use('clam')
        
        # Dark theme with red accents
        self.colors = {
            "bg": "#0a0a0a",           # Deep black
            "bg_secondary": "#1a1a1a", # Lighter black
            "card_bg": "#1e1e1e",      # Card background
            "dark": "#0d0d0d",
            "accent": "#ff0000",        # Bright red
            "accent_hover": "#cc0000",  # Darker red
            "danger": "#ff0000",
            "success": "#00ff00",       # Neon green
            "warning": "#ffaa00",
            "text_primary": "#ffffff",  # White
            "text_secondary": "#b0b0b0", # Gray
            "border": "#333333",
            "critical": "#ff0000",
            "high": "#ff6600",
            "moderate": "#ffaa00",
            "low": "#00ff00",
            "glow": "#ff0000"
        }
        
        style.configure('TFrame', background=self.colors["bg"])
        style.configure('Card.TFrame', background=self.colors["card_bg"], relief='flat')
        style.configure('Main.TLabel', font=('Segoe UI', 28, 'bold'), foreground=self.colors["accent"], background=self.colors["bg"])
        style.configure('Sub.TLabel', font=('Segoe UI', 12), foreground=self.colors["text_secondary"], background=self.colors["bg"])
        style.configure('CardTitle.TLabel', font=('Segoe UI', 12, 'bold'), foreground=self.colors["text_primary"], background=self.colors["card_bg"])
        style.configure('CardText.TLabel', font=('Segoe UI', 10), foreground=self.colors["text_secondary"], background=self.colors["card_bg"])
        
        style.configure('BigBtn.TButton', font=('Segoe UI', 14, 'bold'), padding=20)
        style.configure('Modern.TButton', font=('Segoe UI', 10), padding=10)

    def start_backend(self):
        if not os.path.exists(self.backend_executable):
            messagebox.showerror("Error", "ReliefSystem.exe not found!")
            self.root.destroy()
            return

        try:
            self.process = subprocess.Popen(
                [self.backend_executable],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1
            )
        except Exception as e:
            messagebox.showerror("Error", f"Backend failed: {e}")
            self.root.destroy()

    def show_login(self):
        self.clear_frame()
        self.current_view = None
        
        # Full screen dark background
        frame = tk.Frame(self.container, bg="#0a0a0a")
        frame.pack(expand=True, fill=tk.BOTH)
        
        # Center content
        content = tk.Frame(frame, bg="#0a0a0a")
        content.pack(expand=True)
        
        # Logo/Title with glow effect
        title_frame = tk.Frame(content, bg="#0a0a0a")
        title_frame.pack(pady=40)
        
        tk.Label(title_frame, text="🚨", font=('Segoe UI', 80), bg="#0a0a0a").pack()
        tk.Label(title_frame, text="EMERGENCY", 
                font=('Segoe UI', 36, 'bold'), fg="#ff0000", bg="#0a0a0a").pack()
        tk.Label(title_frame, text="OPERATIONS SYSTEM", 
                font=('Segoe UI', 24, 'bold'), fg="#ffffff", bg="#0a0a0a").pack()
        
        # Subtitle
        tk.Label(content, text="━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━", 
                font=('Segoe UI', 10), fg="#333333", bg="#0a0a0a").pack(pady=20)
        tk.Label(content, text="Select Your Role", 
                font=('Segoe UI', 14), fg="#b0b0b0", bg="#0a0a0a").pack(pady=10)
        
        # Buttons with dark theme
        btn_frame = tk.Frame(content, bg="#0a0a0a")
        btn_frame.pack(pady=30)
        
        # Field Reporter Button
        btn1 = tk.Button(btn_frame, text="📱 FIELD REPORTER", 
                        command=self.show_reporter_mode,
                        font=('Segoe UI', 14, 'bold'), bg="#1e1e1e", fg="#ffffff",
                        relief=tk.FLAT, padx=50, pady=20, cursor="hand2",
                        activebackground="#2a2a2a", activeforeground="#ffffff",
                        bd=2, highlightthickness=2, highlightbackground="#ff0000",
                        highlightcolor="#ff0000")
        btn1.pack(pady=10, fill=tk.X)
        btn1.bind("<Enter>", lambda e: btn1.config(bg="#2a2a2a", highlightbackground="#ff0000"))
        btn1.bind("<Leave>", lambda e: btn1.config(bg="#1e1e1e", highlightbackground="#ff0000"))
        
        # Command Center Button
        btn2 = tk.Button(btn_frame, text="🎯 COMMAND CENTER", 
                        command=self.show_admin_mode,
                        font=('Segoe UI', 14, 'bold'), bg="#ff0000", fg="#ffffff",
                        relief=tk.FLAT, padx=50, pady=20, cursor="hand2",
                        activebackground="#cc0000", activeforeground="#ffffff")
        btn2.pack(pady=10, fill=tk.X)
        btn2.bind("<Enter>", lambda e: btn2.config(bg="#cc0000"))
        btn2.bind("<Leave>", lambda e: btn2.config(bg="#ff0000"))
        
        # Footer
        tk.Label(content, text="Real-time Emergency Management & Response", 
                font=('Segoe UI', 9), fg="#555555", bg="#0a0a0a").pack(pady=(40, 10))

    def show_reporter_mode(self):
        self.clear_frame()
        self.current_view = ReporterGUI(self.container, self)

    def show_admin_mode(self):
        self.clear_frame()
        self.current_view = AdminGUI(self.container, self)

    def clear_frame(self):
        for widget in self.container.winfo_children():
            widget.destroy()
        self.container.update_idletasks()

    def send_command(self, cmd, callback=None):
        def run():
            if not self.process: return
            try:
                self.process.stdin.write(cmd + "\n")
                self.process.stdin.flush()
                
                lines = []
                while True:
                    line = self.process.stdout.readline()
                    if not line or line.strip() == "---END---": break
                    lines.append(line.strip())
                
                resp = "\n".join(lines)
                if callback:
                    self.root.after(0, callback, resp)
            except Exception as e:
                print(f"Error: {e}")
                
        threading.Thread(target=run, daemon=True).start()

    def send_command_sync(self, cmd):
        if not self.process: return ""
        try:
            self.process.stdin.write(cmd + "\n")
            self.process.stdin.flush()
            lines = []
            while True:
                line = self.process.stdout.readline()
                if not line or line.strip() == "---END---": break
                lines.append(line.strip())
            return "\n".join(lines)
        except: return ""
        
    def parse_response(self, text):
        data = {}
        for line in text.split('\n'):
            if '=' in line:
                k, v = line.split('=', 1)
                data[k.strip()] = v.strip()
        return data

    def on_close(self):
        self.running = False
        if self.process: self.process.kill()
        self.root.destroy()


class ReporterGUI(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, bg="#0a0a0a")
        self.app = app
        self.pack(fill=tk.BOTH, expand=True)
        
        # Header with dark theme
        header = tk.Frame(self, bg="#1a1a1a", height=70)
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        
        tk.Button(header, text="◀ Back", command=app.show_login,
                 font=('Segoe UI', 10), bg="#1e1e1e", fg="#ffffff",
                 relief=tk.FLAT, padx=20, pady=8, cursor="hand2").pack(side=tk.LEFT, padx=15, pady=15)
        
        tk.Label(header, text="📱 FIELD REPORT SUBMISSION", 
                font=('Segoe UI', 18, 'bold'), fg="#ff0000", bg="#1a1a1a").pack(pady=20)
        
        # Scrollable container
        canvas = tk.Canvas(self, bg="#0a0a0a", highlightthickness=0)
        scrollbar = tk.Scrollbar(self, orient=tk.VERTICAL, command=canvas.yview)
        
        scrollable_frame = tk.Frame(canvas, bg="#0a0a0a")
        
        # Create window with proper width binding
        canvas_window = canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        
        def configure_scroll(event):
            canvas.configure(scrollregion=canvas.bbox("all"))
        
        def configure_canvas_width(event):
            canvas.itemconfig(canvas_window, width=event.width)
        
        scrollable_frame.bind("<Configure>", configure_scroll)
        canvas.bind("<Configure>", configure_canvas_width)
        
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Form Container with dark card
        self.main_frame = tk.Frame(scrollable_frame, bg="#1e1e1e", relief=tk.SOLID, bd=1, highlightthickness=1, highlightbackground="#333333")
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=50, pady=20)
        
        # Enable mousewheel scrolling
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
        self.bind("<Enter>", lambda e: canvas.bind_all("<MouseWheel>", _on_mousewheel))
        self.bind("<Leave>", lambda e: canvas.unbind_all("<MouseWheel>"))
        
        self.init_form()

    def init_form(self):
        # Inner padding
        form = tk.Frame(self.main_frame, bg="#1e1e1e", padx=30, pady=30)
        form.pack(fill=tk.BOTH, expand=True)
        
        # 1. Location
        tk.Label(form, text="📍 GPS Coordinates (Lat, Lon):", 
                font=('Segoe UI', 11, 'bold'), fg="#ffffff", bg="#1e1e1e").pack(anchor=tk.W, pady=(10, 5))
        
        self.coord_var = tk.StringVar()
        coord_entry = tk.Entry(form, textvariable=self.coord_var, width=40,
                              font=('Segoe UI', 11), bg="#2a2a2a", fg="#ffffff",
                              relief=tk.FLAT, bd=0, insertbackground="#ff0000")
        coord_entry.pack(fill=tk.X, pady=5, ipady=8)
        
        tk.Button(form, text="📡 Use My Location", command=self.sim_gps,
                 font=('Segoe UI', 9), bg="#333333", fg="#ffffff",
                 relief=tk.FLAT, padx=15, pady=5, cursor="hand2").pack(anchor=tk.E, pady=(5, 15))
        
        # 2. Disaster Type
        tk.Label(form, text="🌍 Disaster Type:", 
                font=('Segoe UI', 11, 'bold'), fg="#ffffff", bg="#1e1e1e").pack(anchor=tk.W, pady=(10, 5))
        
        self.disaster_var = tk.StringVar(value="Earthquake")
        disaster_frame = tk.Frame(form, bg="#2a2a2a")
        disaster_frame.pack(fill=tk.X, pady=5)
        
        for disaster in ["Earthquake", "Flood", "Fire"]:
            tk.Radiobutton(disaster_frame, text=disaster, variable=self.disaster_var, value=disaster,
                          font=('Segoe UI', 10), bg="#2a2a2a", fg="#ffffff",
                          selectcolor="#ff0000", activebackground="#2a2a2a",
                          activeforeground="#ffffff").pack(side=tk.LEFT, padx=20, pady=10)
        
        # 3. Stats
        stats_row = tk.Frame(form, bg="#1e1e1e")
        stats_row.pack(fill=tk.X, pady=(20, 10))
        
        # Population
        pop_frame = tk.Frame(stats_row, bg="#1e1e1e")
        pop_frame.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(0, 10))
        tk.Label(pop_frame, text="👥 Population Affected:", 
                font=('Segoe UI', 10), fg="#b0b0b0", bg="#1e1e1e").pack(anchor=tk.W)
        self.pop_var = tk.StringVar()
        tk.Entry(pop_frame, textvariable=self.pop_var, width=15,
                font=('Segoe UI', 11), bg="#2a2a2a", fg="#ffffff",
                relief=tk.FLAT, insertbackground="#ff0000").pack(fill=tk.X, ipady=6)
        
        # Injured
        inj_frame = tk.Frame(stats_row, bg="#1e1e1e")
        inj_frame.pack(side=tk.LEFT, expand=True, fill=tk.X)
        tk.Label(inj_frame, text="🏥 Injured Count:", 
                font=('Segoe UI', 10), fg="#b0b0b0", bg="#1e1e1e").pack(anchor=tk.W)
        self.inj_var = tk.StringVar()
        tk.Entry(inj_frame, textvariable=self.inj_var, width=15,
                font=('Segoe UI', 11), bg="#2a2a2a", fg="#ffffff",
                relief=tk.FLAT, insertbackground="#ff0000").pack(fill=tk.X, ipady=6)
        
        # 4. Resource Criticality
        tk.Label(form, text="⚠️ Resource Shortage Level (0-10):", 
                font=('Segoe UI', 11, 'bold'), fg="#ffffff", bg="#1e1e1e").pack(anchor=tk.W, pady=(25, 15))
        
        self.sliders = {}
        for name, emoji, color in [("Food", "🍞", "#ff6600"), ("Medical", "💊", "#ff0000"), ("Water", "💧", "#00aaff")]:
            slider_frame = tk.Frame(form, bg="#1e1e1e")
            slider_frame.pack(fill=tk.X, pady=8)
            
            tk.Label(slider_frame, text=f"{emoji} {name}", 
                    font=('Segoe UI', 10, 'bold'), fg="#ffffff", bg="#1e1e1e", width=12, anchor=tk.W).pack(side=tk.LEFT)
            
            v = tk.IntVar()
            self.sliders[name.lower()] = v
            
            scale = tk.Scale(slider_frame, from_=0, to=10, orient=tk.HORIZONTAL, variable=v,
                           showvalue=0, bg="#2a2a2a", fg=color, troughcolor="#0a0a0a",
                           highlightthickness=0, bd=0, sliderrelief=tk.FLAT,
                           activebackground=color)
            scale.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=10)
            
            value_label = tk.Label(slider_frame, textvariable=v, 
                                  font=('Segoe UI', 12, 'bold'), fg=color, bg="#1e1e1e", width=3)
            value_label.pack(side=tk.LEFT)
        
        # Submit Button
        tk.Button(form, text="🚀 TRANSMIT EMERGENCY REPORT", command=self.submit,
                 font=('Segoe UI', 13, 'bold'), bg="#ff0000", fg="#ffffff",
                 relief=tk.FLAT, padx=30, pady=15, cursor="hand2",
                 activebackground="#cc0000").pack(fill=tk.X, pady=(30, 10))

    def sim_gps(self):
        self.coord_var.set("34.125, 71.884")

    def submit(self):
        coords = self.coord_var.get().replace(" ", "_").replace(",", "")
        if not coords:
            messagebox.showerror("Error", "Coordinates required")
            return
            
        try:
            pop = int(self.pop_var.get())
            inj = int(self.inj_var.get())
            f = self.sliders['food'].get()
            m = self.sliders['medical'].get()
            w = self.sliders['water'].get()
        except:
            messagebox.showerror("Error", "Invalid numeric data")
            return
            
        loc_id = f"LOC_{coords}"
        cmd = f"ADD {loc_id} {self.disaster_var.get()} {pop} {inj} {f} {m} {w}"
        
        self.app.send_command(cmd, self.on_response)

    def on_response(self, text):
        data = self.app.parse_response(text)
        if data.get("STATUS") == "OK":
            sev = data.get("SEVERITY_LABEL", "UNKNOWN")
            msg = f"Report Received.\nSystem Severity Assessment: {sev}\n\nStandby for confirmation."
            messagebox.showinfo("Transmission Success", msg)
            self.clear_inputs()
        else:
            messagebox.showerror("Transmission Failed", data.get("MSG", "Unknown Error"))
            
    def clear_inputs(self):
        self.coord_var.set("")
        self.pop_var.set("")
        self.inj_var.set("")
        for v in self.sliders.values(): v.set(0)


class AdminGUI(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, bg="#f5f7fa")
        self.app = app
        self.inventory = {"food": 500, "medical": 2000, "water": 1000}
        self.selected_loc_id = None
        
        self.pack(fill=tk.BOTH, expand=True)
        self.running = True
        
        # Modern Header with Dark Theme
        header = tk.Frame(self, bg="#0a0a0a", height=70)
        header.pack(fill=tk.X, side=tk.TOP)
        header.pack_propagate(False)
        
        # Header content
        header_left = tk.Frame(header, bg="#0a0a0a")
        header_left.pack(side=tk.LEFT, padx=20, pady=15)
        
        tk.Label(header_left, text="🎯", font=('Segoe UI', 24), bg="#0a0a0a").pack(side=tk.LEFT, padx=(0, 10))
        tk.Label(header_left, text="COMMAND CENTER", font=('Segoe UI', 18, 'bold'), fg="#ff0000", bg="#0a0a0a").pack(side=tk.LEFT)
        
        # Header buttons
        header_right = tk.Frame(header, bg="#0a0a0a")
        header_right.pack(side=tk.RIGHT, padx=20)
        
        tk.Button(header_right, text="📊 Generate Report", command=self.gen_report,
                 font=('Segoe UI', 10, 'bold'), bg="#00ff00", fg="#000000", 
                 relief=tk.FLAT, padx=20, pady=8, cursor="hand2",
                 activebackground="#00cc00").pack(side=tk.LEFT, padx=5)
        
        tk.Button(header_right, text="🚪 Log Out", command=self.exit_mode,
                 font=('Segoe UI', 10), bg="#ff0000", fg="#ffffff", 
                 relief=tk.FLAT, padx=15, pady=8, cursor="hand2",
                 activebackground="#cc0000").pack(side=tk.LEFT, padx=5)
        
        # Main content area with better height management
        content = tk.Frame(self, bg="#0a0a0a")
        content.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        # Left panel - Pending Emergencies (make it taller)
        left_panel = tk.Frame(content, bg="#1e1e1e", relief=tk.SOLID, bd=1, highlightthickness=1, highlightbackground="#ff0000")
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 8))
        
        # Left panel header
        left_header = tk.Frame(left_panel, bg="#ff0000", height=50)
        left_header.pack(fill=tk.X)
        left_header.pack_propagate(False)
        
        tk.Label(left_header, text="🚨 PENDING EMERGENCIES", 
                font=('Segoe UI', 13, 'bold'), fg="#ffffff", bg="#ff0000").pack(pady=12, padx=15)
        
        # Treeview with dark styling
        tree_frame = tk.Frame(left_panel, bg="#1e1e1e")
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        style = ttk.Style()
        style.configure("Custom.Treeview", 
                       background="#2a2a2a",
                       foreground="#ffffff",
                       rowheight=35,
                       fieldbackground="#2a2a2a",
                       font=('Segoe UI', 10))
        style.configure("Custom.Treeview.Heading",
                       background="#ff0000",
                       foreground="#ffffff",
                       font=('Segoe UI', 10, 'bold'))
        style.map('Custom.Treeview', background=[('selected', '#ff0000')], foreground=[('selected', '#ffffff')])
        
        cols = ("loc", "type", "sev")
        self.tree = ttk.Treeview(tree_frame, columns=cols, show="headings", 
                                selectmode="browse", style="Custom.Treeview", height=12)
        self.tree.heading("loc", text="📍 Location ID")
        self.tree.heading("type", text="🌍 Disaster")
        self.tree.heading("sev", text="⚠️ Severity")
        self.tree.column("loc", width=180)
        self.tree.column("type", width=100)
        self.tree.column("sev", width=100)
        
        sb = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=sb.set)
        
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        sb.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.tree.bind("<<TreeviewSelect>>", self.on_select)
        
        # Right panel - Scrollable for details and controls
        right_outer = tk.Frame(content, bg="#0a0a0a")
        right_outer.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(8, 0))
        
        # Add canvas for scrolling right panel
        right_canvas = tk.Canvas(right_outer, bg="#0a0a0a", highlightthickness=0)
        right_scrollbar = tk.Scrollbar(right_outer, orient=tk.VERTICAL, command=right_canvas.yview)
        
        right_panel = tk.Frame(right_canvas, bg="#0a0a0a")
        
        # Create window with proper width binding
        right_canvas_window = right_canvas.create_window((0, 0), window=right_panel, anchor="nw")
        
        def configure_right_scroll(event):
            right_canvas.configure(scrollregion=right_canvas.bbox("all"))
        
        def configure_right_canvas_width(event):
            right_canvas.itemconfig(right_canvas_window, width=event.width)
        
        right_panel.bind("<Configure>", configure_right_scroll)
        right_canvas.bind("<Configure>", configure_right_canvas_width)
        
        right_canvas.configure(yscrollcommand=right_scrollbar.set)
        
        right_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        right_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Enable mousewheel scrolling for right panel
        def _on_right_mousewheel(event):
            right_canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
        right_outer.bind("<Enter>", lambda e: right_canvas.bind_all("<MouseWheel>", _on_right_mousewheel))
        right_outer.bind("<Leave>", lambda e: right_canvas.unbind_all("<MouseWheel>"))
        
        # Details Card
        details_card = tk.Frame(right_panel, bg="#1e1e1e", relief=tk.SOLID, bd=1, highlightthickness=1, highlightbackground="#333333")
        details_card.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Details header
        details_header = tk.Frame(details_card, bg="#ff0000", height=50)
        details_header.pack(fill=tk.X)
        details_header.pack_propagate(False)
        
        tk.Label(details_header, text="📋 INCIDENT DETAILS", 
                font=('Segoe UI', 13, 'bold'), fg="#ffffff", bg="#ff0000").pack(pady=12, padx=15)
        
        # Details content - with wraplength for proper display
        self.detail_lbl = tk.Label(details_card, text="Select an emergency from the list\nto view detailed information", 
                                   font=('Segoe UI', 10), justify=tk.LEFT, anchor=tk.NW, 
                                   bg="#1e1e1e", fg="#b0b0b0", padx=20, pady=20, wraplength=350)
        self.detail_lbl.pack(fill=tk.BOTH, expand=True)
        
        # Stockpile Card
        stockpile_card = tk.Frame(right_panel, bg="#1e1e1e", relief=tk.SOLID, bd=1, highlightthickness=1, highlightbackground="#333333")
        stockpile_card.pack(fill=tk.X, pady=(0, 10))
        
        stockpile_header = tk.Frame(stockpile_card, bg="#ff6600", height=45)
        stockpile_header.pack(fill=tk.X)
        stockpile_header.pack_propagate(False)
        
        tk.Label(stockpile_header, text="📦 RESOURCE STOCKPILE", 
                font=('Segoe UI', 12, 'bold'), fg="#ffffff", bg="#ff6600").pack(pady=10, padx=15)
        
        # Stockpile content
        stockpile_content = tk.Frame(stockpile_card, bg="#1e1e1e", padx=15, pady=15)
        stockpile_content.pack(fill=tk.X)
        
        self.inv_lbls = {}
        inv_row = tk.Frame(stockpile_content, bg="#1e1e1e")
        inv_row.pack(fill=tk.X)
        
        resources = [("🍞 Food", "food", "#ff6600"), ("💊 Medical", "medical", "#ff0000"), ("💧 Water", "water", "#00aaff")]
        for label, key, color in resources:
            inv_item = tk.Frame(inv_row, bg="#1e1e1e")
            inv_item.pack(side=tk.LEFT, expand=True, padx=5)
            
            tk.Label(inv_item, text=label, font=('Segoe UI', 9), 
                    fg="#b0b0b0", bg="#1e1e1e").pack()
            
            value_label = tk.Label(inv_item, text="0", font=('Segoe UI', 18, 'bold'), 
                                  fg=color, bg="#1e1e1e")
            value_label.pack()
            self.inv_lbls[key] = value_label
        
        tk.Button(stockpile_content, text="➕ Replenish Stock", command=self.replenish,
                 font=('Segoe UI', 9), bg="#00ff00", fg="#000000", 
                 relief=tk.FLAT, padx=15, pady=6, cursor="hand2",
                 activebackground="#00cc00").pack(pady=(10, 0))
        
        # Deployment Card
        deploy_card = tk.Frame(right_panel, bg="#1e1e1e", relief=tk.SOLID, bd=1, highlightthickness=1, highlightbackground="#333333")
        deploy_card.pack(fill=tk.X)
        
        deploy_header = tk.Frame(deploy_card, bg="#ff0000", height=45)
        deploy_header.pack(fill=tk.X)
        deploy_header.pack_propagate(False)
        
        tk.Label(deploy_header, text="🚁 RESOURCE DEPLOYMENT", 
                font=('Segoe UI', 12, 'bold'), fg="#ffffff", bg="#ff0000").pack(pady=10, padx=15)
        
        # Deployment content
        deploy_content = tk.Frame(deploy_card, bg="#1e1e1e", padx=15, pady=15)
        deploy_content.pack(fill=tk.X)
        
        self.d_vars = {}
        for label, key in [("🍞 Food", "food"), ("💊 Medical", "medical"), ("💧 Water", "water")]:
            row = tk.Frame(deploy_content, bg="#1e1e1e")
            row.pack(fill=tk.X, pady=5)
            
            tk.Label(row, text=label, font=('Segoe UI', 10), 
                    fg="#ffffff", bg="#1e1e1e", width=15, anchor=tk.W).pack(side=tk.LEFT)
            
            v = tk.StringVar(value="50")
            self.d_vars[key] = v
            
            spinbox_frame = tk.Frame(row, bg="#2a2a2a")
            spinbox_frame.pack(side=tk.RIGHT)
            
            spinbox = tk.Entry(spinbox_frame, textvariable=v, width=8,
                             font=('Segoe UI', 10), bg="#2a2a2a", fg="#ffffff",
                             relief=tk.FLAT, justify=tk.CENTER, insertbackground="#ff0000")
            spinbox.pack(padx=5, pady=2)
        
        self.btn_dispatch = tk.Button(deploy_content, text="🚀 DISPATCH RELIEF PACKAGE", 
                                      command=self.dispatch, state=tk.DISABLED,
                                      font=('Segoe UI', 11, 'bold'), bg="#ff0000", fg="#ffffff",
                                      relief=tk.FLAT, padx=20, pady=12, cursor="hand2",
                                      activebackground="#cc0000",
                                      disabledforeground="#666666")
        self.btn_dispatch.pack(fill=tk.X, pady=(15, 10))
        
        # Generate Report Button (prominent)
        tk.Button(deploy_content, text="📊 GENERATE FULL REPORT", 
                 command=self.gen_report,
                 font=('Segoe UI', 11, 'bold'), bg="#00ff00", fg="#000000",
                 relief=tk.FLAT, padx=20, pady=12, cursor="hand2",
                 activebackground="#00cc00").pack(fill=tk.X, pady=(5, 0))

        self.update_inv_ui()
        threading.Thread(target=self.poll_list, daemon=True).start()

    def update_inv_ui(self):
        for k, v in self.inventory.items():
            self.inv_lbls[k].config(text=str(v))

    def replenish(self):
        for k in self.inventory: self.inventory[k] += 500
        self.update_inv_ui()
        messagebox.showinfo("Supply", "Added 500 units to all resources.")

    def poll_list(self):
        while self.running:
            try:
                if not self.winfo_exists(): break
            except: break
            
            resp = self.app.send_command_sync("VIEW_PENDING_LIST")
            self.app.root.after(0, self.update_list, resp)
            time.sleep(3)

    def update_list(self, text):
        sel = self.tree.selection()
        sel_id = self.tree.item(sel[0])['values'][0] if sel else None
        
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        lines = text.strip().split('\n')
        for line in lines:
            if line.startswith("ITEM="):
                parts = line[5:].split('|')
                if len(parts) == 3:
                    self.tree.insert("", tk.END, values=parts)
                    
        if sel_id:
            for item in self.tree.get_children():
                if self.tree.item(item)['values'][0] == sel_id:
                    self.tree.selection_set(item)
                    break

    def on_select(self, event):
        sel = self.tree.selection()
        if not sel:
            self.selected_loc_id = None
            self.btn_dispatch.config(state=tk.DISABLED)
            self.detail_lbl.config(text="Select an incident...")
            return
            
        loc_id = self.tree.item(sel[0])['values'][0]
        self.selected_loc_id = loc_id
        self.btn_dispatch.config(state=tk.NORMAL)
        
        self.app.send_command(f"VIEW_DETAILS {loc_id}", self.show_details)

    def show_details(self, text):
        try:
            data = self.app.parse_response(text)
            
            # Debug: print received data
            print(f"Received details: {data}")
            
            if data.get("STATUS") != "OK":
                self.detail_lbl.config(text="❌ Error fetching details\nPlease try again", 
                                      fg="#ff0000", font=('Segoe UI', 11), bg="#1e1e1e", wraplength=350)
                return
            
            # Format details beautifully with safe formatting
            pop = data.get('POP', '0')
            try:
                pop_formatted = f"{int(pop):,}"
            except:
                pop_formatted = pop
            
            info = f"📍 LOCATION: {data.get('LOC', 'N/A')}\n"
            info += f"🌍 DISASTER: {data.get('DISASTER', 'N/A')}\n"
            info += f"⚠️  SEVERITY: {data.get('SEVERITY_LABEL', 'N/A')}\n"
            info += f"🕒 REPORTED: {data.get('TIME', 'N/A')}\n\n"
            info += f"━━━━━━━━━━━━━━━━━━━━━━━━\n"
            info += f"IMPACT ASSESSMENT\n"
            info += f"━━━━━━━━━━━━━━━━━━━━━━━━\n"
            info += f"👥 Population: {pop_formatted}\n"
            info += f"🏥 Injured: {data.get('INJ', '0')}\n\n"
            info += f"━━━━━━━━━━━━━━━━━━━━━━━━\n"
            info += f"RESOURCE NEEDS (0-10)\n"
            info += f"━━━━━━━━━━━━━━━━━━━━━━━━\n"
            info += f"🍞 Food:    {data.get('FOOD', '0')}/10\n"
            info += f"💊 Medical: {data.get('MED', '0')}/10\n"
            info += f"💧 Water:   {data.get('WATER', '0')}/10"
                   
            self.detail_lbl.config(text=info, font=('Segoe UI', 10), fg="#ffffff", bg="#1e1e1e", justify=tk.LEFT, anchor=tk.NW, wraplength=350)
            print(f"Details updated successfully")
        except Exception as e:
            print(f"Error in show_details: {e}")
            self.detail_lbl.config(text=f"❌ Error displaying details:\n{str(e)}", 
                                  fg="#ff0000", font=('Segoe UI', 11), bg="#1e1e1e", wraplength=350)

    def dispatch(self):
        if not self.selected_loc_id: return
        
        try:
            f = int(self.d_vars['food'].get())
            m = int(self.d_vars['medical'].get())
            w = int(self.d_vars['water'].get())
        except: return
        
        if f > self.inventory['food'] or m > self.inventory['medical'] or w > self.inventory['water']:
            messagebox.showerror("Error", "Insufficient Inventory")
            return
            
        if messagebox.askyesno("Confirm", f"Dispatch relief to {self.selected_loc_id}?"):
            self.inventory['food'] -= f
            self.inventory['medical'] -= m
            self.inventory['water'] -= w
            self.update_inv_ui()
            
            self.app.send_command(f"DISPATCH {f} {m} {w}", self.on_dispatch_result)

    def on_dispatch_result(self, text):
         messagebox.showinfo("Result", "Dispatch sequence initiated.")

    def gen_report(self):
        # Show loading indicator with dark theme
        loading = tk.Toplevel(self.app.root)
        loading.title("Generating Reports")
        loading.geometry("400x200")
        loading.configure(bg="#1a1a1a")
        loading.transient(self.app.root)
        loading.grab_set()
        
        # Center the loading window
        loading.update_idletasks()
        x = (loading.winfo_screenwidth() // 2) - (400 // 2)
        y = (loading.winfo_screenheight() // 2) - (200 // 2)
        loading.geometry(f'400x200+{x}+{y}')
        
        # Loading content
        tk.Label(loading, text="📊", font=('Segoe UI', 40), bg="#1a1a1a").pack(pady=20)
        tk.Label(loading, text="Generating Reports...", 
                font=('Segoe UI', 14, 'bold'), fg="#ff0000", bg="#1a1a1a").pack()
        progress_label = tk.Label(loading, text="Please wait", 
                                 font=('Segoe UI', 10), fg="#b0b0b0", bg="#1a1a1a")
        progress_label.pack(pady=10)
        
        # Animate dots
        dots = [0]
        def animate():
            dots[0] = (dots[0] + 1) % 4
            progress_label.config(text="Please wait" + "." * dots[0])
            if loading.winfo_exists():
                loading.after(500, animate)
        animate()
        
        # Generate reports in background
        def generate():
            # Call backend to generate report files
            self.app.send_command_sync("GENERATE_REPORTS")
            
            # Close loading window
            loading.destroy()
            
            # Show dashboard
            ReportDashboard(self.app.root, self.app)
        
        # Start generation in thread
        threading.Thread(target=generate, daemon=True).start()
    
    def exit_mode(self):
        self.running = False
        self.destroy()
        self.app.show_login()


class ReportDashboard(tk.Toplevel):
    """Ultra-Professional Analytics Dashboard with Visual Cards"""
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        self.title("Emergency Analytics Dashboard")
        self.geometry("1400x900")
        self.configure(bg="#0a0a0a")
        
        self.transient(parent)
        self.grab_set()
        
        self.create_ui()
        self.load_data()
    
    def create_ui(self):
        # Dark themed header
        header = tk.Frame(self, bg="#1a1a1a", height=80)
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        
        header_content = tk.Frame(header, bg="#1a1a1a")
        header_content.pack(expand=True, fill=tk.BOTH)
        
        # Icon + Title
        title_frame = tk.Frame(header_content, bg="#1a1a1a")
        title_frame.pack(pady=15)
        
        tk.Label(title_frame, text="📊", font=('Segoe UI', 28), bg="#1a1a1a").pack(side=tk.LEFT, padx=10)
        tk.Label(title_frame, text="EMERGENCY OPERATIONS DASHBOARD", 
                font=('Segoe UI', 20, 'bold'), fg="#ff0000", bg="#1a1a1a").pack(side=tk.LEFT)
        
        # Close button
        close_btn = tk.Button(header, text="✕", command=self.destroy, 
                 font=('Segoe UI', 16, 'bold'), bg="#ff0000", fg="white", 
                 relief=tk.FLAT, width=3, height=1, cursor="hand2",
                 activebackground="#cc0000", activeforeground="white")
        close_btn.place(relx=0.98, rely=0.5, anchor=tk.E)
        
        # Notebook with dark theme styling
        style = ttk.Style()
        style.theme_use('default')
        style.configure('Dark.TNotebook', background="#0a0a0a", borderwidth=0)
        style.configure('Dark.TNotebook.Tab', 
                       background="#2a2a2a", 
                       foreground="#b0b0b0",
                       padding=[20, 10],
                       font=('Segoe UI', 11, 'bold'))
        style.map('Dark.TNotebook.Tab',
                 background=[('selected', '#ff0000')],
                 foreground=[('selected', '#ffffff')])
        
        notebook = ttk.Notebook(self, style='Dark.TNotebook')
        notebook.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        # Tab 1: Pending Emergencies (Card View)
        tab1 = tk.Frame(notebook, bg="#0a0a0a")
        notebook.add(tab1, text="🚨 Pending Emergencies")
        self.pending_container = tab1
        
        # Tab 2: Dispatch History (Card View)
        tab2 = tk.Frame(notebook, bg="#0a0a0a")
        notebook.add(tab2, text="📦 Dispatch History")
        self.history_container = tab2
        
        # Tab 3: Statistics (Visual Charts)
        tab3 = tk.Frame(notebook, bg="#0a0a0a")
        notebook.add(tab3, text="📈 Statistics")
        self.stats_container = tab3
    
    def load_data(self):
        # Get pending emergencies
        resp = self.app.send_command_sync("VIEW_PENDING_LIST")
        self.display_pending_cards(resp)
        
        # Load dispatch history
        self.display_history_cards()
        
        # Display statistics
        self.display_statistics(resp)
    
    def display_pending_cards(self, response):
        # Canvas for scrolling with dark theme
        canvas = tk.Canvas(self.pending_container, bg="#0a0a0a", highlightthickness=0)
        scrollbar = tk.Scrollbar(self.pending_container, orient=tk.VERTICAL, command=canvas.yview)
        scrollable = tk.Frame(canvas, bg="#0a0a0a")
        
        # Proper width binding
        canvas_window = canvas.create_window((0, 0), window=scrollable, anchor="nw")
        
        def configure_scroll(event):
            canvas.configure(scrollregion=canvas.bbox("all"))
        
        def configure_canvas_width(event):
            canvas.itemconfig(canvas_window, width=event.width)
        
        scrollable.bind("<Configure>", configure_scroll)
        canvas.bind("<Configure>", configure_canvas_width)
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Enable mousewheel
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
        self.pending_container.bind("<Enter>", lambda e: canvas.bind_all("<MouseWheel>", _on_mousewheel))
        self.pending_container.bind("<Leave>", lambda e: canvas.unbind_all("<MouseWheel>"))
        
        # Parse emergencies
        lines = response.strip().split('\n')
        emergencies = []
        for line in lines:
            if line.startswith("ITEM="):
                parts = line[5:].split('|')
                if len(parts) == 3:
                    emergencies.append({'location': parts[0], 'disaster': parts[1], 'severity': parts[2]})
        
        if not emergencies:
            empty_frame = tk.Frame(scrollable, bg="#1e1e1e", relief=tk.SOLID, bd=1)
            empty_frame.pack(fill=tk.X, padx=20, pady=50)
            tk.Label(empty_frame, text="✓ No Pending Emergencies", 
                    font=('Segoe UI', 18, 'bold'), fg="#00ff00", bg="#1e1e1e", pady=50).pack()
        else:
            # Header
            header = tk.Frame(scrollable, bg="#0a0a0a")
            header.pack(fill=tk.X, padx=20, pady=(10, 20))
            tk.Label(header, text=f"Total: {len(emergencies)} Emergencies", 
                    font=('Segoe UI', 14, 'bold'), fg="#ff0000", bg="#0a0a0a").pack(anchor=tk.W)
            
            # Create cards
            for idx, emergency in enumerate(emergencies, 1):
                self.create_emergency_card(scrollable, emergency, idx)
    
    def create_emergency_card(self, parent, data, index):
        # Card with dark theme
        shadow = tk.Frame(parent, bg="#333333", height=2)
        shadow.pack(fill=tk.X, padx=23, pady=(8, 0))
        
        card = tk.Frame(parent, bg="#1e1e1e", relief=tk.SOLID, bd=1, highlightthickness=1, highlightbackground="#333333")
        card.pack(fill=tk.X, padx=20, pady=(0, 15))
        
        # Severity colors
        severity_colors = {
            'CRITICAL': '#ff0000',
            'HIGH': '#ff6600',
            'MODERATE': '#ffaa00',
            'LOW': '#00ff00'
        }
        color = severity_colors.get(data['severity'], '#ffffff')
        
        # Left colored bar
        bar = tk.Frame(card, bg=color, width=6)
        bar.pack(side=tk.LEFT, fill=tk.Y)
        
        # Content
        content = tk.Frame(card, bg="#1e1e1e", padx=25, pady=20)
        content.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Header row
        header_row = tk.Frame(content, bg="#1e1e1e")
        header_row.pack(fill=tk.X, pady=(0, 12))
        
        tk.Label(header_row, text=f"#{index}", 
                font=('Segoe UI', 16, 'bold'), fg=color, bg="#1e1e1e").pack(side=tk.LEFT, padx=(0, 10))
        
        tk.Label(header_row, text=data['location'], 
                font=('Segoe UI', 15, 'bold'), fg="#ffffff", bg="#1e1e1e").pack(side=tk.LEFT)
        
        # Severity badge
        badge = tk.Frame(header_row, bg=color, padx=12, pady=5)
        badge.pack(side=tk.RIGHT)
        tk.Label(badge, text=data['severity'], font=('Segoe UI', 10, 'bold'), 
                fg="#000000", bg=color).pack()
        
        # Details
        details = tk.Frame(content, bg="#1e1e1e")
        details.pack(fill=tk.X)
        
        tk.Label(details, text="🌍 Disaster:", font=('Segoe UI', 11), 
                fg="#b0b0b0", bg="#1e1e1e").pack(side=tk.LEFT, padx=(0, 5))
        tk.Label(details, text=data['disaster'], font=('Segoe UI', 11, 'bold'), 
                fg="#ffffff", bg="#1e1e1e").pack(side=tk.LEFT)
    
    def display_history_cards(self):
        # Canvas for scrolling with dark theme
        canvas = tk.Canvas(self.history_container, bg="#0a0a0a", highlightthickness=0)
        scrollbar = tk.Scrollbar(self.history_container, orient=tk.VERTICAL, command=canvas.yview)
        scrollable = tk.Frame(canvas, bg="#0a0a0a")
        
        # Proper width binding
        canvas_window = canvas.create_window((0, 0), window=scrollable, anchor="nw")
        
        def configure_scroll(event):
            canvas.configure(scrollregion=canvas.bbox("all"))
        
        def configure_canvas_width(event):
            canvas.itemconfig(canvas_window, width=event.width)
        
        scrollable.bind("<Configure>", configure_scroll)
        canvas.bind("<Configure>", configure_canvas_width)
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Enable mousewheel
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
        self.history_container.bind("<Enter>", lambda e: canvas.bind_all("<MouseWheel>", _on_mousewheel))
        self.history_container.bind("<Leave>", lambda e: canvas.unbind_all("<MouseWheel>"))
        
        # Read history file
        try:
            with open("Dispatch_History_Report.txt", "r") as f:
                lines = f.readlines()
            
            if not lines:
                empty_frame = tk.Frame(scrollable, bg="#1e1e1e", relief=tk.SOLID, bd=1)
                empty_frame.pack(fill=tk.X, padx=20, pady=50)
                tk.Label(empty_frame, text="📭 No Dispatch History", 
                        font=('Segoe UI', 18), fg="#b0b0b0", bg="#1e1e1e", pady=50).pack()
            else:
                # Header
                header = tk.Frame(scrollable, bg="#0a0a0a")
                header.pack(fill=tk.X, padx=20, pady=(10, 20))
                tk.Label(header, text=f"Total: {len(lines)} Operations", 
                        font=('Segoe UI', 14, 'bold'), fg="#ff0000", bg="#0a0a0a").pack(anchor=tk.W)
                
                for idx, line in enumerate(lines, 1):
                    parts = line.strip().split()
                    if len(parts) >= 4:
                        self.create_history_card(scrollable, {
                            'location': parts[0],
                            'disaster': parts[1],
                            'severity': parts[2],
                            'status': parts[3],
                            'time': " ".join(parts[4:]) if len(parts) > 4 else "N/A"
                        }, idx)
        except FileNotFoundError:
            empty_frame = tk.Frame(scrollable, bg="#1e1e1e", relief=tk.SOLID, bd=1)
            empty_frame.pack(fill=tk.X, padx=20, pady=50)
            tk.Label(empty_frame, text="📭 No Dispatch History Available", 
                    font=('Segoe UI', 18), fg="#b0b0b0", bg="#1e1e1e", pady=50).pack()
    
    def create_history_card(self, parent, data, index):
        card = tk.Frame(parent, bg="#1e1e1e", relief=tk.SOLID, bd=1, highlightthickness=1, highlightbackground="#333333")
        card.pack(fill=tk.X, padx=20, pady=8)
        
        content = tk.Frame(card, bg="#1e1e1e", padx=20, pady=15)
        content.pack(fill=tk.BOTH, expand=True)
        
        # Left side
        left = tk.Frame(content, bg="#1e1e1e")
        left.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        tk.Label(left, text=f"#{index} {data['location']}", 
                font=('Segoe UI', 12, 'bold'), fg="#ffffff", bg="#1e1e1e").pack(anchor=tk.W)
        tk.Label(left, text=f"🌍 {data['disaster']} • {data['severity']}", 
                font=('Segoe UI', 10), fg="#b0b0b0", bg="#1e1e1e").pack(anchor=tk.W, pady=(3, 0))
        tk.Label(left, text=f"🕒 {data['time']}", 
                font=('Segoe UI', 9), fg="#888888", bg="#1e1e1e").pack(anchor=tk.W, pady=(3, 0))
        
        # Right side - Status badge
        status_color = "#00ff00" if data['status'] == "Complete" else "#ffaa00"
        status_frame = tk.Frame(content, bg=status_color, padx=15, pady=8)
        status_frame.pack(side=tk.RIGHT)
        tk.Label(status_frame, text=data['status'], font=('Segoe UI', 10, 'bold'), 
                fg="#000000", bg=status_color).pack()
    
    def display_statistics(self, pending_response):
        # Canvas for scrolling with dark theme
        canvas = tk.Canvas(self.stats_container, bg="#0a0a0a", highlightthickness=0)
        scrollbar = tk.Scrollbar(self.stats_container, orient=tk.VERTICAL, command=canvas.yview)
        scrollable = tk.Frame(canvas, bg="#0a0a0a")
        
        # Proper width binding
        canvas_window = canvas.create_window((0, 0), window=scrollable, anchor="nw")
        
        def configure_scroll(event):
            canvas.configure(scrollregion=canvas.bbox("all"))
        
        def configure_canvas_width(event):
            canvas.itemconfig(canvas_window, width=event.width)
        
        scrollable.bind("<Configure>", configure_scroll)
        canvas.bind("<Configure>", configure_canvas_width)
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Enable mousewheel
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
        self.stats_container.bind("<Enter>", lambda e: canvas.bind_all("<MouseWheel>", _on_mousewheel))
        self.stats_container.bind("<Leave>", lambda e: canvas.unbind_all("<MouseWheel>"))
        
        # Parse data
        lines = pending_response.strip().split('\n')
        total_pending = 0
        severity_count = {'CRITICAL': 0, 'HIGH': 0, 'MODERATE': 0, 'LOW': 0}
        
        for line in lines:
            if line.startswith("ITEM="):
                parts = line[5:].split('|')
                if len(parts) == 3:
                    total_pending += 1
                    if parts[2] in severity_count:
                        severity_count[parts[2]] += 1
        
        # Count dispatched
        total_dispatched = 0
        try:
            with open("Dispatch_History_Report.txt", "r") as f:
                total_dispatched = len(f.readlines())
        except:
            pass
        
        # Main container
        main = tk.Frame(scrollable, bg="#0a0a0a")
        main.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Stats cards row
        stats_row = tk.Frame(main, bg="#0a0a0a")
        stats_row.pack(fill=tk.X, pady=(0, 30))
        
        self.create_stat_card(stats_row, "🚨", "Pending", str(total_pending), "#ff0000")
        self.create_stat_card(stats_row, "✅", "Dispatched", str(total_dispatched), "#00ff00")
        self.create_stat_card(stats_row, "📊", "Total Ops", str(total_pending + total_dispatched), "#00aaff")
        
        # Severity breakdown
        breakdown = tk.Frame(main, bg="#1e1e1e", relief=tk.SOLID, bd=1, highlightthickness=1, highlightbackground="#333333")
        breakdown.pack(fill=tk.BOTH, expand=True)
        
        breakdown_content = tk.Frame(breakdown, bg="#1e1e1e", padx=30, pady=25)
        breakdown_content.pack(fill=tk.BOTH, expand=True)
        
        tk.Label(breakdown_content, text="📊 Severity Distribution", 
                font=('Segoe UI', 16, 'bold'), fg="#ff0000", bg="#1e1e1e").pack(anchor=tk.W, pady=(0, 20))
        
        for severity, count in severity_count.items():
            self.create_progress_bar(breakdown_content, severity, count, 
                                     total_pending if total_pending > 0 else 1)
    
    def create_stat_card(self, parent, icon, title, value, color):
        card = tk.Frame(parent, bg=color, relief=tk.SOLID, bd=2, highlightthickness=0)
        card.pack(side=tk.LEFT, padx=10, fill=tk.BOTH, expand=True)
        
        content = tk.Frame(card, bg=color, padx=20, pady=30)
        content.pack(fill=tk.BOTH, expand=True)
        
        tk.Label(content, text=icon, font=('Segoe UI', 32), bg=color, fg="#000000").pack()
        tk.Label(content, text=title, font=('Segoe UI', 12, 'bold'), 
                fg="#000000", bg=color).pack(pady=(5, 0))
        tk.Label(content, text=value, font=('Segoe UI', 36, 'bold'), 
                fg="#000000", bg=color).pack(pady=(5, 0))
    
    def create_progress_bar(self, parent, label, value, total):
        container = tk.Frame(parent, bg="#1e1e1e")
        container.pack(fill=tk.X, pady=10)
        
        # Label
        label_frame = tk.Frame(container, bg="#1e1e1e")
        label_frame.pack(fill=tk.X, pady=(0, 5))
        
        colors = {'CRITICAL': '#ff0000', 'HIGH': '#ff6600', 'MODERATE': '#ffaa00', 'LOW': '#00ff00'}
        color = colors.get(label, '#00aaff')
        
        tk.Label(label_frame, text=label, font=('Segoe UI', 12, 'bold'), 
                fg="#ffffff", bg="#1e1e1e").pack(side=tk.LEFT)
        
        percentage = (value / total * 100) if total > 0 else 0
        tk.Label(label_frame, text=f"{value} ({percentage:.0f}%)", 
                font=('Segoe UI', 11), fg="#b0b0b0", bg="#1e1e1e").pack(side=tk.RIGHT)
        
        # Progress bar
        bar_bg = tk.Frame(container, bg="#2a2a2a", height=30)
        bar_bg.pack(fill=tk.X)
        
        bar_fill = tk.Frame(bar_bg, bg=color, height=30)
        bar_fill.place(x=0, y=0, relwidth=percentage/100, relheight=1)


if __name__ == "__main__":
    root = tk.Tk()
    app = EmergencyApp(root)
    root.protocol("WM_DELETE_WINDOW", app.on_close)
    root.mainloop()
