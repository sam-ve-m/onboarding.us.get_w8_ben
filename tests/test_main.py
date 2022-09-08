# PROJECT IMPORTS
from http import HTTPStatus

import flask
import pytest
from unittest.mock import patch, MagicMock

from decouple import RepositoryEnv, Config
import logging.config


with patch.object(RepositoryEnv, "__init__", return_value=None):
    with patch.object(Config, "__init__", return_value=None):
        with patch.object(Config, "__call__"):
            with patch.object(logging.config, "dictConfig"):
                from etria_logger import Gladsheim
                from main import get_w8_ben
                from src.domain.models.jwt.models import Jwt
                from src.domain.enums.status_code import InternalCode
                from src.domain.models.response.model import ResponseModel
                from src.domain.exceptions.exceptions import ErrorOnDecodeJwt, UserUniqueIdDoesNotExists, \
                    ErrorOnListingPhysicalW8, ErrorOnGettingPhysicalW8, ErrorResponseDriveWealth
                from src.services.drive_wealth.service import DriveWealthService


error_on_decode_jwt_case = (
    ErrorOnDecodeJwt(),
    ErrorOnDecodeJwt.msg,
    InternalCode.JWT_INVALID,
    "Invalid JWT",
    HTTPStatus.UNAUTHORIZED
)
error_on_listing_physical_w8_case = (
    ErrorOnListingPhysicalW8(),
    ErrorOnListingPhysicalW8.msg,
    InternalCode.ERROR_LISTING_W8_BEN,
    "DriveWealth::get_w8_pdf_link::error_on_listing_physical_w8",
    HTTPStatus.UNAUTHORIZED
)
error_on_getting_physical_w8_case = (
    ErrorOnGettingPhysicalW8(),
    ErrorOnGettingPhysicalW8.msg,
    InternalCode.ERROR_GETTING_W8_BEN,
    "DriveWealth::get_w8_pdf_link::error_on_getting_physical_w8_ben",
    HTTPStatus.UNAUTHORIZED
)
error_response_drive_wealth_case = (
    ErrorResponseDriveWealth(),
    ErrorResponseDriveWealth.msg,
    InternalCode.RESPONSE_ERROR_DRIVE_WEALTH,
    "DriveWealth::dw_caller_transport.execute_get",
    HTTPStatus.UNAUTHORIZED
)
value_exception_case = (
    ValueError("dummy"),
    "dummy",
    InternalCode.INVALID_PARAMS,
    "Invalid params",
    HTTPStatus.BAD_REQUEST
)
exception_case = (
    Exception("dummy"),
    "dummy",
    InternalCode.INTERNAL_SERVER_ERROR,
    "Unexpected error occurred",
    HTTPStatus.INTERNAL_SERVER_ERROR
)


@pytest.mark.asyncio
@pytest.mark.parametrize("exception,error_message,internal_status_code,response_message,response_status_code", [
    error_on_decode_jwt_case,
    error_on_listing_physical_w8_case,
    error_on_getting_physical_w8_case,
    error_response_drive_wealth_case,
    value_exception_case,
    exception_case,
])
@patch.object(DriveWealthService, "get_w8_pdf_link")
@patch.object(Gladsheim, "error")
@patch.object(Jwt, "__init__", return_value=None)
@patch.object(Jwt, "__call__")
@patch.object(ResponseModel, "__init__", return_value=None)
@patch.object(ResponseModel, "build_http_response")
async def test_get_w8_ben_raising_errors(
            mocked_build_response, mocked_response_instance,
            mocked_jwt_decode, mocked_jwt_instance, mocked_logger, mocked_service, monkeypatch,
            exception, error_message, internal_status_code, response_message, response_status_code,
):
    monkeypatch.setattr(flask, "request", MagicMock())
    mocked_jwt_decode.side_effect = exception
    await get_w8_ben()
    mocked_service.assert_not_called()
    mocked_logger.assert_called_once_with(error=exception, message=error_message)
    mocked_response_instance.assert_called_once_with(
        success=False,
        code=internal_status_code,
        message=response_message
    )
    mocked_build_response.assert_called_once_with(status=response_status_code)


dummy_response = "response"


@pytest.mark.asyncio
@patch.object(DriveWealthService, "get_w8_pdf_link", return_value=dummy_response)
@patch.object(Gladsheim, "error")
@patch.object(Jwt, "__init__", return_value=None)
@patch.object(Jwt, "__call__")
@patch.object(ResponseModel, "__init__", return_value=None)
@patch.object(ResponseModel, "build_http_response", return_value=dummy_response)
async def test_get_w8_ben(
            mocked_build_response, mocked_response_instance, mocked_jwt_decode,
            mocked_jwt_instance, mocked_logger, mocked_service, monkeypatch,
):
    monkeypatch.setattr(flask, "request", MagicMock())
    response = await get_w8_ben()
    mocked_jwt_decode.assert_called()
    mocked_service.assert_called()
    mocked_logger.assert_not_called()
    mocked_response_instance.assert_called_once_with(
        success=True,
        code=InternalCode.SUCCESS.value,
        message="The W8 BEN Link was generated successfully",
        result=dummy_response
    )
    mocked_build_response.assert_called_once_with(status=HTTPStatus.OK)
    assert dummy_response == response
