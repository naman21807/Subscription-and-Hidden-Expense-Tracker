"""Add subscription screen."""

import customtkinter as ctk


class AddSubscriptionFrame(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="transparent")
        self.controller = controller

        ctk.CTkLabel(
            self,
            text="Add Subscription",
            font=("Segoe UI", 30, "bold"),
            text_color=self.controller.text_color,
        ).pack(anchor="w", pady=(10, 4))

        ctk.CTkLabel(
            self,
            text="Use YYYY-MM-DD for renewal and last used dates.",
            font=("Segoe UI", 14),
            text_color=self.controller.muted_text,
        ).pack(anchor="w", pady=(0, 24))

        form = ctk.CTkFrame(
            self,
            fg_color=self.controller.card_bg,
            corner_radius=24,
            border_width=2,
            border_color=self.controller.border_color,
        )
        form.pack(fill="x", ipadx=10, ipady=10)

        self.name_entry = self._create_labeled_entry(form, "Name")
        self.cost_entry = self._create_labeled_entry(form, "Monthly Cost")
        self.renewal_entry = self._create_labeled_entry(form, "Renewal Date")
        self.last_used_entry = self._create_labeled_entry(form, "Last Used")

        self.message_label = ctk.CTkLabel(
            form,
            text="",
            font=("Segoe UI", 13),
            text_color=self.controller.dark_pink,
        )
        self.message_label.pack(anchor="w", padx=30, pady=(8, 10))

        button_row = ctk.CTkFrame(form, fg_color="transparent")
        button_row.pack(fill="x", padx=30, pady=(0, 20))
        button_row.grid_columnconfigure((0, 1), weight=1)

        ctk.CTkButton(
            button_row,
            text="Save",
            fg_color=self.controller.dark_pink,
            hover_color="#A91471",
            height=42,
            corner_radius=14,
            font=("Segoe UI", 14, "bold"),
            command=self.save_subscription,
        ).grid(row=0, column=0, padx=(0, 8), sticky="ew")

        ctk.CTkButton(
            button_row,
            text="Back to Dashboard",
            fg_color="white",
            text_color=self.controller.dark_pink,
            border_width=2,
            border_color=self.controller.dark_pink,
            hover_color="#FFF0F5",
            height=42,
            corner_radius=14,
            font=("Segoe UI", 14, "bold"),
            command=lambda: self.controller.show_frame("DashboardFrame"),
        ).grid(row=0, column=1, padx=(8, 0), sticky="ew")

    def _create_labeled_entry(self, parent, label):
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
        )
        entry.pack(fill="x", padx=30, pady=(0, 16))
        return entry

    def refresh(self):
        self.clear_form()
        self.message_label.configure(text="")

    def clear_form(self):
        for entry in (
            self.name_entry,
            self.cost_entry,
            self.renewal_entry,
            self.last_used_entry,
        ):
            entry.delete(0, "end")

    def save_subscription(self):
        name = self.name_entry.get()
        cost = self.cost_entry.get()
        renewal_date = self.renewal_entry.get()
        last_used = self.last_used_entry.get()

        is_valid, message = self.controller.tracker.validate_subscription_data(
            name,
            cost,
            renewal_date,
            last_used,
        )
        if not is_valid:
            self.message_label.configure(text=message, text_color="#C0392B")
            return

        self.controller.tracker.add_subscription(
            user_id=self.controller.current_user_id,
            name=name,
            cost=float(cost),
            renewal_date=renewal_date,
            last_used=last_used,
        )
        self.message_label.configure(
            text="Subscription added successfully.",
            text_color="#2E8B57",
        )
        self.clear_form()
