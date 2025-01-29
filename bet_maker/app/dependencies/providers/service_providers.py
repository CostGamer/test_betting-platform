from dishka import Provider, Scope, provide

from bet_maker.app.core.schemas.repo_protocols import (
    AuthRepoProtocol,
    BetRepoProtocol,
    CommonRepoProtocol,
    RedisRepoProtocol,
    UserRepoProtocol,
)
from bet_maker.app.core.schemas.service_protocols import (
    BackgroundTasksServiceProtocol,
    BalanceServiceProtocol,
    CommonServiceProtocol,
    GetActiveBetsServiceProtocol,
    GetBetsServiceProtocol,
    GetEventsServiceProtocol,
    GetUserInfoServiceProtocol,
    JWTServiceProtocol,
    LoginAuthServiceProtocol,
    PostBetServiceProtocol,
    RegisterAuthServiceProtocol,
    ReissueTokenServiceProtocol,
)
from bet_maker.app.services.auth_service import (
    LoginAuthService,
    RegisterAuthService,
    ReissueTokenService,
)
from bet_maker.app.services.background_task_service import BackgroundTasksService
from bet_maker.app.services.bet_service import (
    GetActiveBetsService,
    GetBetsService,
    PostBetService,
)
from bet_maker.app.services.common_service import CommonService
from bet_maker.app.services.consumer_service import ConsumerService
from bet_maker.app.services.events_service import GetEventsService
from bet_maker.app.services.jwt_service import JWTService
from bet_maker.app.services.user_service import BalanceService, GetUserInfoService
from shared.configs.rabbitmq import RabbitBaseConnection
from shared.configs.settings import Settings


class ServiceProvidersLine(Provider):
    @provide(scope=Scope.REQUEST)
    async def get_consumer_service(
        self,
        rbmq_config: RabbitBaseConnection,
        redis: RedisRepoProtocol,
        settings: Settings,
    ) -> ConsumerService:
        return ConsumerService(rbmq_config, redis, settings)

    @provide(scope=Scope.REQUEST)
    async def get_event_service(
        self, redis_repo: RedisRepoProtocol
    ) -> GetEventsServiceProtocol:
        return GetEventsService(redis_repo)

    @provide(scope=Scope.REQUEST)
    async def get_bg_task_service(
        self,
        bet_repo: BetRepoProtocol,
        event_service: GetEventsServiceProtocol,
        user_repo: UserRepoProtocol,
    ) -> BackgroundTasksServiceProtocol:
        return BackgroundTasksService(bet_repo, event_service, user_repo)

    @provide(scope=Scope.REQUEST)
    async def get_jwt_service(
        self, common_repo: CommonRepoProtocol
    ) -> JWTServiceProtocol:
        return JWTService(common_repo)

    @provide(scope=Scope.REQUEST)
    async def get_register_service(
        self, auth_repo: AuthRepoProtocol, common_repo: CommonRepoProtocol
    ) -> RegisterAuthServiceProtocol:
        return RegisterAuthService(auth_repo, common_repo)

    @provide(scope=Scope.REQUEST)
    async def get_login_service(
        self, jwt_service: JWTServiceProtocol
    ) -> LoginAuthServiceProtocol:
        return LoginAuthService(jwt_service)

    @provide(scope=Scope.REQUEST)
    async def get_reissue_service(
        self, jwt_service: JWTServiceProtocol, common_repo: CommonRepoProtocol
    ) -> ReissueTokenServiceProtocol:
        return ReissueTokenService(jwt_service, common_repo)

    @provide(scope=Scope.REQUEST)
    async def get_common_service(
        self, jwt_service: JWTServiceProtocol
    ) -> CommonServiceProtocol:
        return CommonService(jwt_service)

    @provide(scope=Scope.REQUEST)
    async def get_post_bet_service(
        self,
        bet_repo: BetRepoProtocol,
        event_service: GetEventsServiceProtocol,
        user_repo: UserRepoProtocol,
        common_service: CommonServiceProtocol,
    ) -> PostBetServiceProtocol:
        return PostBetService(bet_repo, event_service, user_repo, common_service)

    @provide(scope=Scope.REQUEST)
    async def get_bets_service(
        self,
        bet_repo: BetRepoProtocol,
        common_service: CommonServiceProtocol,
    ) -> GetBetsServiceProtocol:
        return GetBetsService(bet_repo, common_service)

    @provide(scope=Scope.REQUEST)
    async def get_active_bets_service(
        self, bet_repo: BetRepoProtocol, common_service: CommonServiceProtocol
    ) -> GetActiveBetsServiceProtocol:
        return GetActiveBetsService(bet_repo, common_service)

    @provide(scope=Scope.REQUEST)
    async def get_user_info_service(
        self, user_repo: UserRepoProtocol, common_service: CommonServiceProtocol
    ) -> GetUserInfoServiceProtocol:
        return GetUserInfoService(user_repo, common_service)

    @provide(scope=Scope.REQUEST)
    async def get_balance_service(
        self, user_repo: UserRepoProtocol, common_service: CommonServiceProtocol
    ) -> BalanceServiceProtocol:
        return BalanceService(user_repo, common_service)
