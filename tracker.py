from models import Subscription
from datetime import date


class Tracker:
    """Business logic for subscriptions."""

    def __init__(self, subscriptions_collection):
        self.subscriptions_collection = subscriptions_collection

    def add_subscription(self, user_id, name, cost, renewal_date, last_used):
        subscription = Subscription(name, cost, renewal_date, last_used)
        self.subscriptions_collection.insert_one(subscription.to_dict(user_id))
        return subscription

    def get_subscriptions(self, user_id):
        documents = self.subscriptions_collection.find({"user_id": user_id}).sort("name", 1)
        return [Subscription.from_dict(document) for document in documents]

    def total_monthly_cost(self, user_id):
        subscriptions = self.get_subscriptions(user_id)
        return sum(subscription.monthly_cost() for subscription in subscriptions)

    def total_yearly_cost(self, user_id):
        subscriptions = self.get_subscriptions(user_id)
        return sum(subscription.yearly_cost() for subscription in subscriptions)

    def upcoming_renewals(self, user_id, days=7):
        subscriptions = self.get_subscriptions(user_id)
        today = date.today()
        upcoming = []

        for subscription in subscriptions:
            renewal_date = subscription.upcoming_renewal_date()
            days_left = (renewal_date - today).days

            if 0 <= days_left <= days:
                upcoming.append(subscription)

        return upcoming

    def unused_subscriptions(self, user_id, days_threshold=30):
        subscriptions = self.get_subscriptions(user_id)
        return [
            subscription
            for subscription in subscriptions
            if subscription.is_unused(days_threshold)
        ]

    def validate_subscription_data(self, name, cost, renewal_date, last_used):
        if not name.strip():
            return False, "Subscription name is required."

        try:
            cost_value = float(cost)
            if cost_value < 0:
                return False, "Cost must be a positive number."
        except ValueError:
            return False, "Cost must be a valid number."

        for date_value, label in [(renewal_date, "Renewal date"), (last_used, "Last used date")]:
            try:
                date.fromisoformat(date_value)
            except ValueError:
                return False, f"{label} must be in YYYY-MM-DD format."

        return True, ""
