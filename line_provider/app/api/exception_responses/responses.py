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


get_event_exceptions = {
    400: {
        "invalid_id_error": {
            "summary": "InvalidIDError",
            "value": {"detail": "UUID format is incorrect"},
        },
    },
    404: {
        "event_not_found_error": {
            "summary": "EventNotFoundError",
            "value": {"detail": "Event not found"},
        },
    },
}


get_event_responses = create_error_responses(get_event_exceptions)
