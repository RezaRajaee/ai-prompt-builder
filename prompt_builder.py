# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import subprocess


# ==========================================================
# داده‌های منوها
# ==========================================================

data = {
    "نوع ویدئو": [
        "", "TikTok", "Instagram Reel", "YouTube Shorts",
        "Pinterest Idea Pin", "Kwai"
    ],

    "موضوع": [
        "", "Fantasy", "Animals", "Cars", "Fashion", "Luxury",
        "Comedy", "Cooking", "Horror", "Education", "Nature",
        "Technology", "Mythology", "Sci-Fi", "History"
    ],

    "کاراکتر": [
        "", "Young woman", "Young man", "Little girl", "Old man",
        "Robot", "Alien", "Dragon", "Lion", "Wolf", "Fox", "Cat",
        "Dog", "Lizard", "Viking", "Knight", "Fairy", "Angel", "Demon"
    ],

    "ظاهر کاراکتر": [
        "", "20 years old", "Athletic", "Beautiful", "Muscular",
        "Elegant", "Cute", "Dark skin", "White skin", "Asian",
        "Arab", "Persian", "European"
    ],

    "لباس": [
        "", "Casual", "Sport", "Luxury", "Cyberpunk", "Ancient",
        "Medieval", "Royal", "Armor", "Military", "Business",
        "Bikini", "Evening dress", "Traditional"
    ],

    "محیط": [
        "", "Forest", "Jungle", "Beach", "Snow", "Mountain",
        "Castle", "Village", "Modern city", "Cyberpunk city",
        "Space", "Mars", "Ancient temple", "Japanese street",
        "Chinese village", "Desert", "Waterfall"
    ],

    "زمان": [
        "", "Morning", "Golden hour", "Sunset", "Night",
        "Midnight", "Rain", "Storm", "Snow", "Fog", "Autumn",
        "Spring", "Summer", "Winter"
    ],

    "نور": [
        "", "Cinematic", "Soft light", "Golden light", "Moon light",
        "Studio light", "Neon light", "Volumetric light",
        "God rays", "Back light"
    ],

    "حالت دوربین": [
        "", "Close-up", "Medium shot", "Wide shot", "Drone shot",
        "POV", "Selfie", "Tracking shot", "Orbit shot",
        "Low angle", "High angle", "First person"
    ],

    "حرکت دوربین": [
        "", "Slow push in", "Fast push in", "Zoom out", "Orbit",
        "Dolly", "Crane", "Handheld", "FPV", "Hyperlapse",
        "Slow motion"
    ],

    "احساس": [
        "", "Epic", "Cute", "Funny", "Scary", "Sad", "Happy",
        "Emotional", "Inspirational", "Romantic", "Powerful"
    ],

    "کیفیت": [
        "", "8K", "Ultra realistic", "Photorealistic", "HDR",
        "RAW", "Professional", "Award winning", "Ultra detailed"
    ],

    "سبک": [
        "", "Pixar", "Disney", "Anime", "Studio Ghibli", "Marvel",
        "DC", "Cyberpunk", "Dark Fantasy", "High Fantasy",
        "Steampunk", "Realistic", "Hyperrealistic"
    ],

    "نسبت تصویر": [
        "", "09:16", "16:09", "01:01", "04:05"
    ],

    "مدل هوش مصنوعی": [
        "", "Google Veo", "Kling", "Runway", "Pika", "Hailuo",
        "PixVerse", "Luma"
    ],

    "طول مناسب ویدئو": [
        "", "8 sec", "10 sec", "15 sec", "20 sec", "30 sec"
    ],

    "حرکات شخصیت": [
        "", "Walking", "Running", "Flying", "Swimming", "Talking",
        "Dancing", "Fighting", "Looking at camera", "Jumping",
        "Turning"
    ],

    "افکت‌های محیطی": [
        "", "Fire", "Smoke", "Explosion", "Rain", "Snow",
        "Lightning", "Leaves", "Dust", "Sparkles", "Fog"
    ],

    "موسیقی": [
        "", "Epic", "Pop", "Electronic", "Rock", "Fantasy",
        "Calm", "Horror"
    ],

    "رنگ‌بندی": [
        "", "Warm", "Cold", "Orange & Teal", "Black & Gold",
        "Pink", "Blue", "Green", "Purple"
    ],

    "کلمات منفی": [
        "", "Low quality", "Bad anatomy", "Extra fingers", "Blurry",
        "Text", "Watermark", "Logo", "Noise", "Artifacts",
        "Overexposed"
    ]
}


# ==========================================================
# متغیرهای سراسری
# ==========================================================

combos = {}
is_saved = True
current_file = None


# ==========================================================
# توابع و عملکردهای منطقی
# ==========================================================

