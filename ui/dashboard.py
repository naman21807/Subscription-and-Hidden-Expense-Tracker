"""Tkinter dashboard screen."""

import tkinter as tk


class DashboardFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=controller.bg_color)
        self.controller = controller

    def refresh(self):
        for child in self.winfo_children():
            child.destroy()

        user_id = self.controller.current_user_id
        if not user_id:
            return

        subscriptions = self.controller.tracker.get_subscriptions(user_id)
        monthly_total = self.controller.tracker.total_monthly_cost(user_id)
        yearly_total = self.controller.tracker.total_yearly_cost(user_id)
        upcoming = self.controller.tracker.upcoming_renewals(user_id)
        unused = self.controller.tracker.unused_subscriptions(user_id)

        tk.Label(
            self,
            text="Dashboard",
            font=("Segoe UI", 28, "bold"),
            fg=self.controller.text_color,
            bg=self.controller.bg_color,
        ).pack(anchor="w", pady=(10, 6))

        tk.Label(
            self,
            text="Here is your subscription breakdown for this month.",
            font=("Segoe UI", 13),
            fg=self.controller.muted_text,
            bg=self.controller.bg_color,
        ).pack(anchor="w", pady=(0, 24))

        stats = tk.Frame(self, bg=self.controller.bg_color)
        stats.pack(fill="x", pady=(0, 24))

        self._stat_card(stats, "Monthly Total", f"Rs. {monthly_total:.2f}", f"{len(subscriptions)} active", 0)
        self._stat_card(stats, "Upcoming", str(len(upcoming)), "within 7 days", 1)
        self._stat_card(stats, "Yearly Total", f"Rs. {yearly_total:.2f}", f"{len(unused)} unused", 2)

        actions = tk.Frame(
            self,
            bg="white",
            highlightbackground=self.controller.border_color,
            highlightthickness=2,
            bd=0,
        )
        actions.pack(fill="x", pady=(0, 24))

        tk.Label(
            actions,
            text="Quick Actions",
            font=("Segoe UI", 16, "bold"),
            fg=self.controller.dark_pink,
            bg="white",
        ).pack(anchor="w", padx=24, pady=(20, 12))

        row = tk.Frame(actions, bg="white")
        row.pack(fill="x", padx=24, pady=(0, 20))
        row.grid_columnconfigure((0, 1), weight=1)

        tk.Button(
            row,
            text="Add Subscription",
            font=("Segoe UI", 12, "bold"),
            fg="white",
            bg=self.controller.dark_pink,
            activebackground="#A91471",
            activeforeground="white",
            relief="flat",
            bd=0,
            padx=16,
            pady=10,
            command=lambda: self.controller.show_frame("AddSubscriptionFrame"),
        ).grid(row=0, column=0, sticky="ew", padx=(0, 8))

        tk.Button(
            row,
            text="View Subscriptions",
            font=("Segoe UI", 12, "bold"),
            fg=self.controller.dark_pink,
            bg="white",
            activebackground="#FFF0F5",
            activeforeground=self.controller.dark_pink,
            relief="solid",
            bd=1,
            padx=16,
            pady=10,
            command=lambda: self.controller.show_frame("ViewSubscriptionsFrame"),
        ).grid(row=0, column=1, sticky="ew", padx=(8, 0))

        lists = tk.Frame(self, bg=self.controller.bg_color)
        lists.pack(fill="both", expand=True)
        lists.grid_columnconfigure((0, 1), weight=1)

        self._list_card(lists, "Upcoming Renewals", self._format_upcoming(upcoming), 0)
        self._list_card(lists, "Unused Subscriptions", self._format_unused(unused), 1)

    def _stat_card(self, parent, title, value, subtext, column):
        card = tk.Frame(
            parent,
            bg="white",
            highlightbackground=self.controller.border_color,
            highlightthickness=2,
            bd=0,
            padx=20,
            pady=20,
        )
        card.grid(row=0, column=column, sticky="nsew", padx=(0 if column == 0 else 16, 0))
        parent.grid_columnconfigure(column, weight=1)

        tk.Label(card, text=title, font=("Segoe UI", 12), fg="gray", bg="white").pack(anchor="w")
        tk.Label(card, text=value, font=("Segoe UI", 22, "bold"), fg=self.controller.dark_pink, bg="white").pack(anchor="w")
        tk.Label(card, text=subtext, font=("Segoe UI", 10), fg="#999999", bg="white").pack(anchor="w")

    def _list_card(self, parent, title, content, column):
        card = tk.Frame(
            parent,
            bg="white",
            highlightbackground=self.controller.border_color,
            highlightthickness=2,
            bd=0,
        )
        card.grid(row=0, column=column, sticky="nsew", padx=(0, 10) if column == 0 else (10, 0))

        tk.Label(
            card,
            text=title,
            font=("Segoe UI", 16, "bold"),
            fg=self.controller.dark_pink,
            bg="white",
        ).pack(anchor="w", padx=20, pady=(20, 10))

        text = tk.Text(card, height=12, relief="flat", bd=0, font=("Segoe UI", 12), fg="#555555", bg="white")
        text.insert("1.0", content)
        text.config(state="disabled")
        text.pack(fill="both", expand=True, padx=16, pady=(0, 16))

    def _format_upcoming(self, subscriptions):
        if not subscriptions:
            return "No renewals in the next 7 days."
        return "\n".join(
            f"- {subscription.name} | Rs. {subscription.cost:.2f} | Renews: {subscription.upcoming_renewal_date().isoformat()}"
            for subscription in subscriptions
        )

    def _format_unused(self, subscriptions):
        if not subscriptions:
            return "No unused subscriptions found."
        return "\n".join(
            f"- {subscription.name} | Rs. {subscription.cost:.2f} | Last used: {subscription.last_used}"
            for subscription in subscriptions
        )
