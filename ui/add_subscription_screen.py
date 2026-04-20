"""Add subscription screen."""

import tkinter as tk


class AddSubscriptionFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#f4f6f8")
        self.controller = controller

        form = tk.Frame(self, bg="white", padx=25, pady=25)
        form.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(
            form,
            text="Add Subscription",
            font=("Arial", 16, "bold"),
            bg="white",
        ).grid(row=0, column=0, columnspan=2, pady=(0, 20))

        tk.Label(form, text="Name", bg="white").grid(row=1, column=0, sticky="w", pady=5)
        self.name_entry = tk.Entry(form, width=30)
        self.name_entry.grid(row=1, column=1, pady=5)

        tk.Label(form, text="Monthly Cost", bg="white").grid(row=2, column=0, sticky="w", pady=5)
        self.cost_entry = tk.Entry(form, width=30)
        self.cost_entry.grid(row=2, column=1, pady=5)

        tk.Label(form, text="Renewal Date", bg="white").grid(row=3, column=0, sticky="w", pady=5)
        self.renewal_entry = tk.Entry(form, width=30)
        self.renewal_entry.grid(row=3, column=1, pady=5)

        tk.Label(form, text="Last Used", bg="white").grid(row=4, column=0, sticky="w", pady=5)
        self.last_used_entry = tk.Entry(form, width=30)
        self.last_used_entry.grid(row=4, column=1, pady=5)

        tk.Label(
            form,
            text="Use YYYY-MM-DD format for dates.",
            bg="white",
            fg="#555555",
        ).grid(row=5, column=0, columnspan=2, pady=(5, 10))

        self.message_label = tk.Label(form, text="", bg="white", fg="red")
        self.message_label.grid(row=6, column=0, columnspan=2, pady=(0, 10))

        button_row = tk.Frame(form, bg="white")
        button_row.grid(row=7, column=0, columnspan=2)

        tk.Button(button_row, text="Save", width=12, command=self.save_subscription).grid(row=0, column=0, padx=5)
        tk.Button(
            button_row,
            text="Back",
            width=12,
            command=lambda: controller.show_frame("DashboardFrame"),
        ).grid(row=0, column=1, padx=5)

    def refresh(self):
        self.clear_form()
        self.message_label.config(text="")

    def clear_form(self):
        for entry in (
            self.name_entry,
            self.cost_entry,
            self.renewal_entry,
            self.last_used_entry,
        ):
            entry.delete(0, tk.END)

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
            self.message_label.config(text=message, fg="red")
            return

        self.controller.tracker.add_subscription(
            user_id=self.controller.current_user_id,
            name=name,
            cost=float(cost),
            renewal_date=renewal_date,
            last_used=last_used,
        )
        self.message_label.config(text="Subscription added successfully.", fg="green")
        self.clear_form()
