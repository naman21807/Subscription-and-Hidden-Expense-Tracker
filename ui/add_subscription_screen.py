"""Tkinter add subscription screen."""

import tkinter as tk


class AddSubscriptionFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=controller.bg_color)
        self.controller = controller

        tk.Label(
            self,
            text="Add Subscription",
            font=("Segoe UI", 28, "bold"),
            fg=controller.text_color,
            bg=controller.bg_color,
        ).pack(anchor="w", pady=(10, 6))

        tk.Label(
            self,
            text="Use YYYY-MM-DD for renewal and last used dates.",
            font=("Segoe UI", 13),
            fg=controller.muted_text,
            bg=controller.bg_color,
        ).pack(anchor="w", pady=(0, 24))

        form = tk.Frame(
            self,
            bg="white",
            highlightbackground=controller.border_color,
            highlightthickness=2,
            bd=0,
        )
        form.pack(fill="x")

        self.name_entry = self._create_entry(form, "Name", 0)
        self.cost_entry = self._create_entry(form, "Monthly Cost", 2)
        self.renewal_entry = self._create_entry(form, "Renewal Date", 4)
        self.last_used_entry = self._create_entry(form, "Last Used", 6)

        self.message_label = tk.Label(form, text="", font=("Segoe UI", 12), fg="#C0392B", bg="white")
        self.message_label.grid(row=8, column=0, columnspan=2, sticky="w", padx=30, pady=(8, 10))

        tk.Button(
            form,
            text="Save",
            font=("Segoe UI", 12, "bold"),
            fg="white",
            bg=controller.dark_pink,
            activebackground="#A91471",
            activeforeground="white",
            relief="flat",
            bd=0,
            padx=16,
            pady=10,
            command=self.save_subscription,
        ).grid(row=9, column=0, sticky="ew", padx=(30, 8), pady=(0, 24))

        tk.Button(
            form,
            text="Back to Dashboard",
            font=("Segoe UI", 12, "bold"),
            fg=controller.dark_pink,
            bg="white",
            activebackground="#FFF0F5",
            activeforeground=controller.dark_pink,
            relief="solid",
            bd=1,
            padx=16,
            pady=10,
            command=lambda: controller.show_frame("DashboardFrame"),
        ).grid(row=9, column=1, sticky="ew", padx=(8, 30), pady=(0, 24))

        form.grid_columnconfigure((0, 1), weight=1)

    def _create_entry(self, parent, label, row):
        tk.Label(
            parent,
            text=label,
            font=("Segoe UI", 13, "bold"),
            fg=self.controller.text_color,
            bg="white",
        ).grid(row=row, column=0, columnspan=2, sticky="w", padx=30, pady=(24 if row == 0 else 8, 6))

        entry = tk.Entry(parent, font=("Segoe UI", 12), relief="solid", bd=1)
        entry.grid(row=row + 1, column=0, columnspan=2, sticky="ew", padx=30, pady=(0, 8), ipady=9)
        return entry

    def refresh(self):
        self.clear_form()
        self.message_label.config(text="")

    def clear_form(self):
        for entry in (self.name_entry, self.cost_entry, self.renewal_entry, self.last_used_entry):
            entry.delete(0, tk.END)

    def save_subscription(self):
        name = self.name_entry.get()
        cost = self.cost_entry.get()
        renewal_date = self.renewal_entry.get()
        last_used = self.last_used_entry.get()

        is_valid, message = self.controller.tracker.validate_subscription_data(
            name, cost, renewal_date, last_used
        )
        if not is_valid:
            self.message_label.config(text=message, fg="#C0392B")
            return

        self.controller.tracker.add_subscription(
            user_id=self.controller.current_user_id,
            name=name,
            cost=float(cost),
            renewal_date=renewal_date,
            last_used=last_used,
        )
        self.message_label.config(text="Subscription added successfully.", fg="#2E8B57")
        self.clear_form()
