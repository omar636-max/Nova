import tkinter as tk
from tkinter import font
import json
from pathlib import Path


# =========================================================
# NOVA CALCULATOR PRO
# =========================================================


# =========================================================
# Save Data
# =========================================================

DATA_FOLDER = Path.home() / "NovaCalculator"
DATA_FOLDER.mkdir(exist_ok=True)

HISTORY_FILE = DATA_FOLDER / "history.json"


# =========================================================
# Themes
# =========================================================

DARK = {
    "bg": "#0B0F19",
    "panel": "#121826",
    "display": "#171D2D",
    "text": "#FFFFFF",
    "secondary": "#8D96A8",
    "number": "#1F2738",
    "number_hover": "#2B354A",
    "special": "#30394C",
    "special_hover": "#3C475D",
    "operator": "#7C4DFF",
    "operator_hover": "#935FFF",
    "equal": "#00C896",
    "equal_hover": "#00E0A6"
}


LIGHT = {
    "bg": "#EEF2F7",
    "panel": "#FFFFFF",
    "display": "#E3E8F0",
    "text": "#18202D",
    "secondary": "#687386",
    "number": "#FFFFFF",
    "number_hover": "#E7EBF2",
    "special": "#D8DEE8",
    "special_hover": "#C7CFDC",
    "operator": "#7252E8",
    "operator_hover": "#866BEE",
    "equal": "#00A67D",
    "equal_hover": "#00BC91"
}


theme = DARK

memory = 0
operation_count = 0

button_objects = []


# =========================================================
# Main Window
# =========================================================

window = tk.Tk()
window.title("Nova Calculator Pro")
window.geometry("430x700")
window.resizable(False, False)
window.configure(bg=theme["bg"])


# =========================================================
# Fonts
# =========================================================

title_font = font.Font(
    family="Segoe UI",
    size=18,
    weight="bold"
)

display_font = font.Font(
    family="Segoe UI",
    size=32,
    weight="bold"
)

button_font = font.Font(
    family="Segoe UI",
    size=16,
    weight="bold"
)


# =========================================================
# Header
# =========================================================

header = tk.Frame(
    window,
    bg=theme["bg"]
)

header.pack(
    fill="x",
    padx=20,
    pady=(16, 8)
)


title_label = tk.Label(
    header,
    text="NOVA",
    font=title_font,
    bg=theme["bg"],
    fg=theme["text"]
)

title_label.pack(side="left")


count_label = tk.Label(
    header,
    text="0 calculations",
    font=("Segoe UI", 9),
    bg=theme["bg"],
    fg=theme["secondary"]
)

count_label.pack(
    side="left",
    padx=10
)


# =========================================================
# Theme Button
# =========================================================

theme_button = tk.Button(
    header,
    text="☾",
    font=("Segoe UI", 14, "bold"),
    width=3,
    bd=0,
    relief="flat",
    cursor="hand2"
)

theme_button.pack(side="right")
# =========================================================
# About Button
# =========================================================

def show_about():

    about = tk.Toplevel(window)

    about.title("About Nova")
    about.geometry("340x300")
    about.resizable(False, False)
    about.configure(bg=theme["bg"])

    tk.Label(
        about,
        text="NOVA",
        font=("Segoe UI", 30, "bold"),
        bg=theme["bg"],
        fg=theme["operator"]
    ).pack(pady=(30, 5))

    tk.Label(
        about,
        text="CALCULATOR PRO",
        font=("Segoe UI", 11, "bold"),
        bg=theme["bg"],
        fg=theme["text"]
    ).pack()

    tk.Label(
        about,
        text="Version 1.0",
        font=("Segoe UI", 10),
        bg=theme["bg"],
        fg=theme["secondary"]
    ).pack(pady=15)

    tk.Label(
        about,
        text="A modern calculator built with Python.",
        font=("Segoe UI", 10),
        bg=theme["bg"],
        fg=theme["secondary"]
    ).pack()

    tk.Button(
        about,
        text="Close",
        font=("Segoe UI", 10, "bold"),
        bg=theme["operator"],
        fg="white",
        bd=0,
        relief="flat",
        cursor="hand2",
        command=about.destroy
    ).pack(
        pady=25,
        ipadx=25,
        ipady=7
    )


about_button = tk.Button(
    header,
    text="ⓘ",
    font=("Segoe UI", 14, "bold"),
    width=3,
    bd=0,
    relief="flat",
    cursor="hand2",
    command=show_about
)

about_button.pack(
    side="right",
    padx=5
)

