"""Entry point for the Subscription and Hidden Expense Tracker app."""

import tkinter as tk
from tkinter import messagebox

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

        self.title("Subscription and Hidden Expense Tracker")
        self.geometry("850x600")
        self.resizable(False, False)

        try:
            users_collection, subscriptions_collection = get_collections()
        except ConnectionError as error:
            messagebox.showerror("Database Error", str(error))
            self.destroy()
            return

        self.auth_manager = AuthManager(users_collection)
        self.tracker = Tracker(subscriptions_collection)

        self.current_user_id = None

        container = tk.Frame(self, bg="#f4f6f8")
        container.pack(fill="both", expand=True)

        self.frames = {}
        for frame_class in (
            LoginFrame,
            DashboardFrame,
            AddSubscriptionFrame,
            ViewSubscriptionsFrame,
        ):
            frame = frame_class(container, self)
            self.frames[frame_class.__name__] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.show_frame("LoginFrame")
        self.startup_ok = True

    def show_frame(self, frame_name):
        frame = self.frames[frame_name]

        if hasattr(frame, "refresh"):
            frame.refresh()

        frame.tkraise()

    def login_user(self, user_id):
        self.current_user_id = user_id
        self.show_frame("DashboardFrame")

    def logout_user(self):
        self.current_user_id = None
        self.show_frame("LoginFrame")


if __name__ == "__main__":
    app = SubscriptionTrackerApp()
    if app.startup_ok:
        app.mainloop()
