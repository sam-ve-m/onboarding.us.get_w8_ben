# STANDARD LIBRARIES
import pytest
from unittest.mock import patch, Mock

# PROJECT IMPORTS
from src.domain.exceptions.exceptions import ErrorOnListingPhysicalW8, ErrorOnGettingPhysicalW8
from src.repositories.mongo_db.user.repository import UserRepository
from src.services.drive_wealth.service import DriveWealthService
from src.transport.drive_wealth.transport import DWTransport

# STUB IMPORTS
from tests.src.services.drive_wealth.stub_service import (
    call_list_stub,
    get_physical_stub,
    w8_file_link_stub,
    call_list_invalid_stub,
    get_physical_invalid_stub
)

get_drive_wealth_id = "125458.hagfsdsa"


@pytest.mark.asyncio
@patch.object(DWTransport, "call_list_all_physical_get", return_value=call_list_stub)
@patch.object(DWTransport, "call_get_physical_get", return_value=get_physical_stub)
@patch.object(UserRepository, "find_one", return_value="1234565464")
async def test_when_sending_right_params_to_get_w8_pdf_link_then_return_the_expected(
        mock_call_list_all_physical_get,
        mock_call_get_physical_get,
        mock_find_one
):
    response = await DriveWealthService.get_w8_pdf_link(
        jwt_data=Mock(return_value=get_drive_wealth_id
                      ))
    assert response == w8_file_link_stub
    assert isinstance(response, str)


@pytest.mark.asyncio
@patch.object(DWTransport, "call_list_all_physical_get", return_value=call_list_invalid_stub)
@patch.object(UserRepository, "find_one", return_value="1234565464")
async def test_when_call_list_all_physical_get_is_false_then_return_internal_server_error(
        mock_call_list_all_physical_get, mock_find_one
):
    with pytest.raises(ErrorOnListingPhysicalW8):
        await DriveWealthService.get_w8_pdf_link(
            jwt_data=Mock(return_value=get_drive_wealth_id
                          ))


@pytest.mark.asyncio
@patch.object(DWTransport, "call_list_all_physical_get", return_value=call_list_stub)
@patch.object(DWTransport, "call_get_physical_get", return_value=get_physical_invalid_stub)
@patch.object(UserRepository, "find_one", return_value="1234565464")
async def test_when_call_get_physical_get_is_false_then_return_internal_server_error(
        mock_call_list_all_physical_get, mock_call_get_physical_get, mock_find_one
):
    with pytest.raises(ErrorOnGettingPhysicalW8):
        await DriveWealthService.get_w8_pdf_link(
            jwt_data=Mock(return_value=get_drive_wealth_id
                          ))
