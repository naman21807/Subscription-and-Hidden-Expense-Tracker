"""Tkinter login screen."""

import tkinter as tk


class LoginFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=controller.bg_color)
        self.controller = controller

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        card = tk.Frame(
            self,
            bg="white",
            highlightbackground=controller.border_color,
            highlightthickness=2,
            bd=0,
        )
        card.grid(row=0, column=0, padx=30, pady=30)

        tk.Label(
            card,
            text=controller.app_name,
            font=("Segoe UI", 28, "bold"),
            fg=controller.dark_pink,
            bg="white",
        ).grid(row=0, column=0, columnspan=2, sticky="w", padx=30, pady=(30, 8))

        tk.Label(
            card,
            text="Track subscriptions and spot waste before renewals hit.",
            font=("Segoe UI", 13),
            fg=controller.muted_text,
            bg="white",
            wraplength=320,
            justify="left",
        ).grid(row=1, column=0, columnspan=2, sticky="w", padx=30, pady=(0, 24))

        self.username_entry = self._create_labeled_entry(card, "Username", 2)
        self.password_entry = self._create_labeled_entry(card, "Password", 4, show="*")

        self.message_label = tk.Label(
            card,
            text="",
            font=("Segoe UI", 12),
            fg="#C0392B",
            bg="white",
        )
        self.message_label.grid(row=6, column=0, columnspan=2, sticky="w", padx=30, pady=(12, 8))

        tk.Button(
            card,
            text="Login",
            font=("Segoe UI", 12, "bold"),
            fg="white",
            bg=controller.dark_pink,
            activebackground="#A91471",
            activeforeground="white",
            relief="flat",
            bd=0,
            padx=16,
            pady=10,
            command=self.login,
        ).grid(row=7, column=0, sticky="ew", padx=(30, 8), pady=(0, 30))

        tk.Button(
            card,
            text="Sign Up",
            font=("Segoe UI", 12, "bold"),
            fg=controller.dark_pink,
            bg="white",
            activebackground="#FFF0F5",
            activeforeground=controller.dark_pink,
            relief="solid",
            bd=1,
            padx=16,
            pady=10,
            command=self.signup,
        ).grid(row=7, column=1, sticky="ew", padx=(8, 30), pady=(0, 30))

    def _create_labeled_entry(self, parent, label, row, show=None):
        tk.Label(
            parent,
            text=label,
            font=("Segoe UI", 13, "bold"),
            fg=self.controller.text_color,
            bg="white",
        ).grid(row=row, column=0, columnspan=2, sticky="w", padx=30, pady=(0, 6))

        entry = tk.Entry(parent, font=("Segoe UI", 12), relief="solid", bd=1, show=show)
        entry.grid(row=row + 1, column=0, columnspan=2, sticky="ew", padx=30, pady=(0, 14), ipady=9)
        return entry

    def refresh(self):
        self.password_entry.delete(0, tk.END)
        self.message_label.config(text="")

    def login(self):
        success, result = self.controller.auth_manager.login(
            self.username_entry.get(),
            self.password_entry.get(),
        )
        if success:
            self.message_label.config(text="Login successful.", fg="#2E8B57")
            self.controller.login_user(result)
        else:
            self.message_label.config(text=result, fg="#C0392B")

    def signup(self):
        success, result = self.controller.auth_manager.signup(
            self.username_entry.get(),
            self.password_entry.get(),
        )
        if success:
            self.message_label.config(text="Signup successful. Please log in.", fg="#2E8B57")
            self.password_entry.delete(0, tk.END)
        else:
            self.message_label.config(text=result, fg="#C0392B")