# =========================================================
# Display
# =========================================================

display_frame = tk.Frame(
    window,
    bg=theme["display"]
)

display_frame.pack(
    fill="x",
    padx=20,
    pady=10
)


expression_label = tk.Label(
    display_frame,
    text="",
    font=("Segoe UI", 11),
    anchor="e",
    bg=theme["display"],
    fg=theme["secondary"]
)

expression_label.pack(
    fill="x",
    padx=18,
    pady=(14, 0)
)


display = tk.Entry(
    display_frame,
    font=display_font,
    justify="right",
    bd=0,
    relief="flat",
    bg=theme["display"],
    fg=theme["text"],
    insertbackground=theme["text"]
)

display.pack(
    fill="x",
    padx=18,
    pady=(4, 18),
    ipady=8
)


# =========================================================
# Calculator Functions
# =========================================================

def add_value(value):
    display.insert(tk.END, value)


def clear():
    display.delete(0, tk.END)
    expression_label.config(text="")


def delete_last():
    value = display.get()

    if value:
        display.delete(0, tk.END)
        display.insert(0, value[:-1])


def plus_minus():
    value = display.get()

    if not value:
        return

    if value.startswith("-"):
        value = value[1:]
    else:
        value = "-" + value

    display.delete(0, tk.END)
    display.insert(0, value)


def format_result(result):

    if isinstance(result, float):

        if result.is_integer():
            return str(int(result))

        return f"{result:.10g}"

    return str(result)


def show_error(message="Error"):
    display.delete(0, tk.END)
    display.insert(0, message)


def percent():

    try:

        value = float(display.get())
        result = value / 100

        display.delete(0, tk.END)
        display.insert(0, format_result(result))

    except:

        show_error()


def calculate():

    global operation_count

    expression = display.get()

    if not expression:
        return

    try:

        expression_for_calc = expression

        expression_for_calc = expression_for_calc.replace(
            "×",
            "*"
        )

        expression_for_calc = expression_for_calc.replace(
            "÷",
            "/"
        )

        expression_for_calc = expression_for_calc.replace(
            "−",
            "-"
        )

        result = eval(
            expression_for_calc,
            {"__builtins__": None},
            {}
        )

        result_text = format_result(result)

        expression_label.config(
            text=expression + " ="
        )

        display.delete(0, tk.END)
        display.insert(0, result_text)

        operation_count += 1

        count_label.config(
            text=f"{operation_count} calculations"
        )

        history_list.insert(
            0,
            f"{expression} = {result_text}"
        )

        save_history()

    except ZeroDivisionError:

        show_error("Cannot divide by zero")

    except:

        show_error()


# =========================================================
# Memory Functions
# =========================================================

def memory_clear():

    global memory

    memory = 0


def memory_recall():

    display.delete(0, tk.END)
    display.insert(
        0,
        format_result(memory)
    )


def memory_add():

    global memory

    try:

        value = float(
            display.get()
        )

        memory += value

    except:

        show_error()


def memory_subtract():

    global memory

    try:

        value = float(
            display.get()
        )

        memory -= value

    except:

        show_error()


# =========================================================
# History
# =========================================================

history_frame = tk.Frame(
    window,
    bg=theme["panel"]
)

history_frame.pack(
    fill="x",
    padx=20,
    pady=(6, 10)
)


history_title = tk.Label(
    history_frame,
    text="History",
    font=("Segoe UI", 11, "bold"),
    anchor="w",
    bg=theme["panel"],
    fg=theme["text"]
)

history_title.pack(
    fill="x",
    padx=15,
    pady=(8, 3)
)


history_list = tk.Listbox(
    history_frame,
    height=3,
    font=("Segoe UI", 10),
    bd=0,
    relief="flat",
    highlightthickness=0,
    bg=theme["panel"],
    fg=theme["text"]
)

history_list.pack(
    fill="x",
    padx=15,
    pady=(0, 6)
)


def save_history():

    try:

        items = list(
            history_list.get(
                0,
                tk.END
            )
        )

        items = items[:20]

        with open(
            HISTORY_FILE,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                items,
                file,
                ensure_ascii=False,
                indent=2
            )

    except:

        pass


def load_history():

    global operation_count

    try:

        if HISTORY_FILE.exists():

            with open(
                HISTORY_FILE,
                "r",
                encoding="utf-8"
            ) as file:

                items = json.load(file)

            if isinstance(items, list):

                for item in items[:20]:

                    history_list.insert(
                        tk.END,
                        item
                    )

                operation_count = len(items)

                count_label.config(
                    text=f"{operation_count} calculations"
                )

    except:

        pass


