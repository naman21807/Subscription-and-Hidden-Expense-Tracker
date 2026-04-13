from datetime import datetime, timedelta

class Subscription:
    def __init__(self, name, cost, bill_cycle, start_date, category, last_date=None):
        self.name = name
        self.cost = cost
        self.bill_cycle = bill_cycle
        self.last_date = last_date
        self.start_date = start_date
        self.category = category

    def monthly_cost(self):
        # convert yearly to monthly
        if self.bill_cycle == "yearly":
            return self.cost / 12
        return self.cost

    def yearly_cost(self):
        # convert monthly to yearly
        if self.bill_cycle == "monthly":
            return self.cost * 12
        return self.cost

    def is_unused(self, days_thresh=30):
        # check if subscription is unused
        if not self.last_date:
            return True

        last_used_date = datetime.strptime(self.last_date, "%Y-%m-%d")
        today = datetime.today()
        diff = (today - last_used_date).days  # we are checking the diff here

        return diff > days_thresh  # if this returns true it means that the subscription is unused

    def next_billing_date(self):
        # calculate next billing date based on billing cycle
        start = datetime.strptime(self.start_date, "%Y-%m-%d")
        today = datetime.today()

        # keep adding cycle time until we reach future date
        if self.bill_cycle == "monthly":
            while start < today:
                start += timedelta(days=30)
        elif self.bill_cycle == "yearly":
            while start < today:
                start += timedelta(days=365)

        return start  # returning next billing date

    def to_dict(self):
        # convert the object into a dict to save into the file later
        return {
            "name": self.name,
            "cost": self.cost,
            "bill_cycle": self.bill_cycle,
            "start_date": self.start_date,
            "category": self.category,
            "last_date": self.last_date
        }

    @classmethod
    def from_dict(cls, data):
        # Create object from dictionary
        return cls(
            data["name"],
            data["cost"],
            data["bill_cycle"],
            data["start_date"],
            data["category"],
            data.get("last_date")
        )