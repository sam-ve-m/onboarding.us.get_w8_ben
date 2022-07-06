# PROJECT IMPORTS
from ..domain.exceptions.exceptions import ErrorOnDecodeJwt
from ..repositories.mongo_db.user.repository import UserRepository

# THIRD PARTY IMPORTS
from etria_logger import Gladsheim
from heimdall_client import Heimdall
from heimdall_client.src.domain.enums.heimdall_status_responses import HeimdallStatusResponses


class JWTService:

    user_repository = UserRepository

    @classmethod
    async def decode_jwt_and_get_unique_id(cls, jwt_data: str):
        try:
            jwt_content, heimdall_status_response = await Heimdall.decode_payload(jwt=jwt_data)
            if HeimdallStatusResponses.SUCCESS == heimdall_status_response:
                unique_id = jwt_content["decoded_jwt"]['user'].get('unique_id')
                user = await cls.user_repository.find_one(unique_id)
                user_dw_id = user["portfolios"]["default"]["us"]["dw_id"]
                return unique_id, user_dw_id
            raise ErrorOnDecodeJwt

        except Exception as ex:
            message = "JwtService::decode_jwt_and_get_unique_id::Failed to decode jwt"
            Gladsheim.error(error=ex, message=message)
            raise ex
