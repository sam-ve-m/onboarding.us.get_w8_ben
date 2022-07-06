# STANDARD IMPORTS
from http import HTTPStatus

# THIRD PARTY IMPORTS
from etria_logger import Gladsheim
from flask import request

from func.src.domain.exceptions.exceptions import ErrorOnDecodeJwt
from func.src.services.drive_wealth.service import DriveWealthService
from func.src.services.jwt_service import JWTService


async def get_w8_ben_document():
    jwt_data = request.headers.get("x-thebes-answer")
    unique_id, user_dw_id = await JWTService.decode_jwt_and_get_unique_id(jwt_data=jwt_data)

    w8_ben_extraction = await DriveWealthService.get_w8_pdf(
        user_dw_id=user_dw_id
    )


