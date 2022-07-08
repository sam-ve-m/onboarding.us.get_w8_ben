# STANDARD LIBRARIES
import pytest
from unittest.mock import patch

# PROJECT IMPORTS
from heimdall_client import Heimdall, HeimdallStatusResponses

from src.domain.exceptions.exceptions import ErrorOnDecodeJwt
from src.repositories.mongo_db.user.repository import UserRepository
from src.services.jwt_service.service import JWTService

# STUB IMPORTS
from tests.src.services.jwt_service.service_stub import jwt_decoded_stub, find_one_stub, jwt_data_stub, \
    jwt_to_decode_stub


@pytest.mark.asyncio
@patch.object(Heimdall, "decode_payload", return_value=(jwt_data_stub, HeimdallStatusResponses.SUCCESS))
@patch.object(UserRepository, "find_one", return_value=find_one_stub)
async def test_decode_jwt_and_get_unique_id_when_sending_jwt_to_decode_then_return_the_expected(
        mock_decode_payload, mock_find_one
):
    response = await JWTService.decode_jwt_and_get_unique_id(
        jwt_data=jwt_to_decode_stub
    )
    assert response == '89c69304-018a-40b7-be5b-2121c16e109e.1651525277006'
    assert isinstance(response, str)


@pytest.mark.asyncio
@patch.object(Heimdall, "decode_payload", return_value=(None, HeimdallStatusResponses.INVALID_TOKEN))
async def test_decode_jwt_and_get_unique_id_when_sending_jwt_to_decode_then_return_the_expected(
        mock_decode_payload
):
    with pytest.raises(Exception):
        await JWTService.decode_jwt_and_get_unique_id(
            jwt_data=jwt_to_decode_stub
        )