def clear_history():

    history_list.delete(
        0,
        tk.END
    )

    save_history()


clear_history_button = tk.Button(
    history_frame,
    text="Clear History",
    font=("Segoe UI", 9, "bold"),
    bd=0,
    relief="flat",
    cursor="hand2",
    command=clear_history,
    bg=theme["special"],
    fg=theme["text"],
    activebackground=theme["special_hover"],
    activeforeground=theme["text"]
)

clear_history_button.pack(
    pady=(0, 8)
)


# =========================================================
# Buttons Frame
# =========================================================

buttons_frame = tk.Frame(
    window,
    bg=theme["bg"]
)

buttons_frame.pack(
    fill="both",
    expand=True,
    padx=18
)


for column in range(4):

    buttons_frame.columnconfigure(
        column,
        weight=1
    )


for row in range(6):

    buttons_frame.rowconfigure(
        row,
        weight=1
    )


# =========================================================
# Button Creator
# =========================================================

def create_button(
    text,
    row,
    column,
    command,
    button_type="number"
):

    if button_type == "operator":

        normal = theme["operator"]
        hover = theme["operator_hover"]

    elif button_type == "equal":

        normal = theme["equal"]
        hover = theme["equal_hover"]

    elif button_type == "special":

        normal = theme["special"]
        hover = theme["special_hover"]

    else:

        normal = theme["number"]
        hover = theme["number_hover"]


    button = tk.Button(
        buttons_frame,
        text=text,
        font=button_font,
        bd=0,
        relief="flat",
        cursor="hand2",
        bg=normal,
        fg=theme["text"],
        activebackground=hover,
        activeforeground=theme["text"],
        command=command
    )

    button.grid(
        row=row,
        column=column,
        sticky="nsew",
        padx=5,
        pady=5,
        ipady=7
    )


    button.bind(
        "<Enter>",
        lambda event, b=button, c=hover:
        b.configure(bg=c)
    )


    button.bind(
        "<Leave>",
        lambda event, b=button, c=normal:
        b.configure(bg=c)
    )


    button_objects.append(
        {
            "button": button,
            "type": button_type,
            "normal": normal,
            "hover": hover
        }
    )


# =========================================================
# Memory Row
# =========================================================

create_button(
    "MC",
    0,
    0,
    memory_clear,
    "special"
)

create_button(
    "MR",
    0,
    1,
    memory_recall,
    "special"
)

create_button(
    "M+",
    0,
    2,
    memory_add,
    "special"
)

create_button(
    "M−",
    0,
    3,
    memory_subtract,
    "special"
)


# =========================================================
# Special Row
# =========================================================

create_button(
    "AC",
    1,
    0,
    clear,
    "special"
)

create_button(
    "⌫",
    1,
    1,
    delete_last,
    "special"
)

create_button(
    "±",
    1,
    2,
    plus_minus,
    "special"
)

create_button(
    "%",
    1,
    3,
    percent,
    "special"
)


# =========================================================
# Row 2
# =========================================================

create_button(
    "7",
    2,
    0,
    lambda: add_value("7")
)

create_button(
    "8",
    2,
    1,
    lambda: add_value("8")
)

create_button(
    "9",
    2,
    2,
    lambda: add_value("9")
)

create_button(
    "÷",
    2,
    3,
    lambda: add_value("÷"),
    "operator"
)


# =========================================================
# Row 3
# =========================================================

create_button(
    "4",
    3,
    0,
    lambda: add_value("4")
)

create_button(
    "5",
    3,
    1,
    lambda: add_value("5")
)

create_button(
    "6",
    3,
    2,
    lambda: add_value("6")
)

create_button(
    "×",
    3,
    3,
    lambda: add_value("×"),
    "operator"
)


# =========================================================
# Row 4
# =========================================================

create_button(
    "1",
    4,
    0,
    lambda: add_value("1")
)

create_button(
    "2",
    4,
    1,
    lambda: add_value("2")
)

create_button(
    "3",
    4,
    2,
    lambda: add_value("3")
)

create_button(
    "−",
    4,
    3,
    lambda: add_value("−"),
    "operator"
)


# =========================================================
# Row 5
# =========================================================

create_button(
    "0",
    5,
    0,
    lambda: add_value("0")
)

create_button(
    ".",
    5,
    1,
    lambda: add_value(".")
)

