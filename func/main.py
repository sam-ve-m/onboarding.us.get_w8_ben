# STANDARD IMPORTS
from http import HTTPStatus

# THIRD PARTY IMPORTS
from etria_logger import Gladsheim
from flask import request, Response, Request

# PROJECT IMPORTS
from src.domain.enums.status_code import InternalCode
from src.domain.response.model import ResponseModel
from src.services.drive_wealth.service import DriveWealthService
from src.services.jwt_service.service import JWTService
from src.domain.exceptions.exceptions import (ErrorOnDecodeJwt,
                                              ErrorOnListingPhysicalW8,
                                              ErrorOnGettingPhysicalW8,
                                              ErrorResponseDriveWealth
                                              )


async def get_w8_ben(request_body: Request = request) -> Response:
    jwt_data = request_body.headers.get("x-thebes-answer")
    user_dw_id = await JWTService.decode_jwt_and_get_unique_id(jwt_data=jwt_data)

    try:
        w8_ben_link = await DriveWealthService.get_w8_pdf_link(
            user_dw_id=user_dw_id
        )

        response = ResponseModel(
            success=bool(w8_ben_link),
            result=w8_ben_link,
            message="The W8 BEN Link was generated successfully",
            code=InternalCode.SUCCESS
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

    except ValueError:
        response = ResponseModel(
            success=False,
            code=InternalCode.INVALID_PARAMS,
            message="Invalid params"
        ).build_http_response(status=HTTPStatus.BAD_REQUEST)
        return response

    except Exception as ex:
        Gladsheim.error(error=ex)
        response = ResponseModel(
            success=False,
            code=InternalCode.INTERNAL_SERVER_ERROR,
            message="Unexpected error occurred"
        ).build_http_response(status=HTTPStatus.INTERNAL_SERVER_ERROR)
        return response
