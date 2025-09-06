from core import database


class ProfileManager:
    def __init__(self, db: database.pymongo.database.Database):
        self.db = db

    def get_user_profile(self, email: str) -> dict | None:
        """
        Fetches user profile by email.
        """
        profile = self.db["user_profiles"].find_one({"email": email})
        if profile is None:
            return None
        profile.pop("_id", None)
        return profile

    def update_user_profile(self, email: str, update_data: dict) -> bool:
        """
        Updates user profile.
        """
        result = self.db["user_profiles"].update_one({"email": email}, {"$set": update_data})
        return result.modified_count > 0
    def create_user_profile(self, email: str, full_name: str) -> bool:
        """
        Creates a new user profile.
        """
        result = self.db["user_profiles"].insert_one({
            "email": email,
            "full_name": full_name
        })
        return result.acknowledged