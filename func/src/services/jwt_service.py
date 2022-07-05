# Jormungandr-Onboarding
from ..domain.exceptions.exceptions import ErrorOnDecodeJwt

# Third party
from etria_logger import Gladsheim
from heimdall_client import Heimdall
from heimdall_client.src.domain.enums.heimdall_status_responses import HeimdallStatusResponses


class JWTService:

    @classmethod
    async def decode_jwt_and_get_unique_id(cls, jwt: str, user_repository=UserRepository):
        try:
            jwt_content, heimdall_status_response = await Heimdall.decode_payload(jwt=jwt)
            if HeimdallStatusResponses.SUCCESS == heimdall_status_response:
                unique_id = jwt_content["decoded_jwt"]['user'].get('unique_id')
                user = await user_repository.find_one({"unique_id": user_unique_id})
                dw_id = user["portfolios"]["default"]["us"]["dw_id"]
                return unique_id, dw_id
            raise ErrorOnDecodeJwt
        except Exception as error:
            message = "JwtService::decode_jwt_and_get_unique_id::Failed to decode jwt"
            Gladsheim.error(error=error, message=message)
            raise error
