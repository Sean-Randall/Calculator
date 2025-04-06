import tkinter as tk

# Define two font size sets
LARGE_FONT_STYLE = ("Arial", 40, "bold")
SMALL_FONT_STYLE = ("Arial", 20)
DIGITS_FONT_STYLE_LARGE = ("Arial", 24, "bold")
DIGITS_FONT_STYLE_SMALL = ("Arial", 16, "bold")
DEFAULT_FONT_STYLE_LARGE = ("Arial", 20)
DEFAULT_FONT_STYLE_SMALL = ("Arial", 12)

OFF_WHITE = "#F8FAFF"
WHITE = "#FFFFFF"
LIGHT_BLUE = "#CCEDFF"
LIGHT_GRAY = "#F5F5F5"
LABEL_COLOR = "#25265E"

class Calculator:
    def __init__(self):
        self.window = tk.Tk()
        self.window.geometry("375x667")
        self.window.resizable(0, 0)
        self.window.title("Calculator")

        # Default font setting
        self.font_size = tk.StringVar(value="Large")

        self.create_font_selector()

        self.total_expression = ""
        self.current_expression = ""

        self.display_frame = self.create_display_frame()
        self.total_label, self.label = self.create_display_labels()

        self.digits = {
            7: (1, 1), 8: (1, 2), 9: (1, 3),
            4: (2, 1), 5: (2, 2), 6: (2, 3),
            1: (3, 1), 2: (3, 2), 3: (3, 3),
            0: (4, 2), '.': (4, 1)
        }

        self.operations = {"/": "\u00F7", "*": "\u00D7", "-": "-", "+": "+"}
        self.buttons_frame = self.create_buttons_frame()

        self.buttons_frame.rowconfigure(0, weight=1)
        for x in range(1, 5):
            self.buttons_frame.rowconfigure(x, weight=1)
            self.buttons_frame.columnconfigure(x, weight=1)

        self.create_digit_buttons()
        self.create_operator_buttons()
        self.create_special_buttons()
        self.bind_keys()

        self.window.mainloop()

    def create_font_selector(self):
        font_frame = tk.Frame(self.window, bg=WHITE)
        font_frame.pack(fill='x', padx=10, pady=5)

        label = tk.Label(font_frame, text="Font Size:", bg=WHITE)
        label.pack(side='left')

        font_dropdown = tk.OptionMenu(font_frame, self.font_size, "Small", "Large", command=self.reload_ui)
        font_dropdown.pack(side='left')

    def get_fonts(self):
        if self.font_size.get() == "Small":
            return SMALL_FONT_STYLE, DIGITS_FONT_STYLE_SMALL, DEFAULT_FONT_STYLE_SMALL
        return LARGE_FONT_STYLE, DIGITS_FONT_STYLE_LARGE, DEFAULT_FONT_STYLE_LARGE

    def reload_ui(self, _=None):
        # Destroy and rebuild display and buttons
        self.display_frame.destroy()
        self.buttons_frame.destroy()
        self.display_frame = self.create_display_frame()
        self.total_label, self.label = self.create_display_labels()
        self.buttons_frame = self.create_buttons_frame()
        for x in range(1, 5):
            self.buttons_frame.rowconfigure(x, weight=1)
            self.buttons_frame.columnconfigure(x, weight=1)
        self.create_digit_buttons()
        self.create_operator_buttons()
        self.create_special_buttons()

    def bind_keys(self):
        self.window.bind("<Return>", lambda event: self.evaluate())
        for key in self.digits:
            self.window.bind(str(key), lambda event, digit=key: self.add_to_expression(digit))
        for key in self.operations:
            self.window.bind(key, lambda event, operator=key: self.append_operator(operator))

    def create_display_labels(self):
        large_font, _, _ = self.get_fonts()
        total_label = tk.Label(self.display_frame, text=self.total_expression, anchor=tk.E, bg=WHITE,
                               fg=LABEL_COLOR, padx=24, font=SMALL_FONT_STYLE)
        total_label.pack(expand=True, fill='both')

        label = tk.Label(self.display_frame, text=self.current_expression, anchor=tk.E, bg=WHITE,
                         fg=LABEL_COLOR, padx=24, font=large_font)
        label.pack(expand=True, fill='both')

        return total_label, label

    def create_display_frame(self):
        frame = tk.Frame(self.window, height=221, bg=WHITE)
        frame.pack(expand=True, fill="both")
        return frame

    def add_to_expression(self, value):
        self.current_expression += str(value)
        self.update_label()

    def update_label(self):
        self.label.config(text=self.current_expression[:11])

    def create_digit_buttons(self):
        _, digits_font, _ = self.get_fonts()
        for digit, grid_value in self.digits.items():
            button = tk.Button(self.buttons_frame, text=str(digit), bg=WHITE, fg=LABEL_COLOR,
                               font=digits_font, borderwidth=0,
                               command=lambda x=digit: self.add_to_expression(x))
            button.grid(row=grid_value[0], column=grid_value[1], sticky=tk.NSEW)

    def append_operator(self, operator):
        self.current_expression += operator
        self.total_expression += self.current_expression
        self.current_expression = ""
        self.update_total_label()
        self.update_label()

    def update_total_label(self):
        self.total_label.config(text=self.total_expression)

    def create_operator_buttons(self):
        _, _, default_font = self.get_fonts()
        i = 0
        for operator, symbol in self.operations.items():
            button = tk.Button(self.buttons_frame, text=symbol, bg=OFF_WHITE, fg=LABEL_COLOR,
                               font=default_font, borderwidth=0,
                               command=lambda x=operator: self.append_operator(x))
            button.grid(row=i, column=4, sticky=tk.NSEW)
            i += 1

    def clear(self):
        self.current_expression = ""
        self.total_expression = ""
        self.update_label()
        self.update_total_label()

    def evaluate(self):
        self.total_expression += self.current_expression
        try:
            self.current_expression = str(eval(self.total_expression))
            self.total_expression = ""
        except Exception as e:
            self.current_expression = "Error"
        finally:
            self.update_label()
            self.update_total_label()

    def create_special_buttons(self):
        _, _, default_font = self.get_fonts()
        clear_button = tk.Button(self.buttons_frame, text="C", bg=LIGHT_GRAY, fg=LABEL_COLOR,
                                 font=default_font, borderwidth=0, command=self.clear)
        clear_button.grid(row=0, column=1, sticky=tk.NSEW)

        equals_button = tk.Button(self.buttons_frame, text="=", bg=LIGHT_BLUE, fg=LABEL_COLOR,
                                  font=default_font, borderwidth=0, command=self.evaluate)
        equals_button.grid(row=0, column=2, columnspan=2, sticky=tk.NSEW)

    def create_buttons_frame(self):
        frame = tk.Frame(self.window)
        frame.pack(expand=True, fill="both")
        return frame


if __name__ == "__main__":
    Calculator()
