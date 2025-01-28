from .auth_service_protocols import (
    LoginAuthServiceProtocol,
    RegisterAuthServiceProtocol,
    ReissueTokenServiceProtocol,
)
from .bet_service_protocols import (
    GetActiveBetsServiceProtocol,
    GetBetsServiceProtocol,
    PostBetServiceProtocol,
)
from .common_service_protocols import CommonServiceProtocol
from .cookie_protocols import EstablishCookiesProtocol
from .events_protocols import GetEventsServiceProtocol
from .jwt_service_protocols import JWTServiceProtocol
from .user_service_protocols import BalanceServiceProtocol, GetUserInfoServiceProtocol

__all__ = [
    "JWTServiceProtocol",
    "EstablishCookiesProtocol",
    "LoginAuthServiceProtocol",
    "RegisterAuthServiceProtocol",
    "ReissueTokenServiceProtocol",
    "GetEventsServiceProtocol",
    "PostBetServiceProtocol",
    "CommonServiceProtocol",
    "GetBetsServiceProtocol",
    "GetActiveBetsServiceProtocol",
    "GetUserInfoServiceProtocol",
    "BalanceServiceProtocol",
]
