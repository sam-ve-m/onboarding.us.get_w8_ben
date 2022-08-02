# PROJECT IMPORTS
from heimdall_client import Heimdall, HeimdallStatusResponses
from src.domain.exceptions.exceptions import ErrorOnDecodeJwt
from src.repositories.mongo_db.user.repository import UserRepository


class Jwt:
    def __init__(self, jwt: str):
        self.__jwt = jwt

    async def __decode_and_validate_jwt(self):
        jwt_content, heimdall_status_response = await Heimdall.decode_payload(jwt=self.__jwt)
        if HeimdallStatusResponses.SUCCESS == heimdall_status_response:
            self.__jwt_payload = jwt_content.get("decoded_jwt")
            return self.__jwt_payload
        else:
            raise ErrorOnDecodeJwt

    async def get_drive_wealth_id(self):
        unique_id = self.__jwt_payload.get("user").get("unique_id")
        user = await UserRepository.find_one(unique_id)
        user_dw_id = user.get("portfolios", {}).get("default", {}).get("us", {}).get("dw_id")
        return user_dw_id

    async def __call__(self):
        self.__jwt_payload = await self.__decode_and_validate_jwt()
