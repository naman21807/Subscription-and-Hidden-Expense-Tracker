"""Dashboard screen."""

import tkinter as tk


class DashboardFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#eef2f5")
        self.controller = controller

        header = tk.Frame(self, bg="#1f4e79", padx=20, pady=15)
        header.pack(fill="x")

        tk.Label(
            header,
            text="Dashboard",
            font=("Arial", 18, "bold"),
            fg="white",
            bg="#1f4e79",
        ).pack(side="left")

        tk.Button(header, text="Logout", command=self.controller.logout_user).pack(side="right")

        summary = tk.Frame(self, bg="#eef2f5", padx=20, pady=20)
        summary.pack(fill="x")

        self.monthly_label = tk.Label(summary, text="Monthly Expense: Rs. 0.00", font=("Arial", 13), bg="#eef2f5")
        self.monthly_label.pack(anchor="w", pady=5)

        self.yearly_label = tk.Label(summary, text="Yearly Expense: Rs. 0.00", font=("Arial", 13), bg="#eef2f5")
        self.yearly_label.pack(anchor="w", pady=5)

        action_frame = tk.Frame(self, bg="#eef2f5")
        action_frame.pack(fill="x", padx=20, pady=(0, 20))

        tk.Button(
            action_frame,
            text="Add Subscription",
            width=20,
            command=lambda: controller.show_frame("AddSubscriptionFrame"),
        ).pack(side="left", padx=(0, 10))

        tk.Button(
            action_frame,
            text="View Subscriptions",
            width=20,
            command=lambda: controller.show_frame("ViewSubscriptionsFrame"),
        ).pack(side="left")

        lists_frame = tk.Frame(self, bg="#eef2f5", padx=20, pady=10)
        lists_frame.pack(fill="both", expand=True)

        left_frame = tk.Frame(lists_frame, bg="white", padx=15, pady=15)
        left_frame.pack(side="left", fill="both", expand=True, padx=(0, 10))

        right_frame = tk.Frame(lists_frame, bg="white", padx=15, pady=15)
        right_frame.pack(side="left", fill="both", expand=True)

        tk.Label(left_frame, text="Upcoming Renewals", font=("Arial", 12, "bold"), bg="white").pack(anchor="w")
        self.upcoming_listbox = tk.Listbox(left_frame, width=40, height=15)
        self.upcoming_listbox.pack(fill="both", expand=True, pady=(10, 0))

        tk.Label(right_frame, text="Unused Subscriptions", font=("Arial", 12, "bold"), bg="white").pack(anchor="w")
        self.unused_listbox = tk.Listbox(right_frame, width=40, height=15)
        self.unused_listbox.pack(fill="both", expand=True, pady=(10, 0))

    def refresh(self):
        user_id = self.controller.current_user_id
        if not user_id:
            return

        monthly_total = self.controller.tracker.total_monthly_cost(user_id)
        yearly_total = self.controller.tracker.total_yearly_cost(user_id)
        self.monthly_label.config(text=f"Monthly Expense: Rs. {monthly_total:.2f}")
        self.yearly_label.config(text=f"Yearly Expense: Rs. {yearly_total:.2f}")

        self.upcoming_listbox.delete(0, tk.END)
        for subscription in self.controller.tracker.upcoming_renewals(user_id):
            display_text = f"{subscription.name} - {subscription.upcoming_renewal_date()}"
            self.upcoming_listbox.insert(tk.END, display_text)

        if self.upcoming_listbox.size() == 0:
            self.upcoming_listbox.insert(tk.END, "No renewals in the next 7 days.")

        self.unused_listbox.delete(0, tk.END)
        for subscription in self.controller.tracker.unused_subscriptions(user_id):
            display_text = f"{subscription.name} - Last used: {subscription.last_used}"
            self.unused_listbox.insert(tk.END, display_text)

        if self.unused_listbox.size() == 0:
            self.unused_listbox.insert(tk.END, "No unused subscriptions found.")
