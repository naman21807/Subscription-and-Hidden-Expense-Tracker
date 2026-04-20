# Subscription and Hidden Expense Tracker

This is a Tkinter desktop application that helps users:

- sign up and log in securely
- store their subscriptions in MongoDB
- calculate total monthly and yearly subscription cost
- see upcoming renewals
- find subscriptions that have not been used recently

## Project Structure

- `main.py` - app entry point
- `db.py` - MongoDB connection and collections
- `auth.py` - signup and login logic with password hashing
- `models.py` - `Subscription` class
- `tracker.py` - subscription business logic
- `ui/` - all Tkinter screens

## Database

- Database name: `subscription_tracker`
- Collections:
  - `users`
  - `subscriptions`

## Requirements

Install MongoDB and make sure it is running locally on:

`mongodb://localhost:27017/`

Install Python dependency:

```bash
pip install pymongo
```

## Run the App

```bash
python main.py
```

## Date Format

Use `YYYY-MM-DD` for:

- renewal date
- last used date
