"""View subscriptions screen."""

import tkinter as tk


class ViewSubscriptionsFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#f4f6f8")
        self.controller = controller

        container = tk.Frame(self, bg="white", padx=20, pady=20)
        container.pack(fill="both", expand=True, padx=25, pady=25)

        top_row = tk.Frame(container, bg="white")
        top_row.pack(fill="x")

        tk.Label(
            top_row,
            text="Your Subscriptions",
            font=("Arial", 16, "bold"),
            bg="white",
        ).pack(side="left")

        tk.Button(
            top_row,
            text="Back",
            command=lambda: controller.show_frame("DashboardFrame"),
        ).pack(side="right")

        self.listbox = tk.Listbox(container, width=100, height=24)
        self.listbox.pack(fill="both", expand=True, pady=(20, 0))

    def refresh(self):
        self.listbox.delete(0, tk.END)
        user_id = self.controller.current_user_id

        if not user_id:
            return

        subscriptions = self.controller.tracker.get_subscriptions(user_id)
        if not subscriptions:
            self.listbox.insert(tk.END, "No subscriptions added yet.")
            return

        for subscription in subscriptions:
            line = (
                f"Name: {subscription.name} | "
                f"Monthly Cost: Rs. {subscription.cost:.2f} | "
                f"Renewal Date: {subscription.renewal_date} | "
                f"Last Used: {subscription.last_used}"
            )
            self.listbox.insert(tk.END, line)
