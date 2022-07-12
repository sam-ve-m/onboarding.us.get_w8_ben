# STANDARD IMPORTS
import json
from typing import Tuple
from decouple import config

# THIRD PARTY IMPORTS
from etria_logger import Gladsheim
from mepho import DWApiTransport
from aiohttp import ClientResponse

# PROJECT IMPORTS
from func.src.domain.exceptions.exceptions import ErrorResponseDriveWealth


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
            user_id: str,
    ):
        url = config("DW_USER_PHYSICAL_DOCUMENTS_URL")
        formatted_url = url.format(user_id)
        http_response = await cls.dw_caller_transport.execute_get(
            url=formatted_url, query_params={}
        )

        if not http_response:
            Gladsheim.error(message="DriveWealth::dw_caller_transport.execute_get::Error on getting http response")
            raise ErrorResponseDriveWealth

        response = await cls._build_response(http_response=http_response)
        return response

    @classmethod
    async def call_get_physical_get(
            cls,
            doc_id: str,
    ):
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
