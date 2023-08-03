# wilem

Domain fuzzer, words analyzer y comparator, oriented to phishing domains filters.

## Domain fuzzer

```python
from wilem import fuzzer
from wilem import constants

fuzzer_config = fuzzer.FuzzerDomainConfig(tld_permutation_list=constants.DOMAIN_TLDS, append_word_list=constants.DOMAIN_APPEND_WORDS)
fuzzer = fuzzer.FuzzerDomain("https://google.com", fuzzer_config)
fuzzer.generate()

len(fuzzer.get_fuzzed_as_set())  # 344881
"home.google.ph" in fuzzer.get_fuzzed_as_set()  # True
```
