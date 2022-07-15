# STANDARD IMPORTS
from unittest.mock import patch
from flask import Flask
import pytest
from werkzeug.test import Headers

# PROJECT IMPORTS
from src.services.drive_wealth.service import DriveWealthService
from src.services.jwt_service.service import JWTService
from main import get_w8_ben

# STUB IMPORTS
from tests.main_stub import stub_dw_link, response_bytes_stub, user_dw_id_stub, request_body_stub


@pytest.mark.asyncio
@patch.object(JWTService, "decode_jwt_and_get_unique_id", return_value=user_dw_id_stub)
@patch.object(DriveWealthService, "get_w8_pdf_link", return_value=stub_dw_link)
async def test_get_w8_ben_when_sending_right_params_then_return_the_expected(
        mock_decode_jwt_and_get_unique_id, mock_get_w8_pdf_link
):
    app = Flask(__name__)
    with app.test_request_context(
            request_body_stub,
            headers=Headers({"x-thebes-answer": "jwt_to_decode_stub"}),
    ).request as request:
        response = await get_w8_ben(request_body=request)
        assert response.data == response_bytes_stub


@pytest.mark.asyncio
async def test_get_w8_ben_when_not_sending_right_request_body_right_params_then_return_the_expected():
    with pytest.raises(AttributeError):
        await get_w8_ben(request_body=None)
