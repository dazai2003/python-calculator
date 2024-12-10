import tkinter as tk
from tkinter import ttk
import math
from datetime import datetime

class ModernCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Calculator Wimalaweera")
        self.root.geometry("400x600")
        
        # Style configuration
        self.style = ttk.Style()
        
        # Error handling variables
        self.error_timeout = None
        self.max_digits = 16  # Maximum digits allowed
        
        # History storage
        self.history = []
        
        # Main display
        self.display_var = tk.StringVar(value="0")
        self.display = ttk.Entry(
            root,
            textvariable=self.display_var,
            justify="right",
            font=("Helvetica", 40),
            state="readonly"
        )
        self.display.grid(row=0, column=0, columnspan=4, padx=10, pady=10, sticky="nsew")
        
        # History display
        self.history_frame = ttk.Frame(root)
        self.history_frame.grid(row=1, column=0, columnspan=4, sticky="nsew", padx=10)
        
        self.history_text = tk.Text(
            self.history_frame,
            height=4,
            width=30,
            font=("Helvetica", 10),
            bg="#34495e",
            fg="white"
        )
        self.history_text.pack(fill="both", expand=True)
        
        # Now apply theme after widgets are created
        self.apply_theme()
        
        # Create buttons
        self.create_buttons()
        
        # Remove info button and add copyright footer
        footer_frame = ttk.Frame(root)
        footer_frame.grid(row=7, column=0, columnspan=4, sticky="nsew", padx=2, pady=2)
        
        copyright_text = "© 2024 Vihanga Wimalaweera | @dazai2003"
        footer_label = ttk.Label(
            footer_frame,
            text=copyright_text,
            font=("Helvetica", 9),
            justify="center",
            style="Footer.TLabel"
        )
        footer_label.pack(expand=True)
        
        # Configure grid weights
        for i in range(8):
            root.grid_rowconfigure(i, weight=1)
        for i in range(4):
            root.grid_columnconfigure(i, weight=1)
            
        # Add keyboard bindings
        self.setup_keyboard_bindings()
        
        self.current_expression = "0"
        self.last_was_operator = False

    def create_buttons(self):
        buttons = [
            ('C', 2, 0, 'Operator'), ('±', 2, 1, 'Operator'), 
            ('%', 2, 2, 'Operator'), ('÷', 2, 3, 'Operator'),
            ('7', 3, 0, 'Number'), ('8', 3, 1, 'Number'), 
            ('9', 3, 2, 'Number'), ('×', 3, 3, 'Operator'),
            ('4', 4, 0, 'Number'), ('5', 4, 1, 'Number'), 
            ('6', 4, 2, 'Number'), ('-', 4, 3, 'Operator'),
            ('1', 5, 0, 'Number'), ('2', 5, 1, 'Number'), 
            ('3', 5, 2, 'Number'), ('+', 5, 3, 'Operator'),
            ('0', 6, 0, 'Number', 2), ('.', 6, 2, 'Number'), 
            ('=', 6, 3, 'Operator')
        ]
        
        for button in buttons:
            if len(button) == 5:  # For zero button that spans 2 columns
                text, row, col, style_prefix, colspan = button
                btn = ttk.Button(
                    self.root,
                    text=text,
                    style=f"{style_prefix}.TButton",
                    command=lambda t=text: self.button_click(t)
                )
                btn.grid(row=row, column=col, columnspan=colspan, sticky="nsew", padx=2, pady=2)
            else:
                text, row, col, style_prefix = button
                btn = ttk.Button(
                    self.root,
                    text=text,
                    style=f"{style_prefix}.TButton",
                    command=lambda t=text: self.button_click(t)
                )
                btn.grid(row=row, column=col, sticky="nsew", padx=2, pady=2)

    def configure_styles(self):
        # Summer sky theme
        self.root.configure(bg="#87CEEB")  # Sky blue
        self.history_text.configure(bg="#B0E2FF", fg="#2C5F7C")  # Light blue with darker text
        
        self.style.configure(
            "Custom.TButton",
            padding=10,
            font=("Helvetica", 14),
            background="#4FB4FF",  # Bright blue
            foreground="#003366"
        )
        
        self.style.configure(
            "Number.TButton",
            background="#B0E2FF",  # Soft blue
            foreground="#003366"
        )
        
        self.style.configure(
            "Operator.TButton",
            background="#FFB246",  # Warm orange like sun
            foreground="#003366"
        )
        
        self.style.configure(
            "Custom.TEntry",
            fieldbackground="#B0E2FF",
            foreground="#003366"
        )
        
        # Add footer label style
        self.style.configure(
            "Footer.TLabel",
            padding=5,
            font=("Helvetica", 9),
            background="#87CEEB",
            foreground="#003366"
        )

    def apply_theme(self):
        self.configure_styles()
        self.display.configure(style="Custom.TEntry")

    def button_click(self, value):
        try:
            if value == "C":
                self.clear_display()
            elif value == "=":
                self.calculate_result()
            elif value == "±":
                self.toggle_sign()
            elif value == "%":
                self.calculate_percentage()
            else:
                self.handle_input(value)
        except Exception as e:
            self.show_error(f"Error: {str(e)}")

    def clear_display(self):
        self.current_expression = "0"
        self.display_var.set("0")
        if self.error_timeout:
            self.root.after_cancel(self.error_timeout)

    def calculate_result(self):
        try:
            # Clean the expression
            expression = self.current_expression.replace("×", "*").replace("÷", "/")
            
            # Validate expression
            if not self.is_valid_expression(expression):
                raise ValueError("Invalid expression")
            
            # Calculate result
            result = eval(expression)
            
            # Format result
            if isinstance(result, float):
                # Handle floating point precision
                result = round(result, 10)
                # Remove trailing zeros
                result = f"{result:g}"
            
            # Check result length
            if len(str(result)) > self.max_digits:
                raise ValueError("Result too large")
            
            # Add to history
            timestamp = datetime.now().strftime("%H:%M:%S")
            history_entry = f"{timestamp}: {self.current_expression} = {result}\n"
            self.history.append(history_entry)
            self.history_text.insert("1.0", history_entry)
            
            self.current_expression = str(result)
            self.display_var.set(result)
            
        except Exception as e:
            self.show_error(str(e))

    def toggle_sign(self):
        try:
            if self.current_expression.startswith("-"):
                self.current_expression = self.current_expression[1:]
            else:
                self.current_expression = "-" + self.current_expression
            self.display_var.set(self.current_expression)
        except Exception as e:
            self.show_error(str(e))

    def calculate_percentage(self):
        try:
            value = float(eval(self.current_expression))
            result = value / 100
            self.current_expression = str(result)
            self.display_var.set(result)
        except Exception as e:
            self.show_error("Invalid percentage calculation")

    def handle_input(self, value):
        if len(self.current_expression) >= self.max_digits:
            self.show_error("Maximum digits reached")
            return
        
        if self.current_expression == "0" and value not in "±%÷×+-":
            self.current_expression = value
        else:
            if self.is_valid_input(value):
                self.current_expression += value
        
        self.display_var.set(self.current_expression)

    def is_valid_expression(self, expression):
        # Check for invalid patterns
        invalid_patterns = ["**", "//", "++", "--"]
        for pattern in invalid_patterns:
            if pattern in expression:
                return False
        
        # Check for valid characters
        valid_chars = set("0123456789+-*/.() ")
        if not all(c in valid_chars for c in expression):
            return False
        
        return True

    def is_valid_input(self, value):
        # Prevent multiple decimal points
        if value == "." and "." in self.current_expression:
            return False
        
        # Prevent multiple operators
        if value in "±%÷×+-" and self.current_expression[-1] in "±%÷×+-":
            return False
        
        return True

    def show_error(self, message):
        self.display_var.set(f"Error: {message}")
        self.current_expression = "0"
        
        # Clear error message after 2 seconds
        if self.error_timeout:
            self.root.after_cancel(self.error_timeout)
        self.error_timeout = self.root.after(2000, self.clear_display)

    def setup_keyboard_bindings(self):
        # Number keys (both main keyboard and numpad)
        for i in range(10):
            self.root.bind(str(i), lambda e, num=str(i): self.button_click(num))
            self.root.bind(f"<KP_{i}>", lambda e, num=str(i): self.button_click(num))
        
        # Operators
        self.root.bind("+", lambda e: self.button_click("+"))
        self.root.bind("<KP_Add>", lambda e: self.button_click("+"))
        self.root.bind("-", lambda e: self.button_click("-"))
        self.root.bind("<KP_Subtract>", lambda e: self.button_click("-"))
        self.root.bind("*", lambda e: self.button_click("×"))
        self.root.bind("<KP_Multiply>", lambda e: self.button_click("×"))
        self.root.bind("/", lambda e: self.button_click("÷"))
        self.root.bind("<KP_Divide>", lambda e: self.button_click("÷"))
        
        # Decimal point
        self.root.bind(".", lambda e: self.button_click("."))
        self.root.bind("<KP_Decimal>", lambda e: self.button_click("."))
        
        # Enter and Return for equals
        self.root.bind("<Return>", lambda e: self.button_click("="))
        self.root.bind("<KP_Enter>", lambda e: self.button_click("="))
        
        # Backspace and Delete for clear
        self.root.bind("<BackSpace>", lambda e: self.handle_backspace())
        self.root.bind("<Delete>", lambda e: self.button_click("C"))
        
        # Escape to clear
        self.root.bind("<Escape>", lambda e: self.button_click("C"))
        
        # Percentage
        self.root.bind("%", lambda e: self.button_click("%"))
        
        # Plus/minus (using 'n' key)
        self.root.bind("n", lambda e: self.button_click("±"))

    def handle_backspace(self):
        if self.current_expression and self.current_expression != "0":
            if len(self.current_expression) == 1:
                self.current_expression = "0"
            else:
                self.current_expression = self.current_expression[:-1]
            self.display_var.set(self.current_expression)

def main():
    root = tk.Tk()
    app = ModernCalculator(root)
    root.mainloop()

if __name__ == "__main__":
    main() 