# PROJECT IMPORTS
from ...domain.exceptions.exceptions import InternalServerError
from ...transport.drive_wealth.transport import DWTransport


class DriveWealthService:

    dw_transport = DWTransport

    @classmethod
    async def get_w8_pdf_link(cls, user_dw_id: str) -> str:
        status, response = await cls.dw_transport.call_list_all_physical_get(
            user_id=user_dw_id
        )
        if not status:
            raise InternalServerError("common.unable_to_get_status_from_drive_wealth")
        w8_file = list(filter(lambda x: x["type"]["name"] == "TAX", response))
        if not w8_file:
            raise InternalServerError("common.unable_to_process_file_from_drive_wealth")
        w8_file_id = w8_file[0]["documentID"]
        status, response = await cls.dw_transport.call_get_physical_get(
            doc_id=w8_file_id
        )
        if not status:
            raise InternalServerError("common.unable_to_get_file_from_drive_wealth")
        w8_file_link = response["url"]
        return w8_file_link
