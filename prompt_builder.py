import os
import subprocess
import tkinter as tk
from tkinter import ttk, messagebox, filedialog

# ---------------------------------------------------------
# Application Data
# ---------------------------------------------------------

data = {
    "Video Type": [
        "",
        "TikTok Video",
        "Instagram Reel",
        "YouTube Shorts",
        "Commercial Ad",
        "Cinematic Scene",
        "Music Video",
        "Documentary",
        "Animation / Cartoon",
        "Tutorial / Explainer",
        "Video Game Cutscene",
    ],
    "Topic": [
        "",
        "Sci-Fi",
        "Fantasy",
        "Cyberpunk",
        "Horror",
        "Nature & Wildlife",
        "Action & Adventure",
        "History & Ancient World",
        "Daily Life / Lifestyle",
        "Space & Universe",
        "Mystery & Thriller",
        "Comedy",
    ],
    "Character": [
        "",
        "Young woman",
        "Young man",
        "Elderly man",
        "Elderly woman",
        "Child (boy)",
        "Child (girl)",
        "Robot / Cyborg",
        "Alien creature",
        "Soldier / Warrior",
        "Businessman",
        "Scientist",
        "None (Scenery only)",
    ],
    "Character Appearance": [
        "",
        "20 years old",
        "30 years old",
        "50 years old",
        "Long blond hair",
        "Short black hair",
        "Bearded",
        "Athletic build",
        "Slim build",
        "Futuristic cybernetic eye",
        "Traditional face paint",
        "Glasses",
    ],
    "Clothing": [
        "",
        "Casual (T-shirt & jeans)",
        "Formal suit",
        "Sport",
        "Traditional / Folk costume",
        "Cyberpunk leather jacket",
        "Armor (Medieval)",
        "Armor (Sci-Fi / Exo-suit)",
        "Lab coat",
        "Winter coat / Hood",
        "Vintage 1920s attire",
    ],
    "Environment": [
        "",
        "Futuristic city",
        "Dense forest",
        "Desert dunes",
        "Snow",
        "Ocean / Underwater",
        "Cyberpunk alley",
        "Space station",
        "Medieval castle",
        "Modern minimalist apartment",
        "Post-apocalyptic wasteland",
        "Cozy cafe interior",
    ],
    "Time": [
        "",
        "Golden hour",
        "Sunrise",
        "Noon / Harsh daylight",
        "Blue hour",
        "Midnight",
        "Overcast / Foggy afternoon",
        "Sunset",
    ],
    "Lighting": [
        "",
        "Neon glow",
        "Soft light",
        "Dramatic side light (Chiaroscuro)",
        "Cinematic backlighting (Rim light)",
        "Studio lighting",
        "Candlelight",
        "Bioluminescent light",
        "Moonlight",
        "Volumetric / God rays",
    ],
    "Camera Shot": [
        "",
        "Close-up",
        "Extreme Close-up",
        "Medium shot",
        "Wide shot (Long shot)",
        "Extreme wide shot",
        "Over-the-shoulder",
        "POV (First-person)",
        "Low-angle shot",
        "High-angle shot",
        "Bird's-eye view",
        "Drone shot",
    ],
    "Camera Movement": [
        "",
        "Static (Tripod)",
        "Slow pan left-to-right",
        "Tracking shot (Follow)",
        "Dolly",
        "Orbit / 360 degree rotation",
        "Zoom in slowly",
        "Handheld / Shaky cam",
        "FPV Drone fast fly-through",
        "Crane / Jib shot",
    ],
    "Mood": [
        "",
        "Epic / Majestic",
        "Dark / Mysterious",
        "Calm / Peaceful",
        "Energetic / Fast-paced",
        "Melancholic",
        "Sad",
        "Horror / Creepy",
        "Futuristic / Tech",
        "Romantic",
        "Nostalgic / Retro",
    ],
    "Quality": [
        "",
        "8K",
        "4K",
        "Ultra realistic",
        "Photorealistic",
        "Hyper-detailed",
        "Ray tracing",
        "Unreal Engine 5 render",
        "Octane render",
        "Masterpiece quality",
    ],
    "Style": [
        "",
        "Cinematic / Live-action",
        "Anime (Makoto Shinkai style)",
        "Studio Ghibli style",
        "Pixar 3D animation",
        "Concept art",
        "Oil painting style",
        "Watercolor",
        "Cyberpunk aesthetic",
        "Vintage film (35mm grain)",
        "Claymation / Stop-motion",
    ],
    "Aspect Ratio": [
        "",
        "16:09",
        "09:16",
        "01:01",
        "04:05",
        "21:09",
        "04:03",
    ],
    "AI Model": [
        "",
        "Midjourney v6",
        "Sora (OpenAI)",
        "Runway Gen-2",
        "Runway Gen-3",
        "Pika Labs (Pika 1.0)",
        "Stable Video Diffusion",
        "Kling AI",
        "Luma Dream Machine",
        "Hailuo AI (Minimax)",
        "Flux.1",
    ],
    "Video Duration": [
        "",
        "8 sec",
        "10 sec",
        "15 sec",
        "20 sec",
        "30 sec",
    ],
    "Character Action": [
        "",
        "Standing still looking at camera",
        "Walking slowly towards camera",
        "Running away in fear",
        "Fighting / Martial arts pose",
        "Typing on holographic keyboard",
        "Drinking coffee looking out window",
        "Smiling gently at viewer",
        "Crying with visible tears",
        "Cast magic spell with glowing hands",
    ],
    "Environmental Effects": [
        "",
        "Rain falling with puddles",
        "Heavy snowfall",
        "Floating dust particles in light",
        "Dense fog / Smoke drifting",
        "Sparks / Embers floating in air",
        "Leaves blowing in wind",
        "Explosion in background",
        "Water splashes in slow motion",
    ],
    "Music": [
        "",
        "Orchestral / Cinematic epic",
        "Lo-Fi hip hop chill beat",
        "Synthwave / 80s Retro electronic",
        "Acoustic guitar gentle melody",
        "Dark ambient / Tension build",
        "Cyberpunk industrial techno",
        "Piano solo emotional",
        "No music / Natural sound only",
    ],
    "Color Grading": [
        "",
        "Teal & Orange (Hollywood style)",
        "Warm vintage tones",
        "Cold / Blue desaturated tones",
        "Vibrant saturated colors",
        "Black & White high contrast",
        "Pastel soft colors",
        "Sepia tone",
        "Monochrome with single color accent",
    ],
    "Negative Prompts": [
        "",
        "blurry, low quality, distorted hands, extra limbs",
        "watermark, text, logo, bad anatomy, deformed",
        "overexposed, underexposed, cartoon, low resolution",
        "flickering, noisy, glitch, artifacts",
    ],
}

