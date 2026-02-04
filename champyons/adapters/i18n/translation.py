import gettext as gt

from typing import Optional, Sequence, Union, Callable, Any
from champyons.core.config import config
from .context import get_lang

# --- Cache and types -------------------------------------------------------
Translations = Union[gt.GNUTranslations, gt.NullTranslations]
_catalog_cache: dict[str, Translations] = {}

class SafeDict(dict):
    """A dict that returns {key} if the key is missing."""
    def __missing__(self, key):
        return f"{{{key}}}"

# --- Core translation logic --------------------------------------------------
def _load_catalog(lang_code: str, domains: Sequence[str] = config.default_domains) -> Translations:
    """
    Load and merge translation catalogs for a given language across multiple domains.
    Fallback order: specific -> base -> NullTranslations.
    """
    cache_key = f"{lang_code}:{','.join(domains)}"
    if cache_key in _catalog_cache:
        return _catalog_cache[cache_key]

    parts = lang_code.split("_")  # e.g., ['es', 'MX']

    # Start with safe empty catalog
    merged_catalog: Translations = gt.NullTranslations()
    first_catalog_info: Optional[dict] = None

    # Iterate domains in order
    for domain in domains:
        domain_catalog: Translations = gt.NullTranslations()

        # Build fallback chain: general -> specific
        for i in range(1, len(parts) + 1):
            subtag = "_".join(parts[:i])
            mo_path = config.locales_path / subtag / "LC_MESSAGES" / f"{domain}.mo"
            if mo_path.exists():
                with open(mo_path, "rb") as f:
                    catalog = gt.GNUTranslations(f)
                    if first_catalog_info is None:
                        first_catalog_info = catalog.info()
                    catalog.add_fallback(domain_catalog)
                    domain_catalog = catalog

        # Merge domain catalog into master catalog
        merged_catalog.add_fallback(domain_catalog)

    # Patch metadata info if available (so info().get("language") works)
    if first_catalog_info:
        try:
            merged_catalog._info = first_catalog_info  # type: ignore[attr-defined]
        except AttributeError:
            pass  # fallback safe

    _catalog_cache[cache_key] = merged_catalog
    return merged_catalog

def get_catalog(lang_code: Optional[str] = None, *domains: str) -> Translations:
    """
    Return the loaded catalog for the specified language and domains.
    If not specified, use current locale and DEFAULT_DOMAINS.
    """
    lang = lang_code or get_lang()
    return _load_catalog(lang, domains or config.default_domains)

import re
from typing import Dict


class MessageFormat:
    def __init__(self, msg: str, locale: str = "en"):
        self.msg = msg
        self.locale = locale

    def format(self, params: Dict[str, Any]) -> str:
        """
        Format the message with the given parameters.
        """
        return self._process(self.msg, params)

    def _process(self, msg: str, params: Dict[str, Any]) -> str:
        """
        Recursively parse the message for select, plural, selectordinal blocks.
        """
        # Pattern: {variable, type, body}
        pattern = re.compile(r"""
            \{
                (\w+)                   # variable name
                \s*,\s*
                (select|plural|selectordinal)  # type
                \s*,\s*
                (.*?)                   # body
            \}
        """, re.VERBOSE | re.DOTALL)

        def replacer(match):
            var_name = match.group(1)
            fmt_type = match.group(2)
            body = match.group(3)
            value = params.get(var_name)

            if fmt_type == "select":
                return self._handle_select(body, value, params)
            elif fmt_type == "plural":
                return self._handle_plural(body, value, params)
            elif fmt_type == "selectordinal":
                return self._handle_selectordinal(body, value, params)
            else:
                return str(value)

        # Recurse until all patterns are processed
        while True:
            new_msg = pattern.sub(replacer, msg)
            if new_msg == msg:
                break
            msg = new_msg

        # Replace simple variables
        for k, v in params.items():
            msg = msg.replace(f"{{{k}}}", str(v))

        return msg

    def _parse_options(self, body: str) -> Dict[str, str]:
        """
        Parse ICU-style options like: key {message} key2 {message2}.
        Supports nested braces properly.
        """
        options = {}
        i = 0
        length = len(body)

        while i < length:
            # Skip whitespace
            while i < length and body[i].isspace():
                i += 1

            # Find the key
            start_key = i
            while i < length and not body[i].isspace() and body[i] != '{':
                i += 1
            key = body[start_key:i].strip()

            # Skip spaces until '{'
            while i < length and body[i].isspace():
                i += 1
            if i >= length or body[i] != '{':
                break  # malformed

            i += 1  # skip opening brace
            start_val = i
            depth = 1
            while i < length and depth > 0:
                if body[i] == '{':
                    depth += 1
                elif body[i] == '}':
                    depth -= 1
                i += 1
            value = body[start_val:i-1].strip()
            options[key] = value
        return options

    def _handle_select(self, body: str, value, params: Dict[str, Any]) -> str:
        """
        Handle select statements: chooses a message based on the value.
        """
        options = self._parse_options(body)
        if str(value) in options:
            return self._process(options[str(value)], params)
        elif "other" in options:
            return self._process(options["other"], params)
        else:
            return ""

    def _handle_plural(self, body: str, value, params: Dict[str, Any]) -> str:
        """
        Handle plural statements with =n, one, other options.
        Replaces '#' with the actual number.
        """
        n = int(value)
        options = self._parse_options(body)

        exact_key = f"={n}"
        if exact_key in options:
            return self._process(options[exact_key].replace("#", str(n)), params)
        if n == 1 and "one" in options:
            return self._process(options["one"].replace("#", str(n)), params)
        elif "other" in options:
            return self._process(options["other"].replace("#", str(n)), params)
        else:
            return str(n)

    def _handle_selectordinal(self, body: str, value, params: Dict[str, Any]) -> str:
        """
        Handle selectordinal statements: one, two, few, other.
        Replaces '#' with the actual number.
        """
        n = int(value)
        options = self._parse_options(body)

        if n == 1 and "one" in options:
            return self._process(options["one"].replace("#", str(n)), params)
        elif n == 2 and "two" in options:
            return self._process(options["two"].replace("#", str(n)), params)
        elif n == 3 and "few" in options:
            return self._process(options["few"].replace("#", str(n)), params)
        elif "other" in options:
            return self._process(options["other"].replace("#", str(n)), params)
        else:
            return str(n)
        
def format_message(translated_string: str, **placeholders):
    " Format a translated message safely, leaving unknown placeholders intact."
    return MessageFormat(translated_string).format(placeholders)

def gettext(message: str, **placeholders) -> str:
    """
    Translate a message and format it using context variables.
    Example:
        gettext("Hello, {name}!", name="John Doe")
    """
    catalog = get_catalog()
    translated = catalog.gettext(message)

    return format_message(translated, **placeholders)

class LazyString:
    """A string-like object that evaluates the translation only when needed."""
    def __init__(self, func: Callable[[], str]):
        self._func = func

    def __str__(self):
        return self._func()

    def __repr__(self):
        return f"LazyString({str(self)})"

    def __add__(self, other):
        return str(self) + str(other)

    def __radd__(self, other):
        return str(other) + str(self)

    def __mod__(self, other):
        return str(self) % other

    def format(self, *args, **kwargs):
        return str(self).format(*args, **kwargs)
    
def lazy_gettext(message: str, **kwargs) -> LazyString:
    return LazyString(lambda: gettext(message, **kwargs))

# Common alias
_ = gettext
