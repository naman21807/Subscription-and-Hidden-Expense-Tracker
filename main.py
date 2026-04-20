"""Entry point for the Subscription and Hidden Expense Tracker app."""

from ui.UI import SubscriptionTrackerApp


if __name__ == "__main__":
    app = SubscriptionTrackerApp()
    if app.startup_ok:
        app.mainloop()
