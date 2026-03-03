import tkinter as tk
from tkinter import ttk, messagebox

# Conversion logic
def celsius_to_fahrenheit(c): return (c * 9/5) + 32
def celsius_to_kelvin(c): return c + 273.15
def fahrenheit_to_celsius(f): return (f - 32) * 5/9
def fahrenheit_to_kelvin(f): return fahrenheit_to_celsius(f) + 273.15
def kelvin_to_celsius(k): return k - 273.15
def kelvin_to_fahrenheit(k): return celsius_to_fahrenheit(kelvin_to_celsius(k))

CONVERSIONS = {
    "Celsius":    {"Fahrenheit": celsius_to_fahrenheit, "Kelvin": celsius_to_kelvin,    "Celsius": lambda x: x},
    "Fahrenheit": {"Celsius": fahrenheit_to_celsius,   "Kelvin": fahrenheit_to_kelvin, "Fahrenheit": lambda x: x},
    "Kelvin":     {"Celsius": kelvin_to_celsius,       "Fahrenheit": kelvin_to_fahrenheit, "Kelvin": lambda x: x},
}

SYMBOLS = {"Celsius": "°C", "Fahrenheit": "°F", "Kelvin": "K"}
LIMITS  = {"Celsius": -273.15, "Fahrenheit": -459.67, "Kelvin": 0}

BG        = "#1E1E2E"
CARD      = "#2A2A3E"
ACCENT    = "#7C6AF7"
ACCENT2   = "#56CFE1"
TEXT      = "#CDD6F4"
SUBTEXT   = "#A6ADC8"
ERROR_CLR = "#F38BA8"
SUCCESS   = "#A6E3A1"
ENTRY_BG  = "#313244"

def convert():
    raw = entry_var.get().strip()
    if not raw:
        show_status("⚠  Please enter a temperature value.", ERROR_CLR)
        clear_results()
        return
    try:
        value = float(raw)
    except ValueError:
        show_status("⚠  Invalid input — enter a numeric value.", ERROR_CLR)
        clear_results()
        return

    from_unit = from_var.get()
    limit = LIMITS[from_unit]
    if value < limit:
        show_status(f"⚠  Below absolute zero for {from_unit} (min: {limit})", ERROR_CLR)
        clear_results()
        return

    results = {}
    for unit, fn in CONVERSIONS[from_unit].items():
        results[unit] = fn(value)

    for unit, lbl in result_labels.items():
        lbl.config(text=f"{results[unit]:,.4f}  {SYMBOLS[unit]}", fg=SUCCESS if unit != from_unit else ACCENT2)

    show_status(f"✔  Converted {value} {SYMBOLS[from_unit]} successfully.", SUCCESS)

def clear_all():
    entry_var.set("")
    clear_results()
    show_status("", BG)

def clear_results():
    for lbl in result_labels.values():
        lbl.config(text="—", fg=SUBTEXT)

def show_status(msg, color):
    status_lbl.config(text=msg, fg=color)

def swap_units():
    f, t = from_var.get(), to_var.get()
    from_var.set(t)
    to_var.set(f)

root = tk.Tk()
root.title("Temperature Converter")
root.geometry("520x560")
root.resizable(False, False)
root.configure(bg=BG)

# ── Title ──────────────────────────────────────────────────────────────────
title_frame = tk.Frame(root, bg=ACCENT, pady=12)
title_frame.pack(fill="x")
tk.Label(title_frame, text="🌡  Temperature Converter", font=("Segoe UI", 16, "bold"),
         bg=ACCENT, fg="white").pack()

# ── Input Card ────────────────────────────────────────────────────────────
card1 = tk.Frame(root, bg=CARD, padx=24, pady=18, bd=0, relief="flat")
card1.pack(fill="x", padx=20, pady=(16, 6))

tk.Label(card1, text="Enter Temperature", font=("Segoe UI", 11, "bold"),
         bg=CARD, fg=TEXT).grid(row=0, column=0, columnspan=3, sticky="w", pady=(0, 10))

