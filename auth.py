"""Authentication logic for signup and login."""

import hashlib
import os

from pymongo.errors import DuplicateKeyError


class AuthManager:
    def __init__(self, users_collection):
        self.users_collection = users_collection

    def _hash_password(self, password, salt=None):
        if salt is None:
            salt = os.urandom(16)

        hashed_password = hashlib.pbkdf2_hmac(
            "sha256",
            password.encode("utf-8"),
            salt,
            100000,
        )
        return f"{salt.hex()}${hashed_password.hex()}"

    def _verify_password(self, password, stored_value):
        try:
            salt_hex, password_hash = stored_value.split("$", 1)
        except ValueError:
            return False

        test_hash = self._hash_password(password, bytes.fromhex(salt_hex))
        return test_hash.split("$", 1)[1] == password_hash

    def signup(self, username, password):
        username = username.strip()

        if not username or not password:
            return False, "Username and password are required."

        existing_user = self.users_collection.find_one({"username": username})
        if existing_user:
            return False, "Username already exists."

        password_hash = self._hash_password(password)
        try:
            result = self.users_collection.insert_one(
                {
                    "username": username,
                    "password_hash": password_hash,
                }
            )
        except DuplicateKeyError:
            return False, "Username already exists."

        return True, str(result.inserted_id)

    def login(self, username, password):
        username = username.strip()

        if not username or not password:
            return False, "Username and password are required."

        user = self.users_collection.find_one({"username": username})
        if user is None:
            return False, "Invalid username or password."

        if not self._verify_password(password, user["password_hash"]):
            return False, "Invalid username or password."

        return True, str(user["_id"])
