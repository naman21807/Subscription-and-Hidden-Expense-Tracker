"""Login and signup screen."""

import customtkinter as ctk


class LoginFrame(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color=controller.bg_color)
        self.controller = controller

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        card = ctk.CTkFrame(
            self,
            width=420,
            corner_radius=24,
            fg_color=controller.card_bg,
            border_width=2,
            border_color=controller.border_color,
        )
        card.grid(row=0, column=0, padx=30, pady=30)

        ctk.CTkLabel(
            card,
            text=controller.app_name,
            font=("Segoe UI", 30, "bold"),
            text_color=controller.dark_pink,
        ).pack(anchor="w", padx=30, pady=(30, 8))

        ctk.CTkLabel(
            card,
            text="Track subscriptions and spot waste before renewals hit.",
            font=("Segoe UI", 14),
            text_color=controller.muted_text,
            wraplength=320,
            justify="left",
        ).pack(anchor="w", padx=30, pady=(0, 24))

        self.username_entry = self._create_labeled_entry(card, "Username")
        self.password_entry = self._create_labeled_entry(card, "Password", show="*")

        self.message_label = ctk.CTkLabel(
            card,
            text="",
            font=("Segoe UI", 13),
            text_color=controller.dark_pink,
        )
        self.message_label.pack(anchor="w", padx=30, pady=(16, 6))

        button_row = ctk.CTkFrame(card, fg_color="transparent")
        button_row.pack(fill="x", padx=30, pady=(8, 30))
        button_row.grid_columnconfigure((0, 1), weight=1)

        ctk.CTkButton(
            button_row,
            text="Login",
            fg_color=controller.dark_pink,
            hover_color="#A91471",
            height=42,
            corner_radius=14,
            font=("Segoe UI", 14, "bold"),
            command=self.login,
        ).grid(row=0, column=0, padx=(0, 8), sticky="ew")

        ctk.CTkButton(
            button_row,
            text="Sign Up",
            fg_color="white",
            text_color=controller.dark_pink,
            border_width=2,
            border_color=controller.dark_pink,
            hover_color="#FFF0F5",
            height=42,
            corner_radius=14,
            font=("Segoe UI", 14, "bold"),
            command=self.signup,
        ).grid(row=0, column=1, padx=(8, 0), sticky="ew")

    def _create_labeled_entry(self, parent, label, show=None):
        ctk.CTkLabel(
            parent,
            text=label,
            font=("Segoe UI", 14, "bold"),
            text_color=self.controller.text_color,
        ).pack(anchor="w", padx=30, pady=(0, 6))

        entry = ctk.CTkEntry(
            parent,
            width=340,
            height=42,
            corner_radius=12,
            border_color="#F1B6C8",
            fg_color="#FFF9FB",
            text_color=self.controller.text_color,
            show=show,
        )
        entry.pack(fill="x", padx=30, pady=(0, 16))
        return entry

    def refresh(self):
        self.password_entry.delete(0, "end")
        self.message_label.configure(text="")

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        success, result = self.controller.auth_manager.login(username, password)

        if success:
            self.message_label.configure(text="Login successful.", text_color="#2E8B57")
            self.controller.login_user(result)
        else:
            self.message_label.configure(text=result, text_color="#C0392B")

    def signup(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        success, result = self.controller.auth_manager.signup(username, password)

        if success:
            self.message_label.configure(
                text="Signup successful. Please log in.",
                text_color="#2E8B57",
            )
            self.password_entry.delete(0, "end")
        else:
            self.message_label.configure(text=result, text_color="#C0392B")
