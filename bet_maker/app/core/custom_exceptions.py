class UserWithThisEmailExistsError(Exception):
    pass


class InvalidUsernameOrPasswordError(Exception):
    pass


class ExpectRefreshTokenError(Exception):
    pass


class MissingOrBadJWTError(Exception):
    pass


class ExpectAccessTokenError(Exception):
    pass
