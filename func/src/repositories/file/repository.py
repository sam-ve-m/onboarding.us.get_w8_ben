# STANDARD LIBS
from base64 import b64encode
from enum import Enum
from typing import Union, Optional
from aiohttp import ClientSession

# OUTSIDE LIBRARIES
from func.src.domain.exceptions.exceptions import InternalServerError
from func.src.infrastructure.s3.infrastructure import S3Infrastructure
from func.src.repositories.cache.repository import RepositoryRedis
from func.src.repositories.file.enum.term_file import TermsFileType
from func.src.repositories.file.user_file import UserFileType


class FileRepository:

    infra = S3Infrastructure
    cache = RepositoryRedis

    # This dict keys must be TermsFileType, UserFileType constants
    _file_extension_by_type = {
        "user_selfie": ".jpg",
        "document_front": ".jpg",
        "document_back": ".jpg",
        "term_application": ".pdf",
        "term_open_account": ".pdf",
        "term_refusal": ".pdf",
        "term_non_compliance": ".pdf",
        "term_retail_liquid_provider": ".pdf",
        "term_open_account_dw": ".pdf",
        "term_application_dw": ".pdf",
        "term_and_privacy_policy_data_sharing_policy_dw": ".pdf",
        "term_disclosures_and_disclaimers": ".pdf",
        "term_money_corp": ".pdf",
        "term_gringo_world": ".pdf",
        "term_gringo_world_general_advices": ".pdf",
    }

    @classmethod
    async def save_user_file(
        cls,
        file_type: UserFileType,
        content: Union[str, bytes],
        unique_id: str,
        bucket_name: str,
    ) -> str:
        path = await cls._resolve_user_path(unique_id=unique_id, file_type=file_type)
        file_name = file_type.value
        file_extension = cls._get_file_extension_by_type(file_type=file_type)
        if not path or not file_name or not file_extension:
            raise InternalServerError("files.error")
        fully_qualified_path = f"{path}{file_name}{file_extension}"
        async with cls.infra.get_client() as s3_client:
            await s3_client.upload_fileobj(
                cls._resolve_content(content=content),
                bucket_name,
                fully_qualified_path,
            )
        return fully_qualified_path

    @classmethod
    async def get_user_file(
        cls,
        file_type: UserFileType,
        unique_id: str,
        bucket_name: str,
    ) -> Union[str, dict]:
        path = await cls._resolve_user_path(unique_id=unique_id, file_type=file_type)
        file_name = file_type.value
        file_extension = cls._get_file_extension_by_type(file_type=file_type)
        if not path or not file_name or not file_extension:
            raise InternalServerError("files.error")
        fully_qualified_path = f"{path}{file_name}{file_extension}"
        url = None
        async with cls.infra.get_client() as s3_client:
            url = await s3_client.generate_presigned_url(
                "get_object",
                Params={"Bucket": bucket_name, "Key": fully_qualified_path},
                ExpiresIn=604800,
            )
        return url

    @classmethod
    async def get_file_as_base_64(
        cls,
        file_type: UserFileType,
        unique_id: str,
        bucket_name: str,
    ) -> str:
        url = await cls.get_user_file(
            file_type=file_type, unique_id=unique_id, bucket_name=bucket_name
        )
        if url is None:
            raise InternalServerError("files.error")
        async with ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    byte_content = await response.read()
                    base_64_content = b64encode(byte_content).decode()
                    return f"data:image/jpeg;base64,{base_64_content}"
                raise InternalServerError("files.error")

    @classmethod
    def _get_file_extension_by_type(cls, file_type: Enum) -> Optional[str]:
        valid_files = list()
        for file_enum in [UserFileType, TermsFileType]:
            valid_files += [item.value for item in file_enum]
        if file_type.value not in valid_files:
            raise InternalServerError("files.error")
        return cls._file_extension_by_type.get(file_type.value)
