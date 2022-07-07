# STANDARD IMPORTS
from http import HTTPStatus

# THIRD PARTY IMPORTS
from etria_logger import Gladsheim
from flask import request, Flask, Response

# PROJECT IMPORTS
from src.domain.enums.status_code import InternalCode
from src.domain.exceptions.exceptions import ErrorOnDecodeJwt, UserUniqueIdDoesNotExists
from src.domain.response.model import ResponseModel
from src.services.drive_wealth.service import DriveWealthService
from src.services.jwt_service import JWTService


app = Flask(__name__)


@app.route('/get_w8_ben')
async def get_w8_ben() -> Response:
    jwt_data = request.headers.get("x-thebes-answer")
    unique_id, user_dw_id = await JWTService.decode_jwt_and_get_unique_id(jwt_data=jwt_data)

    try:
        w8_ben_link = await DriveWealthService.get_w8_pdf(
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

    except UserUniqueIdDoesNotExists as error:
        Gladsheim.error(error=error, message=error.msg)
        response = ResponseModel(
            success=False,
            code=InternalCode.DATA_NOT_FOUND,
            message="Unique ID does not exists"
        ).build_http_response(status=HTTPStatus.INTERNAL_SERVER_ERROR)
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


if __name__ == "__main__":
    app.run(debug=True)
