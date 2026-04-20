"""MongoDB connection helpers for the subscription tracker project."""

import os

from pymongo import MongoClient
from pymongo.errors import PyMongoError


def get_database():
    """Connect to MongoDB and return the project database."""
    mongo_uri = os.getenv("MONGODB_URI", "mongodb://localhost:27017/")
    client = MongoClient(mongo_uri, serverSelectionTimeoutMS=3000)
    client.admin.command("ping")
    return client["subscription_tracker"]


def get_collections():
    """Return the collections used by the application."""
    try:
        database = get_database()
        users = database["users"]
        subscriptions = database["subscriptions"]

        # Keep usernames unique so duplicate signup is blocked cleanly.
        users.create_index("username", unique=True)
        subscriptions.create_index("user_id")

        return users, subscriptions
    except PyMongoError as error:
        raise ConnectionError(
            "Could not connect to MongoDB. Start MongoDB on localhost:27017 "
            "or set the MONGODB_URI environment variable."
        ) from error
