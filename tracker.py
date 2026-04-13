# Add subscription
# Delete subscription
# calculate total monthly cost
# Delete unused subscription
from models import Subscription
from datetime import datetime
import pickle

class Tracker:
    def __init__(self):
        self.subscriptions = []

    def add_subscription(self, sub):
        # add a new subscription to the list
        self.subscriptions.append(sub)

    def remove_subscription(self, name):
        # remove subscription by name
        for sub in self.subscriptions:
            if sub.name == name:
                self.subscriptions.remove(sub)
                return True  # removed successfully
        return False  # not found

    def total_monthly_cost(self):
        # calculate total monthly spending
        total = 0
        for sub in self.subscriptions:
            total += sub.monthly_cost()
        return total

    def upcoming_bills(self, days=7):
        # get subscriptions whose billing date is within given days
        upcoming = []
        today = datetime.today()

        for sub in self.subscriptions:
            next_date = sub.next_billing_date()
            diff = (next_date - today).days  # diff in days

            if 0 <= diff <= days:
                upcoming.append(sub)

        return upcoming  # return list of upcoming subscriptions

    def unused_subscriptions(self, days_thresh=30):
        # gets those subscriptions that are not used recently
        unused = []

        for sub in self.subscriptions:
            if sub.is_unused(days_thresh):
                unused.append(sub)

        return unused  # returning list of unused subscriptions

    def save_data(self, filename="data.pkl"):
        # save subscriptions list into a file
        with open(filename, "wb") as ofile:
            pickle.dump(self.subscriptions, ofile)

    def load_data(self, filename="data.pkl"):
        # load subscriptions list from file
        try:
            with open(filename, "rb") as ifile:
                self.subscriptions = pickle.load(ifile)
        except FileNotFoundError:
            self.subscriptions = []  # if file not found, start with empty list