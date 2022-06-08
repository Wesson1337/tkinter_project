"""Simple calculator made in tkinter"""

import tkinter as tk

OFF_WHITE = "#F8FAFF"
WHITE = "#FFFFFF"
LIGHT_BLUE = "#CCEDFF"
ACTIVE_LIGHT_BLUE = "#B9D7E8"
LIGHT_GRAY = "#F5F5F5"
LABEL_COLOR = "#25265E"
RED_COLOR = "#FF5F7C"
ACTIVE_RED = "#EC5F79"


class Calculator:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title('Calculator')
        self.window.minsize(350, 500)
        self.window.resizable(True, True)
        self.window.rowconfigure(0, weight=1, minsize=120)
        self.window.rowconfigure(1, weight=3, minsize=300)
        self.window.columnconfigure(0, weight=1, minsize=300)

        self.digits_dict = {
            7: (1, 1), 8: (1, 2), 9: (1, 3),
            4: (2, 1), 5: (2, 2), 6: (2, 3),
            1: (3, 1), 2: (3, 2), 3: (3, 3),
            0: (4, 2), '.': (4, 1)
        }
        self.operations = {"/": "\u00F7", "*": "\u00D7", "-": "-", "+": "+"}

        self.total_expression = ""
        self.current_expression = ""
        self.last_added = ''

        self._create_main_frame()
        self._create_buttons_frame()

        self.buttons_frm.rowconfigure(0, weight=1)
        for i in range(1, 5):
            self.buttons_frm.rowconfigure(i, weight=1)
            self.buttons_frm.columnconfigure(i, weight=1)

        self._create_digit_buttons()
        self._create_operator_buttons()
        self._create_special_buttons()

        self._create_display_labels()
        self._bind_keys()

    def _bind_keys(self):
        self.window.bind("<Return>", lambda event: self.evaluate())
        for key in self.digits_dict:
            self.window.bind(str(key), lambda event, digit=key: self.add_to_expression(digit))

        for key in self.operations:
            self.window.bind(key, lambda event, operator=key: self.append_operator(operator))

    def _create_main_frame(self):
        self.main_frm = tk.Frame(self.window, height=150, width=350, bg=LIGHT_GRAY)
        self.main_frm.grid(row=0, column=0, sticky='swen')

    def _create_buttons_frame(self):
        self.buttons_frm = tk.Frame(self.window)
        self.buttons_frm.grid(row=1, column=0, sticky='swen')

    def _create_digit_buttons(self):
        for digit, grid_value in self.digits_dict.items():
            button = tk.Button(self.buttons_frm, text=str(digit), bg=WHITE, fg=LABEL_COLOR, borderwidth=0,
                               font=("Arial", 24, "bold"), command=lambda x=digit: self.add_to_expression(x))
            button.grid(row=grid_value[0], column=grid_value[1], sticky='swen')

    def _create_operator_buttons(self):
        i = 0
        for operator, symbol in self.operations.items():
            button = tk.Button(self.buttons_frm, text=symbol, bg=OFF_WHITE, fg=LABEL_COLOR, font=("Arial", 20),
                               command=lambda x=operator: self.append_operator(x), borderwidth=0)
            button.grid(row=i, column=4, sticky='swen')
            i += 1

    def _create_special_buttons(self):
        sqrt_button = tk.Button(self.buttons_frm, text="\u221ax", bg=OFF_WHITE, fg=LABEL_COLOR, font=("Arial", 20),
                                borderwidth=0, command=self.sqrt)
        sqrt_button.grid(row=0, column=3, sticky='swen')

        square_button = tk.Button(self.buttons_frm, text="x\u00b2", bg=OFF_WHITE, fg=LABEL_COLOR, font=("Arial", 20),
                                  borderwidth=0, command=self.square)
        square_button.grid(row=0, column=2, sticky='swen')

        clear_button = tk.Button(self.buttons_frm, text="C", bg=RED_COLOR, fg=LABEL_COLOR, font=("Arial", 20),
                                 borderwidth=0, command=self.clear, activebackground=ACTIVE_RED)
        clear_button.grid(row=0, column=1, sticky='swen')

        equals_button = tk.Button(self.buttons_frm, text="=", bg=LIGHT_BLUE, fg=LABEL_COLOR, font=("Arial", 20),
                                  borderwidth=0, command=self.evaluate, activebackground=ACTIVE_LIGHT_BLUE)
        equals_button.grid(row=4, column=3, columnspan=2, sticky='swen')

    def _create_display_labels(self):
        self.total_label = tk.Label(self.main_frm, text=self.total_expression, anchor=tk.E, bg=LIGHT_GRAY,
                                    fg=LABEL_COLOR, padx=24, font=("Arial", 15))
        self.total_label.pack(expand=True, fill='both')

        self.label = tk.Label(self.main_frm, text=self.current_expression, anchor=tk.E, bg=LIGHT_GRAY,
                              fg=LABEL_COLOR, padx=24, font=("Arial", 30, "bold"))
        self.label.pack(expand=True, fill='both')

    def append_operator(self, operator):
        if self.last_added == 'digit' or self.last_added in self.operations:
            if self.last_added == 'digit':
                self.current_expression += operator
                self.total_expression += self.current_expression
            else:
                self.current_expression = self.current_expression[:-1] + operator
                self.total_expression = self.total_expression[:-1] + self.current_expression
            self.current_expression = ""
            self.update_total_label()
            self.update_label()
        self.last_added = operator

    def add_to_expression(self, value):
        if not self.current_expression == 'Error':
            self.current_expression += str(value)
            self.last_added = 'digit'
            self.update_label()

    def sqrt(self):
        self.current_expression = str(eval(f"{self.current_expression}**0.5"))
        self.update_label()

    def square(self):
        self.current_expression = str(eval(f"{self.current_expression}**2"))
        self.update_label()

    def clear(self):
        self.current_expression = ""
        self.total_expression = ""
        self.update_label()
        self.update_total_label()
        self.last_added = ''

    def evaluate(self):
        if self.current_expression != 'Error' and self.last_added not in self.operations:
            self.total_expression += self.current_expression
            self.update_total_label()
            try:
                self.current_expression = str(eval(self.total_expression))
                self.total_expression = ""
            except Exception:
                self.current_expression = "Error"
            finally:
                self.update_label()

    def update_label(self):
        self.label.config(text=self.current_expression)

    def update_total_label(self):
        expression = self.total_expression
        for operator, symbol in self.operations.items():
            expression = expression.replace(operator, f' {symbol} ')
        self.total_label.config(text=expression)

    def run(self):
        self.window.mainloop()


if __name__ == '__main__':
    Calculator().run()