entry_var = tk.StringVar()
entry = tk.Entry(card1, textvariable=entry_var, font=("Segoe UI", 18, "bold"),
                 bg=ENTRY_BG, fg=ACCENT2, insertbackground=ACCENT2,
                 relief="flat", bd=0, width=14, justify="center")
entry.grid(row=1, column=0, padx=(0, 12), ipady=8)

tk.Label(card1, text="From", font=("Segoe UI", 9), bg=CARD, fg=SUBTEXT).grid(row=0, column=1, padx=(4,0), sticky="sw")
from_var = tk.StringVar(value="Celsius")
from_cb  = ttk.Combobox(card1, textvariable=from_var, values=["Celsius","Fahrenheit","Kelvin"],
                         state="readonly", width=13, font=("Segoe UI", 11))
from_cb.grid(row=1, column=1, padx=(4, 0), ipady=5)

style = ttk.Style()
style.theme_use("clam")
style.configure("TCombobox", fieldbackground=ENTRY_BG, background=ENTRY_BG,
                foreground=TEXT, selectbackground=ACCENT, selectforeground="white",
                borderwidth=0, relief="flat")
style.map("TCombobox", fieldbackground=[("readonly", ENTRY_BG)], foreground=[("readonly", TEXT)])

# ── Convert Button ────────────────────────────────────────────────────────
btn_frame = tk.Frame(root, bg=BG)
btn_frame.pack(pady=8)

convert_btn = tk.Button(btn_frame, text="⟳  Convert", command=convert,
                        font=("Segoe UI", 12, "bold"), bg=ACCENT, fg="white",
                        relief="flat", padx=20, pady=8, cursor="hand2",
                        activebackground="#9A8BFF", activeforeground="white")
convert_btn.pack(side="left", padx=6)

clear_btn = tk.Button(btn_frame, text="✕  Clear", command=clear_all,
                      font=("Segoe UI", 12), bg=ENTRY_BG, fg=SUBTEXT,
                      relief="flat", padx=16, pady=8, cursor="hand2",
                      activebackground="#45475A", activeforeground=TEXT)
clear_btn.pack(side="left", padx=6)

# ── Results Card ──────────────────────────────────────────────────────────
card2 = tk.Frame(root, bg=CARD, padx=24, pady=18)
card2.pack(fill="x", padx=20, pady=6)

tk.Label(card2, text="Results", font=("Segoe UI", 11, "bold"),
         bg=CARD, fg=TEXT).pack(anchor="w", pady=(0, 12))

result_labels = {}
for unit in ["Celsius", "Fahrenheit", "Kelvin"]:
    row = tk.Frame(card2, bg=ENTRY_BG, pady=10, padx=16)
    row.pack(fill="x", pady=4)
    tk.Label(row, text=f"{unit}  {SYMBOLS[unit]}", font=("Segoe UI", 10),
             bg=ENTRY_BG, fg=SUBTEXT, width=16, anchor="w").pack(side="left")
    val_lbl = tk.Label(row, text="—", font=("Segoe UI", 13, "bold"),
                       bg=ENTRY_BG, fg=SUBTEXT, anchor="e")
    val_lbl.pack(side="right")
    result_labels[unit] = val_lbl

# ── Status Bar ────────────────────────────────────────────────────────────
status_lbl = tk.Label(root, text="", font=("Segoe UI", 9),
                      bg=BG, fg=SUBTEXT, pady=6)
status_lbl.pack()

# ── Formula Reference ─────────────────────────────────────────────────────
ref = tk.Frame(root, bg=CARD, padx=16, pady=10)
ref.pack(fill="x", padx=20, pady=(0, 10))
tk.Label(ref, text="Formulas:  °F = (°C × 9/5) + 32   |   K = °C + 273.15",
         font=("Segoe UI", 8), bg=CARD, fg=SUBTEXT).pack()

entry.bind("<Return>", lambda e: convert())
root.mainloop()
