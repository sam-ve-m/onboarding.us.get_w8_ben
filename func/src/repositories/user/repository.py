# THIRD PARTY
from etria_logger import Gladsheim

# PROJECT IMPORTS
from ...infrastructure.mongo_db.infrastructure import MongoDBInfrastructure

# STANDARD IMPORTS
from decouple import config


class UserRepository:

    infra = MongoDBInfrastructure

    @classmethod
    async def __get_collection(cls):
        mongo_client = cls.infra.get_client()
        try:
            database = mongo_client[config("MONGODB_DATABASE_NAME")]
            collection = database[config("MONGODB_USER_COLLECTION")]
            return collection
        except Exception as error:
            message = f'UserRepository::_get_collection::Error when trying to get collection'
            Gladsheim.error(error=error, message=message)
            raise error
