# STANDARD IMPORTS
from http import HTTPStatus

# THIRD PARTY IMPORTS
from etria_logger import Gladsheim
import flask

# PROJECT IMPORTS
from src.domain.enums.status_code import InternalCode
from src.domain.models.jwt.models import Jwt
from src.domain.models.response.model import ResponseModel
from src.services.drive_wealth.service import DriveWealthService
from src.domain.exceptions.exceptions import (
    ErrorOnDecodeJwt,
    ErrorOnListingPhysicalW8,
    ErrorOnGettingPhysicalW8,
    ErrorResponseDriveWealth
)


async def get_w8_ben() -> flask.Response:
    thebes_answer = flask.request.headers.get("x-thebes-answer")

    try:
        jwt_data = Jwt(jwt=thebes_answer)
        await jwt_data()

        w8_ben_link = await DriveWealthService.get_w8_pdf_link(
            jwt_data=jwt_data
        )

        response = ResponseModel(
            success=bool(w8_ben_link),
            result=w8_ben_link,
            message="The W8 BEN Link was generated successfully",
            code=InternalCode.SUCCESS.value
        ).build_http_response(status=HTTPStatus.OK)

        return response

    except ErrorOnDecodeJwt as error:
        Gladsheim.error(error=error, message=error.msg)
        response = ResponseModel(
            success=False,
            code=InternalCode.JWT_INVALID,
            message="Invalid JWT"
        ).build_http_response(status=HTTPStatus.UNAUTHORIZED)
        return response

    except ErrorOnListingPhysicalW8 as error:
        Gladsheim.error(error=error, message=error.msg)
        response = ResponseModel(
            success=False,
            code=InternalCode.ERROR_LISTING_W8_BEN,
            message="DriveWealth::get_w8_pdf_link::error_on_listing_physical_w8"
        ).build_http_response(status=HTTPStatus.UNAUTHORIZED)
        return response

    except ErrorOnGettingPhysicalW8 as error:
        Gladsheim.error(error=error, message=error.msg)
        response = ResponseModel(
            success=False,
            code=InternalCode.ERROR_GETTING_W8_BEN,
            message="DriveWealth::get_w8_pdf_link::error_on_getting_physical_w8_ben"
        ).build_http_response(status=HTTPStatus.UNAUTHORIZED)
        return response

    except ErrorResponseDriveWealth as error:
        Gladsheim.error(error=error, message=error.msg)
        response = ResponseModel(
            success=False,
            code=InternalCode.RESPONSE_ERROR_DRIVE_WEALTH,
            message="DriveWealth::dw_caller_transport.execute_get"
        ).build_http_response(status=HTTPStatus.UNAUTHORIZED)
        return response

    except ValueError as ex:
        Gladsheim.error(error=ex, message=str(ex))
        response = ResponseModel(
            success=False,
            code=InternalCode.INVALID_PARAMS,
            message="Invalid params"
        ).build_http_response(status=HTTPStatus.BAD_REQUEST)
        return response

    except Exception as ex:
        Gladsheim.error(error=ex, message=str(ex))
        response = ResponseModel(
            success=False,
            code=InternalCode.INTERNAL_SERVER_ERROR,
            message="Unexpected error occurred"
        ).build_http_response(status=HTTPStatus.INTERNAL_SERVER_ERROR)
        return response
