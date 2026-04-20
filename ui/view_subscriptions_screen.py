"""Tkinter subscriptions list screen."""

import tkinter as tk


class ViewSubscriptionsFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=controller.bg_color)
        self.controller = controller

        tk.Label(
            self,
            text="Your Subscriptions",
            font=("Segoe UI", 28, "bold"),
            fg=controller.text_color,
            bg=controller.bg_color,
        ).pack(anchor="w", pady=(10, 6))

        tk.Label(
            self,
            text="A full list of every saved plan.",
            font=("Segoe UI", 13),
            fg=controller.muted_text,
            bg=controller.bg_color,
        ).pack(anchor="w", pady=(0, 24))

        self.card = tk.Frame(
            self,
            bg="white",
            highlightbackground=controller.border_color,
            highlightthickness=2,
            bd=0,
        )
        self.card.pack(fill="both", expand=True)

    def refresh(self):
        for child in self.card.winfo_children():
            child.destroy()

        subscriptions = self.controller.tracker.get_subscriptions(self.controller.current_user_id)
        if not subscriptions:
            tk.Label(
                self.card,
                text="No subscriptions added yet.",
                font=("Segoe UI", 13),
                fg=self.controller.muted_text,
                bg="white",
            ).pack(anchor="w", padx=24, pady=24)
            return

        for subscription in subscriptions:
            item = tk.Frame(
                self.card,
                bg="#FFF9FB",
                highlightbackground=self.controller.border_color,
                highlightthickness=1,
                bd=0,
            )
            item.pack(fill="x", padx=20, pady=(16, 0))

            tk.Label(
                item,
                text=subscription.name,
                font=("Segoe UI", 16, "bold"),
                fg=self.controller.dark_pink,
                bg="#FFF9FB",
            ).pack(anchor="w", padx=16, pady=(14, 4))

            tk.Label(
                item,
                text=(
                    f"Monthly Cost: Rs. {subscription.cost:.2f}\n"
                    f"Renewal Date: {subscription.renewal_date}\n"
                    f"Last Used: {subscription.last_used}"
                ),
                font=("Segoe UI", 12),
                fg=self.controller.text_color,
                bg="#FFF9FB",
                justify="left",
            ).pack(anchor="w", padx=16, pady=(0, 14))
