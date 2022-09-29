class ErrorOnDecodeJwt(Exception):
    msg = "Jormungandr-Onboarding::decode_jwt_and_get_unique_id::Fail when trying to get unique_id," \
          " jwt not decoded successfully"


class UserUniqueIdDoesNotExists(Exception):
    msg = "Jormungandr-Onboarding::get_registration_data::Not exists an user with this unique_id"


class InternalServerError(Exception):
    pass


class ErrorResponseDriveWealth(Exception):
    msg = "Jormungandr-Onboarding::DriveWealth::dw_caller_transport.execute_get"


class ErrorOnListingPhysicalW8(Exception):
    msg = "Jormungandr-Onboarding::DriveWealth::dw_transport.call_list_all_physical_get"


class ErrorOnGettingPhysicalW8(Exception):
    msg = "Jormungandr-Onboarding::DriveWealth::dw_transport.call_list_all_physical_get"
