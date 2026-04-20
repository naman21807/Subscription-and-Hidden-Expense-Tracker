"""View subscriptions screen."""

import customtkinter as ctk


class ViewSubscriptionsFrame(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="transparent")
        self.controller = controller

        ctk.CTkLabel(
            self,
            text="Your Subscriptions",
            font=("Segoe UI", 30, "bold"),
            text_color=self.controller.text_color,
        ).pack(anchor="w", pady=(10, 4))

        ctk.CTkLabel(
            self,
            text="A full list of every saved plan.",
            font=("Segoe UI", 14),
            text_color=self.controller.muted_text,
        ).pack(anchor="w", pady=(0, 24))

        self.card = ctk.CTkFrame(
            self,
            fg_color=self.controller.card_bg,
            corner_radius=24,
            border_width=2,
            border_color=self.controller.border_color,
        )
        self.card.pack(fill="both", expand=True)

    def refresh(self):
        for child in self.card.winfo_children():
            child.destroy()

        user_id = self.controller.current_user_id
        if not user_id:
            return

        subscriptions = self.controller.tracker.get_subscriptions(user_id)
        if not subscriptions:
            ctk.CTkLabel(
                self.card,
                text="No subscriptions added yet.",
                font=("Segoe UI", 15),
                text_color=self.controller.muted_text,
            ).pack(anchor="w", padx=24, pady=24)
            return

        for subscription in subscriptions:
            item = ctk.CTkFrame(self.card, fg_color="#FFF9FB", corner_radius=18)
            item.pack(fill="x", padx=20, pady=(16, 0))

            ctk.CTkLabel(
                item,
                text=subscription.name,
                font=("Segoe UI", 18, "bold"),
                text_color=self.controller.dark_pink,
            ).pack(anchor="w", padx=18, pady=(14, 4))

            detail = (
                f"Monthly Cost: Rs. {subscription.cost:.2f}\n"
                f"Renewal Date: {subscription.renewal_date}\n"
                f"Last Used: {subscription.last_used}"
            )
            ctk.CTkLabel(
                item,
                text=detail,
                font=("Segoe UI", 13),
                text_color=self.controller.text_color,
                justify="left",
            ).pack(anchor="w", padx=18, pady=(0, 14))
