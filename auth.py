"""Authentication logic for signup and login."""

import hmac
import hashlib
import os

from pymongo.errors import DuplicateKeyError


class AuthManager:
    def __init__(self, users_collection):
        self.users_collection = users_collection

    def generate_salt(self):
        return os.urandom(16).hex()

    def hash_password(self, password, salt):
        password_hash = hashlib.pbkdf2_hmac(
            "sha256",
            password.encode("utf-8"),
            bytes.fromhex(salt),
            100000,
        )
        return password_hash.hex()

    def verify_password(self, password, salt, password_hash):
        test_hash = self.hash_password(password, salt)
        return hmac.compare_digest(test_hash, password_hash)

    def verify_legacy_password(self, password, salt, password_hash):
        legacy_hash = hashlib.sha256((password + salt).encode("utf-8")).hexdigest()
        return hmac.compare_digest(legacy_hash, password_hash)

    def verify_combined_password_hash(self, password, stored_value):
        try:
            salt, password_hash = stored_value.split("$", 1)
        except ValueError:
            return False
        return self.verify_password(password, salt, password_hash)

    def upgrade_password_storage(self, user_id, password):
        salt = self.generate_salt()
        password_hash = self.hash_password(password, salt)
        self.users_collection.update_one(
            {"_id": user_id},
            {
                "$set": {
                    "salt": salt,
                    "password_hash": password_hash,
                },
                "$unset": {
                    "password": "",
                },
            },
        )

    def signup(self, username, password):
        username = username.strip()

        if not username or not password:
            return False, "Username and password are required."

        existing_user = self.users_collection.find_one({"username": username})
        if existing_user:
            return False, "Username already exists."

        salt = self.generate_salt()
        password_hash = self.hash_password(password, salt)
        try:
            result = self.users_collection.insert_one(
                {
                    "username": username,
                    "salt": salt,
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

        salt = user.get("salt")
        password_hash = user.get("password_hash")

        if salt and password_hash and self.verify_password(password, salt, password_hash):
            return True, str(user["_id"])

        legacy_password_hash = user.get("password")
        if salt and legacy_password_hash and self.verify_legacy_password(password, salt, legacy_password_hash):
            self.upgrade_password_storage(user["_id"], password)
            return True, str(user["_id"])

        if password_hash and "$" in password_hash and self.verify_combined_password_hash(password, password_hash):
            self.upgrade_password_storage(user["_id"], password)
            return True, str(user["_id"])

        return False, "Invalid username or password."
