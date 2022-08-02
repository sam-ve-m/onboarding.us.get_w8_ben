# PROJECT IMPORTS
from ...domain.exceptions.exceptions import ErrorOnGettingPhysicalW8, ErrorResponseDriveWealth, ErrorOnListingPhysicalW8
from ...domain.models.jwt.models import Jwt
from ...transport.drive_wealth.transport import DWTransport


class DriveWealthService:

    dw_transport = DWTransport

    @classmethod
    async def get_w8_pdf_link(cls, jwt_data: Jwt) -> str:
        status, response = await cls.dw_transport.call_list_all_physical_get(
            jwt_data=jwt_data
        )
        if not status:
            raise ErrorOnListingPhysicalW8

        w8_file = list(filter(lambda x: x.get("type", {}).get("name") == "TAX", response))
        if not w8_file:
            raise ErrorResponseDriveWealth

        w8_file_id = w8_file.pop(0).get("documentID")

        status, response = await cls.dw_transport.call_get_physical_get(
            doc_id=w8_file_id
        )
        if not status:
            raise ErrorOnGettingPhysicalW8

        w8_file_link = response.get("url")

        return w8_file_link
