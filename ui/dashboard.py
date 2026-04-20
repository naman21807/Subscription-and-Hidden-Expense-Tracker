"""Dashboard screen."""

import customtkinter as ctk


class DashboardFrame(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="transparent")
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

        ctk.CTkLabel(
            self,
            text="Hey There!",
            font=("Segoe UI", 32, "bold"),
            text_color=self.controller.text_color,
        ).pack(anchor="w", pady=(10, 0))

        ctk.CTkLabel(
            self,
            text="Here is your subscription breakdown for this month.",
            font=("Segoe UI", 14),
            text_color=self.controller.muted_text,
        ).pack(anchor="w", pady=(0, 30))

        stats_frame = ctk.CTkFrame(self, fg_color="transparent")
        stats_frame.pack(fill="x", pady=10)

        self._create_stat_card(
            stats_frame,
            "Monthly Total",
            f"Rs. {monthly_total:.2f}",
            f"{len(subscriptions)} active subscriptions",
            self.controller.accent_pink,
        )
        self._create_stat_card(
            stats_frame,
            "Upcoming Renewals",
            str(len(upcoming)),
            "Due within the next 7 days",
            self.controller.dark_pink,
        )
        self._create_stat_card(
            stats_frame,
            "Yearly Total",
            f"Rs. {yearly_total:.2f}",
            f"{len(unused)} potentially unused subscriptions",
            "#FF82AB",
        )

        action_box = ctk.CTkFrame(
            self,
            fg_color=self.controller.card_bg,
            corner_radius=20,
            border_width=2,
            border_color=self.controller.border_color,
        )
        action_box.pack(fill="x", pady=30, ipady=20)

        ctk.CTkLabel(
            action_box,
            text="Quick Actions",
            font=("Segoe UI", 18, "bold"),
            text_color=self.controller.dark_pink,
        ).pack(anchor="w", padx=25, pady=(15, 10))

        btn_row = ctk.CTkFrame(action_box, fg_color="transparent")
        btn_row.pack(fill="x", padx=20)
        btn_row.grid_columnconfigure((0, 1), weight=1)

        ctk.CTkButton(
            btn_row,
            text="+ Add Subscription",
            fg_color=self.controller.dark_pink,
            hover_color="#A91471",
            corner_radius=15,
            height=45,
            font=("Segoe UI", 14, "bold"),
            command=lambda: self.controller.show_frame("AddSubscriptionFrame"),
        ).grid(row=0, column=0, padx=(0, 6), sticky="ew")

        ctk.CTkButton(
            btn_row,
            text="View Subscriptions",
            fg_color="white",
            border_width=2,
            border_color=self.controller.dark_pink,
            text_color=self.controller.dark_pink,
            hover_color="#FFF0F5",
            corner_radius=15,
            height=45,
            font=("Segoe UI", 14, "bold"),
            command=lambda: self.controller.show_frame("ViewSubscriptionsFrame"),
        ).grid(row=0, column=1, padx=(6, 0), sticky="ew")

        bottom_grid = ctk.CTkFrame(self, fg_color="transparent")
        bottom_grid.pack(fill="both", expand=True)
        bottom_grid.grid_columnconfigure((0, 1), weight=1)

        upcoming_text = self._format_subscription_list(
            upcoming,
            empty_message="No renewals in the next 7 days.",
            include_usage=False,
        )
        unused_text = self._format_subscription_list(
            unused,
            empty_message="No unused subscriptions found.",
            include_usage=True,
        )

        self._create_list_box(bottom_grid, "Upcoming Renewals", upcoming_text, 0)
        self._create_list_box(bottom_grid, "Unused Subscriptions", unused_text, 1)

    def _create_stat_card(self, parent, title, value, subtext, accent):
        card = ctk.CTkFrame(
            parent,
            fg_color=self.controller.card_bg,
            corner_radius=20,
            width=240,
            height=140,
            border_width=2,
            border_color=self.controller.border_color,
        )
        card.pack(side="left", padx=(0, 20), expand=True, fill="both")
        card.pack_propagate(False)

        ctk.CTkLabel(card, text=title, font=("Segoe UI", 13), text_color="gray").pack(
            anchor="w", padx=20, pady=(20, 0)
        )
        ctk.CTkLabel(
            card,
            text=value,
            font=("Segoe UI", 26, "bold"),
            text_color=accent,
        ).pack(anchor="w", padx=20)
        ctk.CTkLabel(
            card,
            text=subtext,
            font=("Segoe UI", 11, "italic"),
            text_color="#999999",
        ).pack(anchor="w", padx=20, pady=(5, 0))

    def _create_list_box(self, parent, title, content, column):
        frame = ctk.CTkFrame(
            parent,
            fg_color=self.controller.card_bg,
            corner_radius=20,
            border_width=2,
            border_color=self.controller.border_color,
        )
        left_pad = 10 if column == 0 else 0
        right_pad = 0 if column == 0 else 10
        frame.grid(row=0, column=column, padx=(left_pad, right_pad), sticky="nsew")

        ctk.CTkLabel(
            frame,
            text=title,
            font=("Segoe UI", 18, "bold"),
            text_color=self.controller.dark_pink,
        ).pack(anchor="w", padx=20, pady=(20, 10))

        box = ctk.CTkTextbox(
            frame,
            fg_color="transparent",
            text_color="#555555",
            font=("Segoe UI", 13),
            height=180,
            border_width=0,
        )
        box.insert("0.0", content)
        box.configure(state="disabled")
        box.pack(fill="both", expand=True, padx=15, pady=10)

    def _format_subscription_list(self, subscriptions, empty_message, include_usage):
        if not subscriptions:
            return empty_message

        lines = []
        for subscription in subscriptions:
            line = f"- {subscription.name} | Rs. {subscription.cost:.2f}"
            if include_usage:
                line += f" | Last used: {subscription.last_used}"
            else:
                line += f" | Renews: {subscription.upcoming_renewal_date().isoformat()}"
            lines.append(line)
        return "\n".join(lines)
