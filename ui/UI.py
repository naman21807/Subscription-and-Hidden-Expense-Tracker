"""CustomTkinter application UI."""

from __future__ import annotations

from tkinter import messagebox

import customtkinter as ctk

from auth import AuthManager
from db import get_collections
from tracker import Tracker


ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")


class SubscriptionTrackerApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.startup_ok = False

        self.title("SubScript")
        self.geometry("1100x700")
        self.minsize(1000, 650)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.bg_color = "#FFF5F8"
        self.sidebar_color = "#FFD1DC"
        self.accent_pink = "#FF69B4"
        self.dark_pink = "#C71585"
        self.card_bg = "#FFFFFF"
        self.border_color = "#FFECF2"
        self.text_color = "#333333"
        self.muted_text = "#777777"

        self.configure(fg_color=self.bg_color)

        try:
            users_collection, subscriptions_collection = get_collections()
        except ConnectionError as error:
            messagebox.showerror("Database Error", str(error))
            self.destroy()
            return

        self.auth_manager = AuthManager(users_collection)
        self.tracker = Tracker(subscriptions_collection)
        self.current_user_id = None
        self.active_screen = "dashboard"
        self.nav_buttons = {}

        self._build_login_screen()
        self._build_main_shell()
        self.show_login()
        self.startup_ok = True

    def _build_login_screen(self):
        self.login_screen = ctk.CTkFrame(self, fg_color=self.bg_color)
        self.login_screen.grid_rowconfigure(0, weight=1)
        self.login_screen.grid_columnconfigure(0, weight=1)

        card = ctk.CTkFrame(
            self.login_screen,
            width=420,
            corner_radius=24,
            fg_color=self.card_bg,
            border_width=2,
            border_color=self.border_color,
        )
        card.grid(row=0, column=0, padx=30, pady=30)

        ctk.CTkLabel(
            card,
            text="SubScript",
            font=("Segoe UI", 30, "bold"),
            text_color=self.dark_pink,
        ).pack(anchor="w", padx=30, pady=(30, 8))

        ctk.CTkLabel(
            card,
            text="Track subscriptions and spot waste before renewals hit.",
            font=("Segoe UI", 14),
            text_color=self.muted_text,
            wraplength=320,
            justify="left",
        ).pack(anchor="w", padx=30, pady=(0, 24))

        self.login_username = self._create_labeled_entry(card, "Username")
        self.login_password = self._create_labeled_entry(card, "Password", show="*")

        self.login_message = ctk.CTkLabel(
            card,
            text="",
            font=("Segoe UI", 13),
            text_color=self.dark_pink,
        )
        self.login_message.pack(anchor="w", padx=30, pady=(16, 6))

        button_row = ctk.CTkFrame(card, fg_color="transparent")
        button_row.pack(fill="x", padx=30, pady=(8, 30))
        button_row.grid_columnconfigure((0, 1), weight=1)

        ctk.CTkButton(
            button_row,
            text="Login",
            fg_color=self.dark_pink,
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
            text_color=self.dark_pink,
            border_width=2,
            border_color=self.dark_pink,
            hover_color="#FFF0F5",
            height=42,
            corner_radius=14,
            font=("Segoe UI", 14, "bold"),
            command=self.signup,
        ).grid(row=0, column=1, padx=(8, 0), sticky="ew")

    def _build_main_shell(self):
        self.app_shell = ctk.CTkFrame(self, fg_color=self.bg_color)
        self.app_shell.grid_rowconfigure(0, weight=1)
        self.app_shell.grid_columnconfigure(1, weight=1)

        self.sidebar = ctk.CTkFrame(
            self.app_shell,
            width=240,
            corner_radius=0,
            fg_color=self.sidebar_color,
            border_width=0,
        )
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.sidebar.grid_propagate(False)

        ctk.CTkLabel(
            self.sidebar,
            text="SubScript",
            font=("Segoe UI", 28, "bold"),
            text_color=self.dark_pink,
        ).pack(pady=40, padx=20)

        self._create_nav_button("dashboard", "Dashboard")
        self._create_nav_button("add", "Add Subscription")
        self._create_nav_button("subscriptions", "Subscriptions")

        ctk.CTkButton(
            self.sidebar,
            text="Logout",
            fg_color=self.dark_pink,
            hover_color="#A91471",
            corner_radius=10,
            height=38,
            command=self.logout_user,
        ).pack(side="bottom", pady=30, padx=30, fill="x")

        self.main_view = ctk.CTkFrame(
            self.app_shell,
            fg_color="transparent",
            border_width=0,
        )
        self.main_view.grid(row=0, column=1, sticky="nsew", padx=40, pady=20)

    def _create_labeled_entry(self, parent, label, show=None):
        ctk.CTkLabel(
            parent,
            text=label,
            font=("Segoe UI", 14, "bold"),
            text_color=self.text_color,
        ).pack(anchor="w", padx=30, pady=(0, 6))

        entry = ctk.CTkEntry(
            parent,
            width=340,
            height=42,
            corner_radius=12,
            border_color="#F1B6C8",
            fg_color="#FFF9FB",
            text_color=self.text_color,
            show=show,
        )
        entry.pack(fill="x", padx=30, pady=(0, 16))
        return entry

    def _create_nav_button(self, key, text):
        button = ctk.CTkButton(
            self.sidebar,
            text=text,
            fg_color="transparent",
            text_color="#666666",
            anchor="w",
            hover_color="#FFECF2",
            corner_radius=12,
            height=45,
            font=("Segoe UI", 13),
            command=lambda name=key: self.show_app_screen(name),
        )
        button.pack(fill="x", padx=15, pady=5)
        self.nav_buttons[key] = button

    def show_login(self):
        self.app_shell.grid_forget()
        self.login_screen.grid(row=0, column=0, sticky="nsew")
        self._reset_login_state()

    def show_app_screen(self, screen_name="dashboard"):
        if not self.current_user_id:
            self.show_login()
            return

        self.login_screen.grid_forget()
        self.app_shell.grid(row=0, column=0, sticky="nsew")
        self.active_screen = screen_name
        self._update_nav_state()
        self._render_active_screen()

    def _update_nav_state(self):
        for key, button in self.nav_buttons.items():
            is_active = key == self.active_screen
            button.configure(
                fg_color="white" if is_active else "transparent",
                text_color=self.dark_pink if is_active else "#666666",
                font=("Segoe UI", 13, "bold" if is_active else "normal"),
            )

    def _clear_main_view(self):
        for child in self.main_view.winfo_children():
            child.destroy()

    def _render_active_screen(self):
        self._clear_main_view()

        if self.active_screen == "dashboard":
            self._render_dashboard()
        elif self.active_screen == "add":
            self._render_add_subscription()
        elif self.active_screen == "subscriptions":
            self._render_subscriptions()

    def _render_dashboard(self):
        subscriptions = self.tracker.get_subscriptions(self.current_user_id)
        monthly_total = self.tracker.total_monthly_cost(self.current_user_id)
        yearly_total = self.tracker.total_yearly_cost(self.current_user_id)
        upcoming = self.tracker.upcoming_renewals(self.current_user_id)
        unused = self.tracker.unused_subscriptions(self.current_user_id)

        ctk.CTkLabel(
            self.main_view,
            text="Hey There!",
            font=("Segoe UI", 32, "bold"),
            text_color=self.text_color,
        ).pack(anchor="w", pady=(10, 0))

        ctk.CTkLabel(
            self.main_view,
            text="Here is your subscription breakdown for this month.",
            font=("Segoe UI", 14),
            text_color=self.muted_text,
        ).pack(anchor="w", pady=(0, 30))

        stats_frame = ctk.CTkFrame(self.main_view, fg_color="transparent")
        stats_frame.pack(fill="x", pady=10)

        self._create_stat_card(
            stats_frame,
            "Monthly Total",
            f"Rs. {monthly_total:.2f}",
            f"{len(subscriptions)} active subscriptions",
            self.accent_pink,
        )
        self._create_stat_card(
            stats_frame,
            "Upcoming Renewals",
            str(len(upcoming)),
            "Due within the next 7 days",
            self.dark_pink,
        )
        self._create_stat_card(
            stats_frame,
            "Yearly Total",
            f"Rs. {yearly_total:.2f}",
            f"{len(unused)} potentially unused subscriptions",
            "#FF82AB",
        )

        action_box = ctk.CTkFrame(
            self.main_view,
            fg_color=self.card_bg,
            corner_radius=20,
            border_width=2,
            border_color=self.border_color,
        )
        action_box.pack(fill="x", pady=30, ipady=20)

        ctk.CTkLabel(
            action_box,
            text="Quick Actions",
            font=("Segoe UI", 18, "bold"),
            text_color=self.dark_pink,
        ).pack(anchor="w", padx=25, pady=(15, 10))

        btn_row = ctk.CTkFrame(action_box, fg_color="transparent")
        btn_row.pack(fill="x", padx=20)
        btn_row.grid_columnconfigure((0, 1), weight=1)

        ctk.CTkButton(
            btn_row,
            text="+ Add Subscription",
            fg_color=self.dark_pink,
            hover_color="#A91471",
            corner_radius=15,
            height=45,
            font=("Segoe UI", 14, "bold"),
            command=lambda: self.show_app_screen("add"),
        ).grid(row=0, column=0, padx=(0, 6), sticky="ew")

        ctk.CTkButton(
            btn_row,
            text="View Subscriptions",
            fg_color="white",
            border_width=2,
            border_color=self.dark_pink,
            text_color=self.dark_pink,
            hover_color="#FFF0F5",
            corner_radius=15,
            height=45,
            font=("Segoe UI", 14, "bold"),
            command=lambda: self.show_app_screen("subscriptions"),
        ).grid(row=0, column=1, padx=(6, 0), sticky="ew")

        bottom_grid = ctk.CTkFrame(self.main_view, fg_color="transparent")
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

    def _render_add_subscription(self):
        ctk.CTkLabel(
            self.main_view,
            text="Add Subscription",
            font=("Segoe UI", 30, "bold"),
            text_color=self.text_color,
        ).pack(anchor="w", pady=(10, 4))

        ctk.CTkLabel(
            self.main_view,
            text="Use YYYY-MM-DD for renewal and last used dates.",
            font=("Segoe UI", 14),
            text_color=self.muted_text,
        ).pack(anchor="w", pady=(0, 24))

        form = ctk.CTkFrame(
            self.main_view,
            fg_color=self.card_bg,
            corner_radius=24,
            border_width=2,
            border_color=self.border_color,
        )
        form.pack(fill="x", ipadx=10, ipady=10)

        self.add_name_entry = self._create_labeled_entry(form, "Name")
        self.add_cost_entry = self._create_labeled_entry(form, "Monthly Cost")
        self.add_renewal_entry = self._create_labeled_entry(form, "Renewal Date")
        self.add_last_used_entry = self._create_labeled_entry(form, "Last Used")

        self.add_message = ctk.CTkLabel(
            form,
            text="",
            font=("Segoe UI", 13),
            text_color=self.dark_pink,
        )
        self.add_message.pack(anchor="w", padx=30, pady=(8, 10))

        button_row = ctk.CTkFrame(form, fg_color="transparent")
        button_row.pack(fill="x", padx=30, pady=(0, 20))
        button_row.grid_columnconfigure((0, 1), weight=1)

        ctk.CTkButton(
            button_row,
            text="Save",
            fg_color=self.dark_pink,
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
            text_color=self.dark_pink,
            border_width=2,
            border_color=self.dark_pink,
            hover_color="#FFF0F5",
            height=42,
            corner_radius=14,
            font=("Segoe UI", 14, "bold"),
            command=lambda: self.show_app_screen("dashboard"),
        ).grid(row=0, column=1, padx=(8, 0), sticky="ew")

    def _render_subscriptions(self):
        ctk.CTkLabel(
            self.main_view,
            text="Your Subscriptions",
            font=("Segoe UI", 30, "bold"),
            text_color=self.text_color,
        ).pack(anchor="w", pady=(10, 4))

        ctk.CTkLabel(
            self.main_view,
            text="A full list of every saved plan.",
            font=("Segoe UI", 14),
            text_color=self.muted_text,
        ).pack(anchor="w", pady=(0, 24))

        card = ctk.CTkFrame(
            self.main_view,
            fg_color=self.card_bg,
            corner_radius=24,
            border_width=2,
            border_color=self.border_color,
        )
        card.pack(fill="both", expand=True)

        subscriptions = self.tracker.get_subscriptions(self.current_user_id)

        if not subscriptions:
            ctk.CTkLabel(
                card,
                text="No subscriptions added yet.",
                font=("Segoe UI", 15),
                text_color=self.muted_text,
            ).pack(anchor="w", padx=24, pady=24)
            return

        for subscription in subscriptions:
            item = ctk.CTkFrame(card, fg_color="#FFF9FB", corner_radius=18)
            item.pack(fill="x", padx=20, pady=(16, 0))

            ctk.CTkLabel(
                item,
                text=subscription.name,
                font=("Segoe UI", 18, "bold"),
                text_color=self.dark_pink,
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
                text_color=self.text_color,
                justify="left",
            ).pack(anchor="w", padx=18, pady=(0, 14))

    def _create_stat_card(self, parent, title, value, subtext, accent):
        card = ctk.CTkFrame(
            parent,
            fg_color=self.card_bg,
            corner_radius=20,
            width=240,
            height=140,
            border_width=2,
            border_color=self.border_color,
        )
        card.pack(side="left", padx=(0, 20), expand=True, fill="both")
        card.pack_propagate(False)

        ctk.CTkLabel(
            card,
            text=title,
            font=("Segoe UI", 13),
            text_color="gray",
        ).pack(anchor="w", padx=20, pady=(20, 0))
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
            fg_color=self.card_bg,
            corner_radius=20,
            border_width=2,
            border_color=self.border_color,
        )
        left_pad = 10 if column == 0 else 0
        right_pad = 0 if column == 0 else 10
        frame.grid(row=0, column=column, padx=(left_pad, right_pad), sticky="nsew")

        ctk.CTkLabel(
            frame,
            text=title,
            font=("Segoe UI", 18, "bold"),
            text_color=self.dark_pink,
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

    def _reset_login_state(self):
        self.login_password.delete(0, "end")
        self.login_message.configure(text="")

    def login(self):
        username = self.login_username.get()
        password = self.login_password.get()
        success, result = self.auth_manager.login(username, password)

        if success:
            self.current_user_id = result
            self.login_message.configure(text="Login successful.", text_color="#2E8B57")
            self.show_app_screen("dashboard")
        else:
            self.login_message.configure(text=result, text_color="#C0392B")

    def signup(self):
        username = self.login_username.get()
        password = self.login_password.get()
        success, result = self.auth_manager.signup(username, password)

        if success:
            self.login_message.configure(
                text="Signup successful. Please log in.",
                text_color="#2E8B57",
            )
            self.login_password.delete(0, "end")
        else:
            self.login_message.configure(text=result, text_color="#C0392B")

    def save_subscription(self):
        name = self.add_name_entry.get()
        cost = self.add_cost_entry.get()
        renewal_date = self.add_renewal_entry.get()
        last_used = self.add_last_used_entry.get()

        is_valid, message = self.tracker.validate_subscription_data(
            name,
            cost,
            renewal_date,
            last_used,
        )
        if not is_valid:
            self.add_message.configure(text=message, text_color="#C0392B")
            return

        self.tracker.add_subscription(
            user_id=self.current_user_id,
            name=name,
            cost=float(cost),
            renewal_date=renewal_date,
            last_used=last_used,
        )
        self.add_message.configure(
            text="Subscription added successfully.",
            text_color="#2E8B57",
        )
        self.add_name_entry.delete(0, "end")
        self.add_cost_entry.delete(0, "end")
        self.add_renewal_entry.delete(0, "end")
        self.add_last_used_entry.delete(0, "end")

    def logout_user(self):
        self.current_user_id = None
        self.active_screen = "dashboard"
        self.show_login()
