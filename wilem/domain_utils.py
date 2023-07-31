import re
from typing import NamedTuple

import tld as tld_module

ParsedDominio = NamedTuple("ParsedDominio", [("subdominio", str), ("dominio", str), ("tld", str)])


def validar_dominio_str(dominio: str) -> bool:
    """
    Valida que el dominio sea válido.
    """
    try:
        tld_module.get_fld(dominio, fix_protocol=True)
        pattern = re.compile(r"^(?:http(s)?:\/\/)?[\w%.-]+(?:\.[\w\.-]+)+[\w%\-\._~:\/?#[\]@!\$&'\(\)\*\+,;=.%]+$")
        if not pattern.match(dominio):
            return False
    except Exception:
        return False
    return True


def parse_dominio(dominio: str, fix_protocol: bool = False) -> ParsedDominio:
    """
    Retorna las partes del dominio/url como namedptuple.
    Si el dominio es inválido lanza ValueError.
    Attrs: subdominio, dominio, tld.
    """
    if not validar_dominio_str(dominio):
        raise ValueError("Dominio inválido.")
    tld_object: tld_module.Result = tld_module.get_tld(dominio, fix_protocol=fix_protocol, as_object=True)  # type: ignore
    return ParsedDominio(tld_object.subdomain, tld_object.domain, tld_object.tld)
