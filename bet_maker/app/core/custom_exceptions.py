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


class EventNotFoundError(Exception):
    pass


class NoMoneyError(Exception):
    pass


class NotEnoughMoneyError(Exception):
    pass