create_button(
    "+",
    5,
    2,
    lambda: add_value("+"),
    "operator"
)

create_button(
    "=",
    5,
    3,
    calculate,
    "equal"
)


# =========================================================
# Theme Functions
# =========================================================

def apply_theme():

    window.configure(
        bg=theme["bg"]
    )

    header.configure(
        bg=theme["bg"]
    )

    title_label.configure(
        bg=theme["bg"],
        fg=theme["text"]
    )

    count_label.configure(
        bg=theme["bg"],
        fg=theme["secondary"]
    )

    theme_button.configure(
        bg=theme["special"],
        fg=theme["text"],
        activebackground=theme["special_hover"],
        activeforeground=theme["text"]
    )

    display_frame.configure(
        bg=theme["display"]
    )

    expression_label.configure(
        bg=theme["display"],
        fg=theme["secondary"]
    )

    display.configure(
        bg=theme["display"],
        fg=theme["text"],
        insertbackground=theme["text"]
    )

    history_frame.configure(
        bg=theme["panel"]
    )

    history_title.configure(
        bg=theme["panel"],
        fg=theme["text"]
    )

    history_list.configure(
        bg=theme["panel"],
        fg=theme["text"]
    )

    clear_history_button.configure(
        bg=theme["special"],
        fg=theme["text"],
        activebackground=theme["special_hover"],
        activeforeground=theme["text"]
    )

    buttons_frame.configure(
        bg=theme["bg"]
    )

    for item in button_objects:

        button = item["button"]

        if item["type"] == "operator":

            normal = theme["operator"]
            hover = theme["operator_hover"]

        elif item["type"] == "equal":

            normal = theme["equal"]
            hover = theme["equal_hover"]

        elif item["type"] == "special":

            normal = theme["special"]
            hover = theme["special_hover"]

        else:

            normal = theme["number"]
            hover = theme["number_hover"]

        button.configure(
            bg=normal,
            fg=theme["text"],
            activebackground=hover,
            activeforeground=theme["text"]
        )

        item["normal"] = normal
        item["hover"] = hover


def toggle_theme():

    global theme

    if theme == DARK:

        theme = LIGHT
        theme_button.config(
            text="☀"
        )

    else:

        theme = DARK
        theme_button.config(
            text="☾"
        )

    apply_theme()


theme_button.config(
    command=toggle_theme
)


# =========================================================
# Keyboard Support
# =========================================================

def keyboard_input(event):

    key = event.keysym
    char = event.char

    if char.isdigit():

        add_value(char)

    elif char in "+-.":

        add_value(char)

    elif char == "*":

        add_value("×")

    elif char == "/":

        add_value("÷")

    elif key == "Return":

        calculate()

    elif key == "BackSpace":

        delete_last()

    elif key == "Escape":

        clear()


window.bind(
    "<Key>",
    keyboard_input
)


# =========================================================
# Load History
# =========================================================

load_history()


# =========================================================
# Splash Screen
# =========================================================

window.withdraw()


splash = tk.Toplevel()

splash.title("NOVA")
splash.geometry("430x260")
splash.resizable(False, False)

splash.configure(
    bg="#0B0F19"
)


# Center splash screen

screen_width = splash.winfo_screenwidth()
screen_height = splash.winfo_screenheight()

x = (screen_width - 430) // 2
y = (screen_height - 260) // 2

splash.geometry(
    f"430x260+{x}+{y}"
)


# Logo

logo_label = tk.Label(
    splash,
    text="N",
    font=("Segoe UI", 58, "bold"),
    bg="#0B0F19",
    fg="#7C4DFF"
)

logo_label.pack(
    pady=(25, 0)
)


# Name

name_label = tk.Label(
    splash,
    text="NOVA",
    font=("Segoe UI", 25, "bold"),
    bg="#0B0F19",
    fg="#FFFFFF"
)

name_label.pack()


# Subtitle

subtitle_label = tk.Label(
    splash,
    text="CALCULATOR PRO",
    font=("Segoe UI", 10),
    bg="#0B0F19",
    fg="#8D96A8"
)

subtitle_label.pack(
    pady=4
)


# Loading

loading_label = tk.Label(
    splash,
    text="Starting...",
    font=("Segoe UI", 9),
    bg="#0B0F19",
    fg="#00C896"
)

loading_label.pack(
    pady=12
)


def show_calculator():

    splash.destroy()
    window.deiconify()


splash.after(
    1800,
    show_calculator
)


# =========================================================
# Start
# =========================================================

window.mainloop()  