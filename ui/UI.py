"""Tkinter application shell."""

from pathlib import Path
import sys
import tkinter as tk
from tkinter import messagebox

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from auth import AuthManager
from db import get_collections
from tracker import Tracker
from ui.add_subscription_screen import AddSubscriptionFrame
from ui.dashboard import DashboardFrame
from ui.login_screen import LoginFrame
from ui.view_subscriptions_screen import ViewSubscriptionsFrame


class SubscriptionTrackerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.startup_ok = False

        self.app_name = "SubScript"
        self.bg_color = "#FFF5F8"
        self.sidebar_color = "#FFD1DC"
        self.dark_pink = "#C71585"
        self.border_color = "#FFECF2"
        self.text_color = "#333333"
        self.muted_text = "#777777"

        self.title(self.app_name)
        self.geometry("1100x700")
        self.minsize(1000, 650)
        self.configure(bg=self.bg_color)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        try:
            users_collection, subscriptions_collection = get_collections()
        except ConnectionError as error:
            messagebox.showerror("Database Error", str(error))
            self.destroy()
            return

        self.auth_manager = AuthManager(users_collection)
        self.tracker = Tracker(subscriptions_collection)
        self.current_user_id = None
        self.current_frame_name = "LoginFrame"
        self.nav_buttons = {}
        self.frames = {}

        self._build_login_container()
        self._build_app_shell()
        self._create_frames()
        self.show_frame("LoginFrame")
        self.startup_ok = True

    def _build_login_container(self):
        self.login_container = tk.Frame(self, bg=self.bg_color)
        self.login_container.grid(row=0, column=0, sticky="nsew")
        self.login_container.grid_rowconfigure(0, weight=1)
        self.login_container.grid_columnconfigure(0, weight=1)

    def _build_app_shell(self):
        self.app_shell = tk.Frame(self, bg=self.bg_color)
        self.app_shell.grid_rowconfigure(0, weight=1)
        self.app_shell.grid_columnconfigure(1, weight=1)

        self.sidebar = tk.Frame(self.app_shell, bg=self.sidebar_color, width=240)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.sidebar.grid_propagate(False)

        tk.Label(
            self.sidebar,
            text=self.app_name,
            font=("Segoe UI", 28, "bold"),
            fg=self.dark_pink,
            bg=self.sidebar_color,
        ).pack(anchor="w", padx=32, pady=(48, 56))

        self._create_nav_button("DashboardFrame", "Dashboard")
        self._create_nav_button("AddSubscriptionFrame", "Add Subscription")
        self._create_nav_button("ViewSubscriptionsFrame", "Subscriptions")

        tk.Button(
            self.sidebar,
            text="Logout",
            font=("Segoe UI", 12, "bold"),
            fg="white",
            bg=self.dark_pink,
            activebackground="#A91471",
            activeforeground="white",
            relief="flat",
            bd=0,
            padx=18,
            pady=10,
            command=self.logout_user,
        ).pack(side="bottom", fill="x", padx=28, pady=28)

        self.content_frame = tk.Frame(self.app_shell, bg=self.bg_color)
        self.content_frame.grid(row=0, column=1, sticky="nsew", padx=40, pady=24)
        self.content_frame.grid_rowconfigure(0, weight=1)
        self.content_frame.grid_columnconfigure(0, weight=1)

    def _create_frames(self):
        self.frames["LoginFrame"] = LoginFrame(self.login_container, self)
        self.frames["LoginFrame"].grid(row=0, column=0, sticky="nsew")

        for frame_class in (DashboardFrame, AddSubscriptionFrame, ViewSubscriptionsFrame):
            frame = frame_class(self.content_frame, self)
            self.frames[frame_class.__name__] = frame
            frame.grid(row=0, column=0, sticky="nsew")

    def _create_nav_button(self, frame_name, text):
        button = tk.Button(
            self.sidebar,
            text=text,
            font=("Segoe UI", 12),
            fg="#444444",
            bg=self.sidebar_color,
            activebackground="#FFE8F0",
            activeforeground=self.dark_pink,
            relief="flat",
            bd=0,
            anchor="w",
            padx=16,
            pady=14,
            command=lambda name=frame_name: self.show_frame(name),
        )
        button.pack(fill="x", padx=18, pady=6)
        self.nav_buttons[frame_name] = button

    def show_frame(self, frame_name):
        self.current_frame_name = frame_name

        if frame_name == "LoginFrame":
            self.app_shell.grid_forget()
            self.login_container.grid(row=0, column=0, sticky="nsew")
        else:
            if not self.current_user_id:
                self.show_frame("LoginFrame")
                return
            self.login_container.grid_forget()
            self.app_shell.grid(row=0, column=0, sticky="nsew")

        frame = self.frames[frame_name]
        if hasattr(frame, "refresh"):
            frame.refresh()
        frame.tkraise()
        self._update_nav_state()

    def _update_nav_state(self):
        for frame_name, button in self.nav_buttons.items():
            is_active = frame_name == self.current_frame_name
            button.config(
                fg=self.dark_pink if is_active else "#444444",
                bg="white" if is_active else self.sidebar_color,
                font=("Segoe UI", 12, "bold" if is_active else "normal"),
            )

    def login_user(self, user_id):
        self.current_user_id = user_id
        self.show_frame("DashboardFrame")

    def logout_user(self):
        self.current_user_id = None
        self.show_frame("LoginFrame")
