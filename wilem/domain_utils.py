import re
from typing import NamedTuple

import tld as tld_module

ParsedDomain = NamedTuple("ParsedDomain", [("subdomain", str), ("domain", str), ("tld", str)])


def validate_domain_str(domain: str) -> bool:
    """
    Validates the domain.
    """
    try:
        tld_module.get_fld(domain, fix_protocol=True)
        pattern = re.compile(r"^(?:http(s)?:\/\/)?[\w%.-]+(?:\.[\w\.-]+)+[\w%\-\._~:\/?#[\]@!\$&'\(\)\*\+,;=.%]+$")
        if not pattern.match(domain):
            return False
    except Exception:
        return False
    return True


def parse_domain(domain: str, fix_protocol: bool = False) -> ParsedDomain:
    """
    Returns all parts of the URL as namedtuple.
    If the domain is invalid raises ValueError.
    Attrs: subdomain, domain, tld.
    """
    if not validate_domain_str(domain):
        raise ValueError("Invalid domain.")
    tld_object: tld_module.Result = tld_module.get_tld(domain, fix_protocol=fix_protocol, as_object=True)  # type: ignore
    return ParsedDomain(tld_object.subdomain, tld_object.domain, tld_object.tld)
