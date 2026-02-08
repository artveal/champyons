from functools import lru_cache
from pathlib import Path
from fluent.runtime import FluentLocalization, FluentResourceLoader

class FluentCache:
    """ Cache of Fluent localizations by language"""
    def __init__(self, locales_dir: Path, files: list[str]):
        """
        Args:
            locales_dir: locales directory (e.g. /locales/fluent)
            files: list of .ftl diles to be loaded (e.g. ["messages.ftl", "game.ftl"])
        """
        self.locales_dir = locales_dir
        self.files = files

    @lru_cache(maxsize=32)
    def get(self, language: str, fallback: str = "en") -> FluentLocalization:
        """
        Get cached localization for language.
        
        Args:
            language: main language. If it is an specific local variante (eg. "es_AR"), an automatic, generic fallback will be added as well ("es")
            fallback: language that will be used if no main langugage is found
        """

        loader = FluentResourceLoader(str(self.locales_dir / "{locale}/"))

        locales = [language, fallback]
        normalized_lang = language.split("_")[0]
        if normalized_lang not in locales:
            locales.insert(1, normalized_lang)
        return FluentLocalization(
            locales=locales,
            resource_ids=self.files,
            resource_loader=loader
        )
    
    def clear(self) -> None:
        """ Clears cache """
        self.get.cache_clear()
    
    def info(self) -> dict:
        cache_info = self.get.cache_info()
        return {
            "hits": cache_info.hits,
            "misses": cache_info.misses,
            "size": cache_info.currsize,
            "max_size": cache_info.maxsize
        }