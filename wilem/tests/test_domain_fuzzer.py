import pytest

from wilem.exceptions import FuzzerConfigException
from wilem.fuzzer import FuzzerDomain, FuzzerDomainConfig


def test_domain_fuzzer_default_config() -> None:
    f = FuzzerDomain("http://google.com")
    f.generate()
    assert "goog1e.com" in f.get_fuzzed_as_list()


def test_domain_misconfiguration() -> None:
    with pytest.raises(FuzzerConfigException):
        c = FuzzerDomainConfig(tld=False, tld_permutation_list=["com.ar", "ph"])
        FuzzerDomain("http://google.com", c)