# ---------------------------------------------------------
# Global Tracking Variables
# ---------------------------------------------------------

combos = {}
current_file = None
is_saved = True
is_updating = False

# ---------------------------------------------------------
# Core Logic Functions
# ---------------------------------------------------------

def update_prompt(event=None):
    """Generates the prompt string from the active combobox selections."""
    global is_saved
    parts = []
    for name, combo in combos.items():
        val = combo.get()
        if val != "":
            parts.append(f"{name}: {val}")

    prompt = ", ".join(parts)
    output_text.delete("1.0", tk.END)
    output_text.insert(tk.END, prompt)

    is_saved = False
    update_window_title()


def update_window_title():
    """Updates the window title to reflect file state and unsaved changes."""
    title = "Smart Prompt Generator \u2013 Ramin"
    if current_file:
        filename = os.path.basename(current_file)
        title += f" - {filename}"
    if not is_saved:
        title += " *"
    root.title(title)


def new_file(event=None):
    """Resets all fields and output after confirming unsaved changes."""
    global current_file, is_saved
    if not is_saved:
        response = messagebox.askyesnocancel(
            "Unsaved Changes",
            "There are unsaved changes.\nWould you like to save them before starting a new form?"
        )
        if response is None:
            return
        elif response is True:
            if not save_file():
                return

    for combo in combos.values():
        combo.set("")

    output_text.delete("1.0", tk.END)
    current_file = None
    is_saved = True
    update_window_title()


def save_file(event=None):
    """Saves the current prompt output to a text file."""
    global current_file, is_saved
    text = output_text.get("1.0", tk.END).strip()

    if not text:
        messagebox.showwarning(
            "Empty Output",
            "There is no prompt content to save.\nPlease select some options first."
        )
        return False

    file_path = filedialog.asksaveasfilename(
        title="Save Prompt",
        defaultextension=".txt",
        filetypes=[("Text File", "*.txt"), ("All Files", "*.*")]
    )

    if not file_path:
        return False

    try:
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(text)

        current_file = file_path
        is_saved = True
        update_window_title()
        messagebox.showinfo("Saved", "Prompt saved successfully.")
        return True

    except Exception as error:
        messagebox.showerror("Save Error", f"An error occurred while saving the file:\n{error}")
        return False


