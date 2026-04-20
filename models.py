from datetime import date, datetime


class Subscription:
    """Simple model for a user's subscription."""

    DATE_FORMAT = "%Y-%m-%d"

    def __init__(self, name, cost, renewal_date, last_used):
        self.name = name
        self.cost = float(cost)
        self.renewal_date = renewal_date
        self.last_used = last_used

    def monthly_cost(self):
        """Return the stored monthly subscription cost."""
        return self.cost

    def yearly_cost(self):
        """Return the yearly cost based on the monthly amount."""
        return self.cost * 12

    def parsed_renewal_date(self):
        return datetime.strptime(self.renewal_date, self.DATE_FORMAT).date()

    def parsed_last_used(self):
        return datetime.strptime(self.last_used, self.DATE_FORMAT).date()

    def upcoming_renewal_date(self):
        """Treat renewal_date as a recurring yearly date and return the next one."""
        base_date = self.parsed_renewal_date()
        today = date.today()
        next_date = self._safe_replace_year(base_date, today.year)

        if next_date < today:
            next_date = self._safe_replace_year(base_date, today.year + 1)

        return next_date

    def is_unused(self, days_threshold=30):
        """Return True when the subscription was not used recently."""
        today = date.today()
        days_since_used = (today - self.parsed_last_used()).days
        return days_since_used > days_threshold

    def to_dict(self, user_id):
        """Convert the object into a MongoDB-friendly dictionary."""
        return {
            "user_id": user_id,
            "name": self.name,
            "cost": self.cost,
            "renewal_date": self.renewal_date,
            "last_used": self.last_used,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            name=data["name"],
            cost=data["cost"],
            renewal_date=data["renewal_date"],
            last_used=data["last_used"],
        )

    @staticmethod
    def _safe_replace_year(date_value, year):
        """Handle leap-day renewals in non-leap years."""
        try:
            return date_value.replace(year=year)
        except ValueError:
            return date_value.replace(year=year, day=28)
