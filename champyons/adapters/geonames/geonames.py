import requests
from typing import Any

from champyons.core.domain.value_objects.geography.geonames import GeonamesResult

class GeonamesApiClient:
    def __init__(self, *, username: str, timeout: int = 10, lang: str = "en", style: str = "FULL"):
        self.base_url = 'http://api.geonames.org/'
        self.username = username
        self.timeout = timeout
        self.lang = lang
        self.style = style

    @staticmethod
    def _dict_to_geoname_full(data: dict[str, Any]) -> GeonamesResult:
        """
        Convert a dict (or list of dicts) from GeoNames API to GeonamesResultFull Pydantic model.
        """
        return GeonamesResult.from_dict(data)

    @staticmethod
    def _results_to_geoname_full(dataset: list[dict[str, Any]]) -> list[GeonamesResult]:
        """
        Convert a dict (or list of dicts) from GeoNames API to GeoNaGeonamesResultFullmeFull Pydantic model.
        """
        return list([GeonamesResult.from_dict(data) for data in dataset])

    def _parse(self, endpoint: str, **query_params: Any) -> dict[str, Any]:
        url = f"{self.base_url.rstrip('/')}/{endpoint.lstrip('/')}"
        query_params["username"] = self.username
        response = requests.get(
            url,
            params=query_params,
            timeout=self.timeout,
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

    def parse_from_geonames_id(self, *, geonames_id: int|str) -> GeonamesResult:
        data = self._parse("getJSON", username= self.username, geonameId=geonames_id, style=self.d, lang=self.lang)
        return self._dict_to_geoname_full(data)

    def _parse_paginated_results(self, endpoint: str, **kwargs: Any) -> list[GeonamesResult]:
        max_rows = kwargs.pop("maxRows", 1000)


        results: list[dict[str, Any]] = []

        # get first page
        data = self._parse(endpoint, username=self.username, style=self.style, lang=self.lang, maxRows=max_rows, inclBbox=False, **kwargs)
        results.extend(data.get("geonames", []))

        # get total results from first page of results:
        total_results = data.get("totalResultsCount", 0)
        if total_results == 0:
            return self._results_to_geoname_full(results)    
        
        total_pages = (total_results + max_rows - 1) // max_rows
        
        #iterate all pages of results:
        for page_index in range(1, total_pages):
            data = self._parse(endpoint, username=self.username, style=self.style, lang=self.lang, maxRows=max_rows, inclBbox=False, startRow=page_index*max_rows, **kwargs)
            results.extend(data.get("geonames", []))

        return self._results_to_geoname_full(results)

    def parse_from_geonames_search(self, **kwargs: Any) -> list[GeonamesResult]:
        return self._parse_paginated_results("searchJSON", username=self.username, lang=self.lang, **kwargs)

    def parse_children_from_geonames_id(self, geonames_id: int|str, **kwargs) -> list[GeonamesResult]:
        return self._parse_paginated_results("childrenJSON", geonameId=geonames_id, username=self.username, lang=self.lang, **kwargs)


