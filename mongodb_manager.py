from pymongo import MongoClient

client = MongoClient("localhost", 27017)

db = client.lazyhelperdb
lazy_helper_db = db.users


class DataBaseManagerUser:

    @classmethod
    def insert_user_data(cls, user_id: str, phone: str):
        data = {"phone": phone, "user_id": user_id}
        lazy_helper_db.insert_one(data)
        return True

    @classmethod
    def check_login(cls, user_id):
        data = lazy_helper_db.find_one({"user_id": user_id})
        if data is not None:
            return True
        else:
            return False

    @classmethod
    def users_list(cls):
        users_list = []
        users = lazy_helper_db.find({})
        for user in users:
            users_list.append(user)
        return users_list
