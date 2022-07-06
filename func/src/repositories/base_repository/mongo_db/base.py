# PROJECT IMPORTS
from src.infrastructure.mongo_db.infrastructure import MongoDBInfrastructure

# THIRD PART IMPORTS
from etria_logger import Gladsheim


class MongoDbBaseRepository:
    infra = MongoDBInfrastructure
    database = None
    collection = None

    @classmethod
    async def _get_collection(cls):
        mongo_client = cls.infra.get_client()
        try:
            database = mongo_client[cls.database]
            collection = database[cls.collection]
            return collection
        except Exception as error:
            message = f'UserRepository::_get_collection::Error when trying to get collection'
            Gladsheim.error(error=error, message=message)
            raise error