def load_file(event=None):
    """Loads a previously saved prompt file and restores combobox selections."""
    global current_file, is_saved, is_updating
    if not is_saved:
        response = messagebox.askyesnocancel(
            "Unsaved Changes",
            "There are unsaved changes.\nWould you like to save them before loading a file?"
        )
        if response is None:
            return
        elif response is True:
            if not save_file():
                return

    file_path = filedialog.askopenfilename(
        title="Load Prompt",
        filetypes=[("Text File", "*.txt"), ("All Files", "*.*")]
    )

    if not file_path:
        return

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read().strip()

        if not content:
            messagebox.showwarning("Empty File", "The selected file is empty.")
            return

        # Reset all dropdowns first
        for combo in combos.values():
            combo.set("")

        # Parse Key: Value pairs
        # Format is: Key1: Value1, Key2: Value2, ...
        parsed_data = {}
        items = content.split(", ")
        for item in items:
            if ": " in item:
                key, val = item.split(": ", 1)
                parsed_data[key.strip()] = val.strip()

        # Restore values in comboboxes
        for name, combo in combos.items():
            if name in parsed_data:
                target_val = parsed_data[name]
                if target_val in combo["values"]:
                    combo.set(target_val)
                else:
                    # If the value exists with slight variations or custom edit
                    combo.set(target_val)

        # Update the output area
        is_updating = True
        output_text.delete("1.0", tk.END)
        output_text.insert(tk.END, content)
        is_updating = False

        current_file = file_path
        is_saved = True
        update_window_title()
        messagebox.showinfo("Loaded", "Prompt file loaded successfully.")

    except Exception as error:
        messagebox.showerror("Load Error", f"An error occurred while loading the file:\n{error}")


def copy_output():
    """Copies the prompt content to the Windows clipboard."""
    text = output_text.get("1.0", tk.END).strip()
    if not text:
        messagebox.showwarning("Empty", "No prompt to copy.")
        return

    try:
        root.clipboard_clear()
        root.clipboard_append(text)
        root.update()
        _show_copy_feedback()
    except Exception:
        try:
            process = subprocess.Popen(
                ["clip"],
                stdin=subprocess.PIPE,
                close_fds=True
            )
            process.communicate(input=text.encode("utf-16le"))
            _show_copy_feedback()
        except Exception as error:
            messagebox.showerror(
                "Copy Failed",
                f"Could not copy to clipboard:\n{error}"
            )


def _show_copy_feedback():
    """Temporarily alters the copy button text to confirm clipboard copy."""
    copy_btn.config(
        text="\u2714 Copied successfully!",
        bg="#1b5e20",
        fg="#ffffff"
    )
    root.after(1500, _reset_copy_btn)


def _reset_copy_btn():
    """Restores the copy button appearance to its normal state."""
    copy_btn.config(
        text="\U0001F4CB Copy to Clipboard",
        bg="#007acc",
        fg="#ffffff"
    )


def quit_app():
    """Handles application exit with unsaved changes verification."""
    global is_saved
    if not is_saved:
        response = messagebox.askyesnocancel(
            "Exit Confirmation",
            "There are unsaved changes.\nWould you like to save them before exiting?"
        )
        if response is None:
            return
        elif response is True:
            if not save_file():
                return

    root.destroy()


def on_text_modified(event=None):
    """Tracks manual modifications inside the prompt output Text widget."""
    global is_saved
    if is_updating:
        return
    if output_text.edit_modified():
        is_saved = False
        update_window_title()
        output_text.edit_modified(False)


# ---------------------------------------------------------
# Window & UI Setup
# ---------------------------------------------------------

root = tk.Tk()
root.title("Smart Prompt Generator \u2013 Ramin")
root.geometry("1100x750")
root.minsize(950, 650)
root.state("zoomed")

# ---------------------------------------------------------
# Menu Bar
# ---------------------------------------------------------

menubar = tk.Menu(root)

file_menu = tk.Menu(menubar, tearoff=0)
file_menu.add_command(label="New", command=new_file, accelerator="Ctrl+N")
file_menu.add_command(label="Load", command=load_file, accelerator="Ctrl+O")
file_menu.add_command(label="Save", command=save_file, accelerator="Ctrl+S")
file_menu.add_separator()
file_menu.add_command(label="Quit", command=quit_app, accelerator="Alt+F4")

edit_menu = tk.Menu(menubar, tearoff=0)
edit_menu.add_command(label="Copy", command=copy_output, accelerator="Ctrl+C")
edit_menu.add_separator()
edit_menu.add_command(label="Clear All", command=new_file)

menubar.add_cascade(label="File", menu=file_menu)
menubar.add_cascade(label="Edit", menu=edit_menu)

root.config(menu=menubar)

# Keyboard Shortcuts
root.bind("<Control-n>", new_file)
root.bind("<Control-N>", new_file)
root.bind("<Control-o>", load_file)
root.bind("<Control-O>", load_file)
root.bind("<Control-s>", save_file)
root.bind("<Control-S>", save_file)
root.bind("<Control-c>", lambda e: copy_output())
root.bind("<Control-C>", lambda e: copy_output())
root.protocol("WM_DELETE_WINDOW", quit_app)