def update_prompt(event=None):
    """ساخت و به‌روزرسانی متن پرامپت"""
    global is_saved
    is_saved = False

    result = []
    for menu_name, combo in combos.items():
        val = combo.get().strip()
        if val:
            result.append(f"{menu_name}: {val}")

    final_text = ", ".join(result)

    output_text.delete("1.0", tk.END)
    output_text.insert("1.0", final_text)

    update_window_title()


def update_window_title():
    title = "دستیار تولید پرامپت هوشمند - رامین"
    if not is_saved:
        title += " *"
    root.title(title)


def new_file(event=None):
    global is_saved, current_file

    if not is_saved:
        answer = messagebox.askyesnocancel(
            "تغییرات ذخیره‌نشده",
            "تغییراتی اعمال شده که ذخیره نشده‌اند.\nآیا مایل به ذخیره قبل از شروع فرم جدید هستید؟"
        )
        if answer is None:
            return
        if answer is True:
            if not save_file():
                return

    for combo in combos.values():
        combo.set("")

    output_text.delete("1.0", tk.END)
    current_file = None
    is_saved = True
    update_window_title()


def save_file(event=None):
    global is_saved, current_file

    text = output_text.get("1.0", tk.END).strip()
    if not text:
        messagebox.showwarning("خروجی خالی", "ابتدا گزینه‌هایی را انتخاب کنید.")
        return False

    file_path = filedialog.asksaveasfilename(
        title="ذخیره پرامپت",
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
        messagebox.showinfo("موفقیت", "پرامپت با موفقیت ذخیره شد.")
        return True
    except Exception as error:
        messagebox.showerror("خطا در ذخیره", f"خطا رخ داد:\n{error}")
        return False


def copy_output(event=None):
    """
    کپی مطمئن و قطعی در کلیپ‌بورد ویندوز و حافظه سیستم
    """
    text = output_text.get("1.0", tk.END).strip()
    if not text:
        messagebox.showwarning("خروجی خالی", "متنی برای کپی در حافظه وجود ندارد!")
        return

    # روش اول: استفاده از موتور داخلی Tkinter با پاک‌سازی کامل
    try:
        root.clipboard_clear()
        root.clipboard_append(text)
        root.update()  # الزام ویندوز به نگه‌داشتن داده در حافظه
    except Exception:
        pass

    # روش دوم (پشتیبان اختصاصی ویندوز برای اطمینان ۱۰۰٪): دستور clip
    try:
        process = subprocess.Popen(
            'clip',
            stdin=subprocess.PIPE,
            shell=True,
            close_fds=True
        )
        process.communicate(input=text.encode('utf-16le'))
    except Exception:
        pass

    # فیدبک بصری روی دکمه برای اطمینان کاربر
    copy_btn.config(text="✔ با موفقیت کپی شد!", style="Success.TButton")
    root.after(1500, lambda: copy_btn.config(text="📋 کپی در حافظه (Ctrl+C)", style="TButton"))


def quit_app():
    if not is_saved:
        answer = messagebox.askyesnocancel(
            "خروج",
            "تغییرات ذخیره نشده‌اند.\nآیا می‌خواهید قبل از خروج ذخیره کنید؟"
        )
        if answer is None:
            return
        if answer is True:
            if not save_file():
                return

    root.destroy()


def on_text_modified(event=None):
    global is_saved
    if is_saved:
        is_saved = False
        update_window_title()


# ==========================================================
# پنجره اصلی
# ==========================================================

root = tk.Tk()
root.title("دستیار تولید پرامپت هوشمند - رامین")
root.geometry("1100x750")
root.minsize(950, 650)

# استایل‌دهی
style = ttk.Style()
style.theme_use("clam")
style.configure("Success.TButton", foreground="#0b6623", font=("Tahoma", 9, "bold"))

# ماکسیمایز اولیه
try:
    root.state("zoomed")
except tk.TclError:
    root.attributes("-zoomed", True)


# ==========================================================
# منوبار
# ==========================================================

menubar = tk.Menu(root)

file_menu = tk.Menu(menubar, tearoff=0)
file_menu.add_command(label="New", accelerator="Ctrl+N", command=new_file)
file_menu.add_command(label="Save", accelerator="Ctrl+S", command=save_file)
file_menu.add_separator()
file_menu.add_command(label="Quit", accelerator="Alt+F4", command=quit_app)

edit_menu = tk.Menu(menubar, tearoff=0)
edit_menu.add_command(label="Copy", accelerator="Ctrl+C", command=copy_output)
edit_menu.add_separator()
edit_menu.add_command(label="Clear All", command=new_file)

menubar.add_cascade(label="File", menu=file_menu)
menubar.add_cascade(label="Edit", menu=edit_menu)
root.config(menu=menubar)

root.bind_all("<Control-n>", new_file)
root.bind_all("<Control-N>", new_file)
root.bind_all("<Control-s>", save_file)
root.bind_all("<Control-S>", save_file)
root.bind_all("<Control-c>", copy_output)
root.bind_all("<Control-C>", copy_output)


# ==========================================================
# چارچوب اسکرول‌پذیر
# ==========================================================

main_container = ttk.Frame(root)
main_container.pack(fill="both", expand=True)

canvas = tk.Canvas(main_container, background="#f4f5f7", highlightthickness=0)
scrollbar = ttk.Scrollbar(main_container, orient="vertical", command=canvas.yview)

canvas.configure(yscrollcommand=scrollbar.set)
scrollbar.pack(side="right", fill="y")
canvas.pack(side="left", fill="both", expand=True)

form_frame = ttk.Frame(canvas, padding=20)
canvas_window = canvas.create_window((0, 0), window=form_frame, anchor="nw")


def on_canvas_resize(event):
    canvas.itemconfig(canvas_window, width=event.width)


canvas.bind("<Configure>", on_canvas_resize)


def on_frame_resize(event):
    canvas.configure(scrollregion=canvas.bbox("all"))


form_frame.bind("<Configure>", on_frame_resize)


def on_mouse_wheel(event):
    canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")


canvas.bind_all("<MouseWheel>", on_mouse_wheel)


# ==========================================================
# گرید ۲ ستونه (۴ ستون RTL)
# ==========================================================

form_frame.columnconfigure(0, weight=1)
form_frame.columnconfigure(1, weight=0)
form_frame.columnconfigure(2, weight=0)
form_frame.columnconfigure(3, weight=1)
form_frame.columnconfigure(4, weight=0)

items = list(data.items())
total_items = len(items)
half = (total_items + 1) // 2

for i in range(half):
    # ستون راست
    right_name, right_opts = items[i]

    lbl_r = ttk.Label(
        form_frame,
        text=right_name,
        anchor="e",
        justify="right",
        font=("Tahoma", 9, "bold")
    )
    lbl_r.grid(row=i, column=4, padx=(8, 15), pady=7, sticky="e")

    cmb_r = ttk.Combobox(
        form_frame,
        values=right_opts,
        state="readonly",
        width=28,
        font=("Tahoma", 9)
    )
    cmb_r.grid(row=i, column=3, padx=(15, 8), pady=7, sticky="ew")
    cmb_r.set("")
    cmb_r.bind("<<ComboboxSelected>>", update_prompt)
    combos[right_name] = cmb_r

    # ستون چپ
    if i + half < total_items:
        left_name, left_opts = items[i + half]

        lbl_l = ttk.Label(
            form_frame,
            text=left_name,
            anchor="e",
            justify="right",
            font=("Tahoma", 9, "bold")
        )
        lbl_l.grid(row=i, column=1, padx=(8, 25), pady=7, sticky="e")

        cmb_l = ttk.Combobox(
            form_frame,
            values=left_opts,
            state="readonly",
            width=28,
            font=("Tahoma", 9)
        )
        cmb_l.grid(row=i, column=0, padx=(15, 8), pady=7, sticky="ew")
        cmb_l.set("")
        cmb_l.bind("<<ComboboxSelected>>", update_prompt)
        combos[left_name] = cmb_l


# ==========================================================
# باکس خروجی و دکمه کپی
# ==========================================================

current_row = half

sep = ttk.Separator(form_frame, orient="horizontal")
sep.grid(row=current_row, column=0, columnspan=5, sticky="ew", pady=(18, 12), padx=5)
current_row += 1

out_lbl = ttk.Label(
    form_frame,
    text="خروجی پرامپت:",
    anchor="e",
    justify="right",
    font=("Tahoma", 10, "bold")
)
out_lbl.grid(row=current_row, column=4, padx=(8, 15), pady=(0, 5), sticky="ne")

output_text = tk.Text(
    form_frame,
    height=5,
    wrap="word",
    undo=True,
    font=("Consolas", 10),
    relief="solid",
    borderwidth=1
)
output_text.grid(row=current_row, column=0, columnspan=4, padx=(15, 8), pady=(0, 5), sticky="ew")
output_text.bind("<KeyRelease>", on_text_modified)
current_row += 1

copy_btn = ttk.Button(
    form_frame,
    text="📋 کپی در حافظه (Ctrl+C)",
    command=copy_output
)
copy_btn.grid(row=current_row, column=0, columnspan=4, padx=(15, 8), pady=(10, 20), sticky="e")


root.protocol("WM_DELETE_WINDOW", quit_app)
update_window_title()
root.mainloop()
