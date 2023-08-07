# wilem

Domain fuzzer, words analyzer y comparator, oriented to phishing domains filters.

## Domain fuzzer

```python
from wilem import fuzzer
from wilem import constants
fuzzer_config = fuzzer.FuzzerDomainConfig(append_word_list=constants.DOMAIN_APPEND_WORDS)
f = fuzzer.FuzzerDomain("https://google.com", fuzzer_config)
f.generate()
len(f.get_fuzzed_as_set())  # 344881
"home.google" in f.get_fuzzed_as_set()  # True
```
