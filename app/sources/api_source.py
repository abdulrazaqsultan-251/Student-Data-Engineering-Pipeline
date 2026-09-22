from typing import Any

import requests


API_URL = "https://dummyjson.com/users?limit=20"


def extract_api(
    url: str = API_URL,
    timeout: int = 10,
) -> list[dict[str, Any]]:
    """
    Extract records from a REST API.

    Parameters
    ----------
    url:
        REST API endpoint.
    timeout:
        Request timeout in seconds.

    Returns
    -------
    list[dict[str, Any]]
        Raw API records.
    """

    try:
        response = requests.get(
            url,
            timeout=timeout,
        )

        response.raise_for_status()

    except requests.RequestException as exc:
        raise RuntimeError(
            f"API extraction failed: {url}"
        ) from exc

    data = response.json()

    if not isinstance(data, dict):
        raise ValueError(
            "API response must be a JSON object."
        )

    records = data.get("users")

    if not isinstance(records, list):
        raise ValueError(
            "API response does not contain "
            "a valid 'users' list."
        )

    if not records:
        raise ValueError(
            "API returned no user records."
        )

    return records