# THIRD PARTY
from decouple import config
from etria_logger import Gladsheim

# STANDARD IMPORTS
from src.infrastructure.mongo_db.infrastructure import MongoDBInfrastructure


class UserRepository:
    infra = MongoDBInfrastructure
    database = config("MONGODB_DATABASE_NAME")
    collection = config("MONGODB_USER_COLLECTION")

    @classmethod
    async def _get_collection(cls):
        mongo_client = cls.infra.get_client()
        try:
            database = mongo_client[cls.database]
            collection = database[cls.collection]
            return collection
        except Exception as error:
            message = f'MongoUserRepository::_get_collection::Error when trying to get collection'
            Gladsheim.error(error=error, message=message)
            raise error

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
