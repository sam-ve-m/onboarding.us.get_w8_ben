from unittest.mock import patch
import pytest

from func.src.services.drive_wealth.service import DriveWealthService
from func.src.transport.drive_wealth.transport import DWTransport

user_dw_id_stub = '89c69304-018a-40b7-be5b-2121c16e109e'


@pytest.mark.asyncio
@patch.object(DWTransport, "call_get_physical_get", return_value=(True, {"url": "https://bo-api.drivewealth.io/back-office/users/89c69304-018a-40b7-be5b-2121c16e109e"}))
@patch.object(DWTransport, "call_list_all_physical_get", return_value=(True, {"type": {"name": "TAX"}}))
async def test_when_sending_right_params_to_get_w8_pdf_link_then_return_the_expected(
        mock_call_list_all_physical_get, mock_call_get_physical_get
):
    response = await DriveWealthService.get_w8_pdf_link(
        user_dw_id=user_dw_id_stub
    )
    assert response == ""