# ---------------------------------------------------------
# Scrollable Frame Architecture
# ---------------------------------------------------------

main_canvas = tk.Canvas(root, borderwidth=0, highlightthickness=0)
main_scrollbar = ttk.Scrollbar(
    root,
    orient="vertical",
    command=main_canvas.yview
)
scrollable_frame = ttk.Frame(main_canvas, padding="15 10 15 10")

scrollable_frame.bind(
    "<Configure>",
    lambda e: main_canvas.configure(scrollregion=main_canvas.bbox("all"))
)

canvas_window = main_canvas.create_window(
    (0, 0),
    window=scrollable_frame,
    anchor="nw"
)

def _on_canvas_configure(event):
    main_canvas.itemconfig(canvas_window, width=event.width)

main_canvas.bind("<Configure>", _on_canvas_configure)
main_canvas.configure(xscrollcommand=None, yscrollcommand=main_scrollbar.set)

main_canvas.pack(side="left", fill="both", expand=True)
main_scrollbar.pack(side="right", fill="y")

def _on_mousewheel(event):
    main_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

main_canvas.bind_all("<MouseWheel>", _on_mousewheel)

# ---------------------------------------------------------
# 2-Column Grid (4 RTL Columns)
# ---------------------------------------------------------

scrollable_frame.columnconfigure(0, weight=1)
scrollable_frame.columnconfigure(1, weight=0)
scrollable_frame.columnconfigure(2, weight=0)
scrollable_frame.columnconfigure(3, weight=1)
scrollable_frame.columnconfigure(4, weight=0)

items = list(data.items())
total_items = len(items)
half = (total_items + 1) // 2

for i in range(half):
    # Right Column (First half of items)
    name_r, options_r = items[i]

    lbl_r = ttk.Label(
        scrollable_frame,
        text=f"{name_r}:",
        font=("Tahoma", 9, "bold"),
        anchor="e"
    )
    lbl_r.grid(row=i, column=4, sticky="e", padx=(8, 12), pady=5)

    cb_r = ttk.Combobox(
        scrollable_frame,
        values=options_r,
        state="readonly",
        width=28,
        font=("Tahoma", 9)
    )
    cb_r.set("")
    cb_r.grid(row=i, column=3, sticky="ew", padx=(10, 8), pady=5)
    cb_r.bind("<<ComboboxSelected>>", update_prompt)
    combos[name_r] = cb_r

    # Left Column (Second half of items)
    if i + half < total_items:
        name_l, options_l = items[i + half]

        lbl_l = ttk.Label(
            scrollable_frame,
            text=f"{name_l}:",
            font=("Tahoma", 9, "bold"),
            anchor="e"
        )
        lbl_l.grid(row=i, column=1, sticky="e", padx=(8, 12), pady=5)

        cb_l = ttk.Combobox(
            scrollable_frame,
            values=options_l,
            state="readonly",
            width=28,
            font=("Tahoma", 9)
        )
        cb_l.set("")
        cb_l.grid(row=i, column=0, sticky="ew", padx=(10, 8), pady=5)
        cb_l.bind("<<ComboboxSelected>>", update_prompt)
        combos[name_l] = cb_l

# ---------------------------------------------------------
# Output Text Area & Copy Button
# ---------------------------------------------------------

current_row = half

sep = ttk.Separator(scrollable_frame, orient="horizontal")
sep.grid(
    row=current_row,
    column=0,
    columnspan=5,
    sticky="ew",
    pady=(16, 12)
)
current_row += 1

output_label = ttk.Label(
    scrollable_frame,
    text=":Prompt Output",
    font=("Tahoma", 10, "bold")
)
output_label.grid(
    row=current_row,
    column=4,
    sticky="ne",
    padx=(8, 12),
    pady=4
)

output_text = tk.Text(
    scrollable_frame,
    height=5,
    wrap="word",
    font=("Consolas", 10),
    undo=True,
    relief="solid",
    borderwidth=1
)
output_text.grid(
    row=current_row,
    column=0,
    columnspan=4,
    sticky="ew",
    padx=(10, 8),
    pady=4
)
output_text.bind("<<Modified>>", on_text_modified)
current_row += 1

copy_btn = tk.Button(
    scrollable_frame,
    text="\U0001F4CB Copy to Clipboard",
    command=copy_output,
    bg="#007acc",
    fg="#ffffff",
    activebackground="#005999",
    activeforeground="#ffffff",
    font=("Tahoma", 9, "bold"),
    relief="flat",
    cursor="hand2",
    padx=16,
    pady=6
)
copy_btn.grid(
    row=current_row,
    column=0,
    columnspan=5,
    sticky="e",
    padx=10,
    pady=(8, 12)
)

# ---------------------------------------------------------
# Application Entry Point
# ---------------------------------------------------------

root.mainloop()
