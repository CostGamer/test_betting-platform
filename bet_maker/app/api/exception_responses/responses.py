from http import HTTPStatus
from typing import Any


def create_error_responses(
    error_responses: dict[int, dict[str, dict[str, Any]]]
) -> dict:
    """Generates error response schemas for an API based on provided error examples.

    This function takes a dictionary of error status codes and their associated examples,
    then constructs a response schema for each status code in a format compatible with OpenAPI.

    Args:
        error_responses (dict[int, dict[str, dict[str, Any]]]): A dictionary where the keys are
                                                              HTTP status codes (integers) and the values
                                                              are dictionaries containing response examples
                                                              for each status code.

    Returns:
        dict: A dictionary of response schemas for each error status code, where the keys are status codes
              and the values are response descriptions and examples formatted for OpenAPI specification.
    """
    responses = {}

    for status_code, examples in error_responses.items():
        description = HTTPStatus(status_code).phrase
        responses[status_code] = {
            "description": description,
            "content": {"application/json": {"examples": examples}},
        }

    return responses


get_user_register_exceptions = {
    400: {
        "user_already_exists_error": {
            "summary": "UserWithThisEmailExistsError",
            "value": {"detail": "This email already in the system"},
        },
        "email_not_valid_error": {
            "summary": "EmailNotValidError",
            "value": {"detail": "Email is not valid"},
        },
    }
}

get_user_login_exceptions = {
    400: {
        "invalid_username_password_error": {
            "summary": "InvalidUsernameOrPasswordError",
            "value": {"detail": "Invalid password or username"},
        },
    }
}

get_token_reissue_exceptions = {
    400: {
        "invalid_jwt_error": {
            "summary": "InvalidTokenError",
            "value": {"detail": "Invalid jwt"},
        },
    },
    409: {
        "refresh_token_expect_error": {
            "summary": "ExpectRefreshTokenError",
            "value": {"detail": "Expect refresh jwt"},
        },
    },
}

post_bet_exceptions = {
    400: {
        "not_enough_money_error": {
            "summary": "NotEnoughMoneyError",
            "value": {"detail": "Top up the balance or change the amount of the bet"},
        },
        "expect_access_token_error": {
            "summary": "ExpectAccessTokenError",
            "value": {"detail": "Invalid JWT type"},
        },
    },
    401: {
        "invalid_token_error": {
            "summary": "InvalidTokenError",
            "value": {"detail": "Invalid JWT"},
        },
        "missing_or_bad_jwt_error": {
            "summary": "MissingOrBadJWTError",
            "value": {"detail": "Invalid JWT"},
        },
    },
    403: {
        "no_money_error": {
            "summary": "NoMoneyError",
            "value": {"detail": "Top up the balance"},
        },
    },
    404: {
        "event_not_found_error": {
            "summary": "EventNotFoundError",
            "value": {"detail": "Event with this name not found"},
        },
    },
}

get_all_bets_exceptions = {
    400: {
        "expect_access_token_error": {
            "summary": "ExpectAccessTokenError",
            "value": {"detail": "Invalid JWT type"},
        },
    },
    401: {
        "invalid_token_error": {
            "summary": "InvalidTokenError",
            "value": {"detail": "Invalid JWT"},
        },
        "missing_or_bad_jwt_error": {
            "summary": "MissingOrBadJWTError",
            "value": {"detail": "Invalid JWT"},
        },
    },
}

get_all_active_bets_exceptions = {
    400: {
        "expect_access_token_error": {
            "summary": "ExpectAccessTokenError",
            "value": {"detail": "Invalid JWT type"},
        },
    },
    401: {
        "invalid_token_error": {
            "summary": "InvalidTokenError",
            "value": {"detail": "Invalid JWT"},
        },
        "missing_or_bad_jwt_error": {
            "summary": "MissingOrBadJWTError",
            "value": {"detail": "Invalid JWT"},
        },
    },
}

get_user_info_exceptions = {
    400: {
        "expect_access_token_error": {
            "summary": "ExpectAccessTokenError",
            "value": {"detail": "Invalid JWT type"},
        },
    },
    401: {
        "invalid_token_error": {
            "summary": "InvalidTokenError",
            "value": {"detail": "Invalid JWT"},
        },
        "missing_or_bad_jwt_error": {
            "summary": "MissingOrBadJWTError",
            "value": {"detail": "Invalid JWT"},
        },
    },
}


get_balance_top_up_exceptions = {
    400: {
        "expect_access_token_error": {
            "summary": "ExpectAccessTokenError",
            "value": {"detail": "Invalid JWT type"},
        },
        "not_enough_money_error": {
            "summary": "NotEnoughMoneyError",
            "value": {"detail": "Top up the balance or change the amount of the bet"},
        },
    },
    401: {
        "invalid_token_error": {
            "summary": "InvalidTokenError",
            "value": {"detail": "Invalid JWT"},
        },
        "missing_or_bad_jwt_error": {
            "summary": "MissingOrBadJWTError",
            "value": {"detail": "Invalid JWT"},
        },
    },
}


get_balance_withdraw_exceptions = {
    400: {
        "expect_access_token_error": {
            "summary": "ExpectAccessTokenError",
            "value": {"detail": "Invalid JWT type"},
        },
        "not_enough_money_error": {
            "summary": "NotEnoughMoneyError",
            "value": {"detail": "Top up the balance or change the amount of the bet"},
        },
    },
    401: {
        "invalid_token_error": {
            "summary": "InvalidTokenError",
            "value": {"detail": "Invalid JWT"},
        },
        "missing_or_bad_jwt_error": {
            "summary": "MissingOrBadJWTError",
            "value": {"detail": "Invalid JWT"},
        },
    },
}

get_user_register_responses = create_error_responses(get_user_register_exceptions)
get_user_login_responses = create_error_responses(get_user_login_exceptions)
get_token_reissue_responses = create_error_responses(get_token_reissue_exceptions)
post_bet_responses = create_error_responses(post_bet_exceptions)
get_all_bets_responses = create_error_responses(get_all_bets_exceptions)
get_all_active_bets_responses = create_error_responses(get_all_active_bets_exceptions)
get_user_info_responses = create_error_responses(get_user_info_exceptions)
get_balance_top_up_responses = create_error_responses(get_balance_top_up_exceptions)
get_balance_withdraw_responses = create_error_responses(get_balance_withdraw_exceptions)
