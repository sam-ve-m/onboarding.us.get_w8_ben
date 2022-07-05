from src.transports.dw.transport import DWTransport
from src.repositories.file.repository import FileRepository
from func.src.domain.exceptions.exceptions import InternalServerError


class DriveWealthService:

    dw_transport = DWTransport
    file_repository = FileRepository

    @classmethod
    async def get_w8_pdf(cls, user_dw_id: str) -> str:
        status, response = await cls.dw_transport.call_list_all_physical_get(
            user_id=user_dw_id
        )
        if not status:
            raise InternalServerError("common.unable_to_process")
        w8_file = list(filter(lambda x: x["type"]["name"] == "TAX", response))
        if not w8_file:
            raise InternalServerError("common.unable_to_process")
        w8_file_id = w8_file[0]["documentID"]
        status, response = await cls.dw_transport.call_get_physical_get(
            doc_id=w8_file_id
        )
        if not status:
            raise InternalServerError("common.unable_to_process")
        w8_file_link = response["url"]
        return w8_file_link
