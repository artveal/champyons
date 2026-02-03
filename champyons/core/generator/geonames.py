import requests
from typing import Any

from champyons.core.domain.value_objects.geonames import GeonamesResult

BASE_URL = 'http://api.geonames.org/'
DEFAULT_TIMEOUT = 10  # seconds
DEFAULT_LANG = "en"
DEFAULT_STYLE = "FULL"

def _dict_to_geoname_full(data: dict[str, Any]) -> GeonamesResult:
    """
    Convert a dict (or list of dicts) from GeoNames API to GeonamesResultFull Pydantic model.
    """
    return GeonamesResult.from_dict(data)

def _results_to_geoname_full(dataset: list[dict[str, Any]]) -> list[GeonamesResult]:
    """
    Convert a dict (or list of dicts) from GeoNames API to GeoNaGeonamesResultFullmeFull Pydantic model.
    """
    return list([GeonamesResult.from_dict(data) for data in dataset])

def _parse(endpoint: str, *, username: str, **query_params: Any) -> dict[str, Any]:
    url = f"{BASE_URL.rstrip('/')}/{endpoint.lstrip('/')}"
    query_params["username"] = username
    response = requests.get(
        url,
        params=query_params,
        timeout=DEFAULT_TIMEOUT,
    )
    response.raise_for_status()

    try:
        data: dict[str, Any] = response.json()
    except ValueError as exc:
        raise ValueError(f"Invalid JSON response from {response.url}") from exc

    if "status" in data:
        status: dict = data.get("status", {})
        error_code = status.get("value", "unknown")
        error_msg = status.get("message", "unknown error")
        raise RuntimeError(
            f"GeoNames API error while calling {response.url}: "
            f"[{error_code}] {error_msg}"
        )

    return data

def parse_from_geonames_id(*, username: str, geonames_id: int|str, lang: str|None = None) -> GeonamesResult:
    data = _parse("getJSON", username= username, geonameId=geonames_id, style=DEFAULT_STYLE, lang=lang or DEFAULT_LANG)
    return _dict_to_geoname_full(data)

def _parse_paginated_results(endpoint: str, *, username: str, lang: str|None = None, **kwargs: Any) -> list[GeonamesResult]:
    max_rows = kwargs.pop("maxRows", 1000)
    language = lang or DEFAULT_LANG

    results: list[dict[str, Any]] = []

    # get first page
    data = _parse(endpoint, username=username, style=DEFAULT_STYLE, lang=language, maxRows=max_rows, inclBbox=False, **kwargs)
    results.extend(data.get("geonames", []))

    # get total results from first page of results:
    total_results = data.get("totalResultsCount", 0)
    if total_results == 0:
        return _results_to_geoname_full(results)    
    
    total_pages = (total_results + max_rows - 1) // max_rows
    
    #iterate all pages of results:
    for page_index in range(1, total_pages):
        data = _parse(endpoint, username=username, style=DEFAULT_STYLE, lang=language, maxRows=max_rows, inclBbox=False, startRow=page_index*max_rows, **kwargs)
        results.extend(data.get("geonames", []))

    return _results_to_geoname_full(results)

def parse_from_geonames_search(*, username: str, lang: str|None = None, **kwargs: Any) -> list[GeonamesResult]:
    return _parse_paginated_results("searchJSON", username=username, lang=lang, **kwargs)

def parse_children_from_geonames_id(*, username: str, geonames_id: int|str, lang: str|None = None, **kwargs) -> list[GeonamesResult]:
    return _parse_paginated_results("childrenJSON", geonameId=geonames_id, username=username, lang=lang, **kwargs)


