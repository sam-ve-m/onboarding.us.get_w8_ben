# THIRD PARTY
from decouple import config
from etria_logger import Gladsheim

# STANDARD IMPORTS
from ...base_repository.mongo_db.base import MongoDbBaseRepository


class UserRepository(MongoDbBaseRepository):
    database = config("MONGODB_DATABASE_NAME")
    collection = config("MONGODB_USER_COLLECTION")

    @classmethod
    async def find_one(cls, unique_id: str) -> dict:
        collection = await cls._get_collection()
        try:
            user = await collection.find_one({"unique_id": unique_id})
            return user
        except Exception as error:
            message = f'UserRepository::find_one_user::with this query::"unique_id":{unique_id}'
            Gladsheim.error(error=error, message=message)
            raise error
