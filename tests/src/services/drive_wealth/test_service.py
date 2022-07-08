# STANDARD LIBRARIES
import pytest
from unittest.mock import patch

# PROJECT IMPORTS
from func.src.domain.exceptions.exceptions import ErrorOnListingPhysicalW8, ErrorOnGettingPhysicalW8
from func.src.services.drive_wealth.service import DriveWealthService
from func.src.transport.drive_wealth.transport import DWTransport

# STUB IMPORTS
from tests.src.services.drive_wealth.stub_service import call_list_stub, get_physical_stub, user_dw_id_stub, \
    w8_file_link_stub, call_list_invalid_stub, get_physical_invalid_stub


@pytest.mark.asyncio
@patch.object(DWTransport, "call_list_all_physical_get", return_value=call_list_stub)
@patch.object(DWTransport, "call_get_physical_get", return_value=get_physical_stub)
async def test_when_sending_right_params_to_get_w8_pdf_link_then_return_the_expected(
        mock_call_list_all_physical_get, mock_call_get_physical_get
):
    response = await DriveWealthService.get_w8_pdf_link(
        user_dw_id=user_dw_id_stub
    )
    assert response == w8_file_link_stub
    assert isinstance(response, str)


@pytest.mark.asyncio
@patch.object(DWTransport, "call_list_all_physical_get", return_value=call_list_invalid_stub)
async def test_when_call_list_all_physical_get_is_false_then_return_internal_server_error(
        mock_call_list_all_physical_get
):
    with pytest.raises(ErrorOnListingPhysicalW8):
        await DriveWealthService.get_w8_pdf_link(
            user_dw_id=user_dw_id_stub
        )


@pytest.mark.asyncio
@patch.object(DWTransport, "call_list_all_physical_get", return_value=call_list_stub)
@patch.object(DWTransport, "call_get_physical_get", return_value=get_physical_invalid_stub)
async def test_when_call_get_physical_get_is_false_then_return_internal_server_error(
        mock_call_list_all_physical_get, mock_call_get_physical_get
):
    with pytest.raises(ErrorOnGettingPhysicalW8):
        await DriveWealthService.get_w8_pdf_link(
            user_dw_id=user_dw_id_stub
        )
