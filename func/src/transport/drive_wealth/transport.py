# STANDARD IMPORTS
import json
from typing import Tuple
from decouple import config

# THIRD PARTY IMPORTS
from etria_logger import Gladsheim
from mepho import DWApiTransport
from aiohttp import ClientResponse

# PROJECT IMPORTS
from src.domain.exceptions.exceptions import ErrorResponseDriveWealth
from src.domain.models.jwt.models import Jwt


class DWTransport:

    dw_caller_transport = DWApiTransport

    @classmethod
    async def _build_response(cls, http_response: ClientResponse) -> Tuple[bool, dict]:
        status = False
        if http_response.status in [200, 201]:
            status = True
        body = await http_response.text()
        dict_body = json.loads(body)
        return status, dict_body

    @classmethod
    async def call_list_all_physical_get(
            cls,
            jwt_data: Jwt,
    ) -> tuple:
        url = config("DW_USER_PHYSICAL_DOCUMENTS_URL")
        dw_id = await jwt_data.get_drive_wealth_id()
        formatted_url = url.format(dw_id)
        http_response = await cls.dw_caller_transport.execute_get(
            url=formatted_url, query_params={}
        )

        if not http_response:
            Gladsheim.error(message="DriveWealth::dw_caller_transport.execute_get::Error on getting http response", url=formatted_url)
            raise ErrorResponseDriveWealth

        response = await cls._build_response(
            http_response=http_response
        )
        return response

    @classmethod
    async def call_get_physical_get(
            cls,
            doc_id: str,
    ) -> tuple:
        url = config("DW_USER_PHYSICAL_DOCUMENT_URL")
        formatted_url = url.format(doc_id)
        http_response = await cls.dw_caller_transport.execute_get(
            url=formatted_url, query_params={}
        )
        if not http_response:
            Gladsheim.error(message="DriveWealth::dw_caller_transport.execute_get::Error on getting http response")
            raise ErrorResponseDriveWealth

        response = await cls._build_response(http_response=http_response)
        return response
