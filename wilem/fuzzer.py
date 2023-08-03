import re
from dataclasses import dataclass
from typing import Dict, List, Set

from wilem import domain_utils


@dataclass
class FuzzerConfig:
    bitsquatting: bool = True
    homoglyph: bool = True
    hyphenation: bool = True
    insertion: bool = True
    omission: bool = True
    repetition: bool = True
    replacement: bool = True
    transposition: bool = True
    vowel_swap: bool = True
    addition: bool = True


@dataclass
class FuzzerDominioConfig(FuzzerConfig):
    subdomain: bool = True
    append_word: bool = True
    tld: bool = True
    addition_permutable: bool = True
    insertion_permutable: bool = True
    omission_permutable: bool = True
    repetition_permutable: bool = True
    replacement_permutable: bool = True
    transposition_permutable: bool = True
    vowel_swap_permutable: bool = True


class Fuzzer:
    def __init__(self, palabra: str, config: FuzzerConfig | None = None) -> None:
        self.palabra: str = palabra
        self.config = config or FuzzerConfig()
        self.fuzzed_list_dict: List[Dict[str, str]] = []
        self.fuzzed_as_plain_list: List[str] = []
        self.fuzzed_as_set: Set[str] = set()
        self.qwerty = {
            "1": "2q",
            "2": "3wq1",
            "3": "4ew2",
            "4": "5re3",
            "5": "6tr4",
            "6": "7yt5",
            "7": "8uy6",
            "8": "9iu7",
            "9": "0oi8",
            "0": "po9",
            "q": "12wa",
            "w": "3esaq2",
            "e": "4rdsw3",
            "r": "5tfde4",
            "t": "6ygfr5",
            "y": "7uhgt6",
            "u": "8ijhy7",
            "i": "9okju8",
            "o": "0plki9",
            "p": "lo0",
            "a": "qwsz",
            "s": "edxzaw",
            "d": "rfcxse",
            "f": "tgvcdr",
            "g": "yhbvft",
            "h": "ujnbgy",
            "j": "ikmnhu",
            "k": "olmji",
            "l": "kop",
            "z": "asx",
            "x": "zsdc",
            "c": "xdfv",
            "v": "cfgb",
            "b": "vghn",
            "n": "bhjm",
            "m": "njk",
        }
        self.qwertz = {
            "1": "2q",
            "2": "3wq1",
            "3": "4ew2",
            "4": "5re3",
            "5": "6tr4",
            "6": "7zt5",
            "7": "8uz6",
            "8": "9iu7",
            "9": "0oi8",
            "0": "po9",
            "q": "12wa",
            "w": "3esaq2",
            "e": "4rdsw3",
            "r": "5tfde4",
            "t": "6zgfr5",
            "z": "7uhgt6",
            "u": "8ijhz7",
            "i": "9okju8",
            "o": "0plki9",
            "p": "lo0",
            "a": "qwsy",
            "s": "edxyaw",
            "d": "rfcxse",
            "f": "tgvcdr",
            "g": "zhbvft",
            "h": "ujnbgz",
            "j": "ikmnhu",
            "k": "olmji",
            "l": "kop",
            "y": "asx",
            "x": "ysdc",
            "c": "xdfv",
            "v": "cfgb",
            "b": "vghn",
            "n": "bhjm",
            "m": "njk",
        }
        self.azerty = {
            "1": "2a",
            "2": "3za1",
            "3": "4ez2",
            "4": "5re3",
            "5": "6tr4",
            "6": "7yt5",
            "7": "8uy6",
            "8": "9iu7",
            "9": "0oi8",
            "0": "po9",
            "a": "2zq1",
            "z": "3esqa2",
            "e": "4rdsz3",
            "r": "5tfde4",
            "t": "6ygfr5",
            "y": "7uhgt6",
            "u": "8ijhy7",
            "i": "9okju8",
            "o": "0plki9",
            "p": "lo0m",
            "q": "zswa",
            "s": "edxwqz",
            "d": "rfcxse",
            "f": "tgvcdr",
            "g": "yhbvft",
            "h": "ujnbgy",
            "j": "iknhu",
            "k": "olji",
            "l": "kopm",
            "m": "lp",
            "w": "sxq",
            "x": "wsdc",
            "c": "xdfv",
            "v": "cfgb",
            "b": "vghn",
            "n": "bhj",
        }
        self.glyphs = {
            "a": ["à", "á", "â", "ã", "ä", "å", "ɑ", "ạ", "ǎ", "ă", "ȧ", "ą"],
            "b": ["d", "lb", "ʙ", "ɓ", "ḃ", "ḅ", "ḇ", "ƅ"],
            "c": ["e", "ƈ", "ċ", "ć", "ç", "č", "ĉ"],
            "d": ["b", "cl", "dl", "ɗ", "đ", "ď", "ɖ", "ḑ", "ḋ", "ḍ", "ḏ", "ḓ"],
            "e": ["c", "é", "è", "ê", "ë", "ē", "ĕ", "ě", "ė", "ẹ", "ę", "ȩ", "ɇ", "ḛ"],
            "f": ["ƒ", "ḟ"],
            "g": ["q", "ɢ", "ɡ", "ġ", "ğ", "ǵ", "ģ", "ĝ", "ǧ", "ǥ"],
            "h": ["lh", "ĥ", "ȟ", "ħ", "ɦ", "ḧ", "ḩ", "ⱨ", "ḣ", "ḥ", "ḫ", "ẖ"],
            "i": ["1", "l", "í", "ì", "ï", "ı", "ɩ", "ǐ", "ĭ", "ỉ", "ị", "ɨ", "ȋ", "ī"],
            "j": ["ʝ", "ɉ"],
            "k": ["lk", "ik", "lc", "ḳ", "ḵ", "ⱪ", "ķ"],
            "l": ["1", "i", "ɫ", "ł"],
            "m": ["n", "nn", "rn", "rr", "ṁ", "ṃ", "ᴍ", "ɱ", "ḿ"],
            "n": ["m", "r", "ń", "ṅ", "ṇ", "ṉ", "ñ", "ņ", "ǹ", "ň", "ꞑ"],
            "o": ["0", "ȯ", "ọ", "ỏ", "ơ", "ó", "ö"],
            "p": ["ƿ", "ƥ", "ṕ", "ṗ"],
            "q": ["g", "ʠ"],
            "r": ["ʀ", "ɼ", "ɽ", "ŕ", "ŗ", "ř", "ɍ", "ɾ", "ȓ", "ȑ", "ṙ", "ṛ", "ṟ"],
            "s": ["ʂ", "ś", "ṣ", "ṡ", "ș", "ŝ", "š"],
            "t": ["ţ", "ŧ", "ṫ", "ṭ", "ț", "ƫ"],
            "u": ["ᴜ", "ǔ", "ŭ", "ü", "ʉ", "ù", "ú", "û", "ũ", "ū", "ų", "ư", "ů", "ű", "ȕ", "ȗ", "ụ"],
            "v": ["ṿ", "ⱱ", "ᶌ", "ṽ", "ⱴ"],
            "w": ["vv", "ŵ", "ẁ", "ẃ", "ẅ", "ⱳ", "ẇ", "ẉ", "ẘ"],
            "y": ["ʏ", "ý", "ÿ", "ŷ", "ƴ", "ȳ", "ɏ", "ỿ", "ẏ", "ỵ"],
            "z": ["ʐ", "ż", "ź", "ᴢ", "ƶ", "ẓ", "ẕ", "ⱬ"],
        }
        self.keyboards = [self.qwerty, self.qwertz, self.azerty]

    def bitsquatting_fuzzer(self) -> List[str]:
        result = []
        masks = [1, 2, 4, 8, 16, 32, 64, 128]
        for i in range(0, len(self.palabra)):
            c = self.palabra[i]
            for j in range(0, len(masks)):
                b = chr(ord(c) ^ masks[j])
                o = ord(b)
                if (o >= 48 and o <= 57) or (o >= 97 and o <= 122) or o == 45:
                    result.append(self.palabra[:i] + b + self.palabra[i + 1 :])
        return result

    def homoglyph_fuzzer(self) -> List[str]:
        result_1pass = set()
        for ws in range(1, len(self.palabra)):
            for i in range(0, (len(self.palabra) - ws) + 1):
                win = self.palabra[i : i + ws]
                j = 0
                while j < ws:
                    c = win[j]
                    if c in self.glyphs:
                        win_copy = win
                        for g in self.glyphs[c]:
                            win = win.replace(c, g)
                            result_1pass.add(self.palabra[:i] + win + self.palabra[i + ws :])
                            win = win_copy
                    j += 1
        result_2pass = set()
        for domain in result_1pass:
            for ws in range(1, len(domain)):
                for i in range(0, (len(domain) - ws) + 1):
                    win = domain[i : i + ws]
                    j = 0
                    while j < ws:
                        c = win[j]
                        if c in self.glyphs:
                            win_copy = win
                            for g in self.glyphs[c]:
                                win = win.replace(c, g)
                                result_2pass.add(domain[:i] + win + domain[i + ws :])
                                win = win_copy
                        j += 1
        return list(result_1pass | result_2pass)

    def hyphenation_fuzzer(self) -> List[str]:
        result = []
        for i in range(1, len(self.palabra)):
            result.append(self.palabra[:i] + "-" + self.palabra[i:])
        return result

    def insertion_fuzzer(self) -> List[str]:
        result = []
        for i in range(1, len(self.palabra) - 1):
            for keys in self.keyboards:
                if self.palabra[i] in keys:
                    for c in keys[self.palabra[i]]:
                        result.append(self.palabra[:i] + c + self.palabra[i] + self.palabra[i + 1 :])
                        result.append(self.palabra[:i] + self.palabra[i] + c + self.palabra[i + 1 :])
        return list(set(result))

    def omission_fuzzer(self) -> List[str]:
        result = []
        for i in range(0, len(self.palabra)):
            result.append(self.palabra[:i] + self.palabra[i + 1 :])
        n = re.sub(r"(.)\1+", r"\1", self.palabra)
        if n not in result and n != self.palabra:
            result.append(n)
        return list(set(result))

    def repetition_fuzzer(self) -> List[str]:
        result = []
        for i in range(0, len(self.palabra)):
            if self.palabra[i].isalpha():
                result.append(self.palabra[:i] + self.palabra[i] + self.palabra[i] + self.palabra[i + 1 :])
        return list(set(result))

    def replacement_fuzzer(self) -> List[str]:
        result = []
        for i in range(0, len(self.palabra)):
            for keys in self.keyboards:
                if self.palabra[i] in keys:
                    for c in keys[self.palabra[i]]:
                        result.append(self.palabra[:i] + c + self.palabra[i + 1 :])
        return list(set(result))

    def transposition_fuzzer(self) -> List[str]:
        result = []
        for i in range(0, len(self.palabra) - 1):
            if self.palabra[i + 1] != self.palabra[i]:
                result.append(self.palabra[:i] + self.palabra[i + 1] + self.palabra[i] + self.palabra[i + 2 :])
        return result

    def vowel_swap_fuzzer(self) -> List[str]:
        vowels = "aeiou"
        result = []
        for i in range(0, len(self.palabra)):
            for vowel in vowels:
                if self.palabra[i] in vowels:
                    result.append(self.palabra[:i] + vowel + self.palabra[i + 1 :])
        return list(set(result))

    def addition_fuzzer(self) -> List[str]:
        result = []
        for i in range(97, 123):
            result.append(self.palabra + chr(i))
        return result

    def generate(self) -> None:
        if self.config.addition:
            for fuzzed in self.addition_fuzzer():
                self.fuzzed_list_dict.append({"fuzzer": "addition", "fuzzed": fuzzed})
        if self.config.bitsquatting:
            for fuzzed in self.bitsquatting_fuzzer():
                self.fuzzed_list_dict.append({"fuzzer": "bitsquatting", "fuzzed": fuzzed})
        if self.config.homoglyph:
            for fuzzed in self.homoglyph_fuzzer():
                self.fuzzed_list_dict.append({"fuzzer": "homoglyph", "fuzzed": fuzzed})
        if self.config.hyphenation:
            for fuzzed in self.hyphenation_fuzzer():
                self.fuzzed_list_dict.append({"fuzzer": "hyphenation", "fuzzed": fuzzed})
        if self.config.insertion:
            for fuzzed in self.insertion_fuzzer():
                self.fuzzed_list_dict.append({"fuzzer": "insertion", "fuzzed": fuzzed})
        if self.config.omission:
            for fuzzed in self.omission_fuzzer():
                self.fuzzed_list_dict.append({"fuzzer": "omission", "fuzzed": fuzzed})
        if self.config.repetition:
            for fuzzed in self.repetition_fuzzer():
                self.fuzzed_list_dict.append({"fuzzer": "repetition", "fuzzed": fuzzed})
        if self.config.replacement:
            for fuzzed in self.replacement_fuzzer():
                self.fuzzed_list_dict.append({"fuzzer": "replacement", "fuzzed": fuzzed})
        if self.config.transposition:
            for fuzzed in self.transposition_fuzzer():
                self.fuzzed_list_dict.append({"fuzzer": "transposition", "fuzzed": fuzzed})
        if self.config.vowel_swap:
            for fuzzed in self.vowel_swap_fuzzer():
                self.fuzzed_list_dict.append({"fuzzer": "vowel_swap", "fuzzed": fuzzed})
        aux = list({d["fuzzed"]: d for d in self.fuzzed_list_dict}.values())
        self.fuzzed_list_dict = aux
        del aux
        self.fuzzed_as_plain_list = [f["fuzzed"] for f in self.fuzzed_list_dict]

    def get_fuzzed_as_list(self) -> List[str]:
        return self.fuzzed_as_plain_list

    def get_fuzzed_as_set(self) -> Set[str]:
        if not self.fuzzed_as_set:
            self.fuzzed_as_set = self.fuzzed_as_set = set(self.fuzzed_as_plain_list)
        return self.fuzzed_as_set


class FuzzerDominio(Fuzzer):
    def __init__(
        self,
        dominio: str,
        config: FuzzerDominioConfig | None = None,
        append_words: List[str] | None = None,
        tld_dictionary: List[str] | None = None,
    ) -> None:
        parsed_domain = domain_utils.parse_dominio(dominio)
        self.subdominio = parsed_domain.subdominio
        self.dominio = parsed_domain.dominio
        self.tld = parsed_domain.tld
        self.append_words = append_words or []
        self.tld_swap_list = tld_dictionary or []
        super().__init__(self.dominio, config)
        self.config: FuzzerDominioConfig = config or FuzzerDominioConfig()
        self.permutable_fuzzed_list_dict: List[str] = [self.dominio]

    def __filter_domains(self) -> None:
        def idna(domain: str) -> str:
            try:
                return domain.encode("idna").decode()
            except UnicodeError:
                return ""

        idna_domains = list(map(idna, [x["domain-name"] for x in self.fuzzed_list_dict]))
        valid_regex = re.compile("(?=^.{4,253}$)(^((?!-)[a-zA-Z0-9-]{1,63}(?<!-)\.)+[a-zA-Z]{2,63}\.?$)", re.IGNORECASE)
        seen = set()
        filtered = []
        for idx, domain in enumerate(idna_domains):
            if valid_regex.match(domain) and domain not in seen:
                filtered.append(self.fuzzed_list_dict[idx])
                seen.add(domain)
        self.fuzzed_list_dict = filtered

    def tld_fuzzer(self) -> List[str]:
        result = []
        if self.tld in self.tld_swap_list:
            self.tld_swap_list.remove(self.tld)
        for permutable in self.permutable_fuzzed_list_dict:
            for tld in self.tld_swap_list:
                result.append(permutable + "." + tld)
        return list(set(result))

    def subdomain_fuzzer(self) -> List[str]:
        result = []
        for i in range(1, len(self.palabra) - 1):
            if self.palabra[i] not in ["-", "."] and self.palabra[i - 1] not in ["-", "."]:
                result.append(self.palabra[:i] + "." + self.palabra[i:])
        return result

    def append_word_fuzzer(self, separator: str) -> List[str]:
        result = []
        for permutable in self.permutable_fuzzed_list_dict:
            for word in self.append_words:
                result.append(permutable + separator + word)
                result.append(word + separator + permutable)
        return list(set(result))

    def generate(self) -> None:
        if self.config.addition:
            for fuzzed in self.addition_fuzzer():
                self.fuzzed_list_dict.append(
                    {"fuzzer": "addition", "fuzzed": ".".join(filter(None, [self.subdominio, fuzzed, self.tld]))}
                )
                if self.config.addition_permutable and (self.config.append_word or self.config.tld):
                    self.permutable_fuzzed_list_dict.append(fuzzed)
        if self.config.bitsquatting:
            for fuzzed in self.bitsquatting_fuzzer():
                self.fuzzed_list_dict.append(
                    {"fuzzer": "bitsquatting", "fuzzed": ".".join(filter(None, [self.subdominio, fuzzed, self.tld]))}
                )
        if self.config.homoglyph:
            for fuzzed in self.homoglyph_fuzzer():
                self.fuzzed_list_dict.append(
                    {"fuzzer": "homoglyph", "fuzzed": ".".join(filter(None, [self.subdominio, fuzzed, self.tld]))}
                )
        if self.config.hyphenation:
            for fuzzed in self.hyphenation_fuzzer():
                self.fuzzed_list_dict.append(
                    {"fuzzer": "hyphenation", "fuzzed": ".".join(filter(None, [self.subdominio, fuzzed, self.tld]))}
                )
        if self.config.insertion:
            for fuzzed in self.insertion_fuzzer():
                self.fuzzed_list_dict.append(
                    {"fuzzer": "insertion", "fuzzed": ".".join(filter(None, [self.subdominio, fuzzed, self.tld]))}
                )
                if self.config.insertion_permutable and (self.config.append_word or self.config.tld):
                    self.permutable_fuzzed_list_dict.append(fuzzed)
        if self.config.omission:
            for fuzzed in self.omission_fuzzer():
                self.fuzzed_list_dict.append(
                    {"fuzzer": "omission", "fuzzed": ".".join(filter(None, [self.subdominio, fuzzed, self.tld]))}
                )
                if self.config.omission_permutable and (self.config.append_word or self.config.tld):
                    self.permutable_fuzzed_list_dict.append(fuzzed)
        if self.config.repetition:
            for fuzzed in self.repetition_fuzzer():
                self.fuzzed_list_dict.append(
                    {"fuzzer": "repetition", "fuzzed": ".".join(filter(None, [self.subdominio, fuzzed, self.tld]))}
                )
                if self.config.repetition_permutable and (self.config.append_word or self.config.tld):
                    self.permutable_fuzzed_list_dict.append(fuzzed)
        if self.config.replacement:
            for fuzzed in self.replacement_fuzzer():
                self.fuzzed_list_dict.append(
                    {"fuzzer": "replacement", "fuzzed": ".".join(filter(None, [self.subdominio, fuzzed, self.tld]))}
                )
                if self.config.replacement_permutable and (self.config.append_word or self.config.tld):
                    self.permutable_fuzzed_list_dict.append(fuzzed)
        if self.config.transposition:
            for fuzzed in self.transposition_fuzzer():
                self.fuzzed_list_dict.append(
                    {"fuzzer": "transposition", "fuzzed": ".".join(filter(None, [self.subdominio, fuzzed, self.tld]))}
                )
                if self.config.transposition_permutable and (self.config.append_word or self.config.tld):
                    self.permutable_fuzzed_list_dict.append(fuzzed)
        if self.config.vowel_swap:
            for fuzzed in self.vowel_swap_fuzzer():
                self.fuzzed_list_dict.append(
                    {"fuzzer": "vowel_swap", "fuzzed": ".".join(filter(None, [self.subdominio, fuzzed, self.tld]))}
                )
                if self.config.vowel_swap_permutable and (self.config.append_word or self.config.tld):
                    self.permutable_fuzzed_list_dict.append(fuzzed)
        if self.config.subdomain:
            for fuzzed in self.subdomain_fuzzer():
                self.fuzzed_list_dict.append({"fuzzer": "subdomain", "fuzzed": ".".join(filter(None, [fuzzed, self.tld]))})
        if self.config.append_word:
            aux = []
            for fuzzed in self.append_word_fuzzer(separator="-"):
                self.fuzzed_list_dict.append(
                    {"fuzzer": "append_word", "fuzzed": ".".join(filter(None, [self.subdominio, fuzzed, self.tld]))}
                )
                self.fuzzed_list_dict.append({"fuzzer": "append_word", "fuzzed": ".".join(filter(None, [fuzzed, self.tld]))})
                if self.config.tld:
                    aux.append(fuzzed)
            for fuzzed in self.append_word_fuzzer(separator="."):
                self.fuzzed_list_dict.append({"fuzzer": "append_word", "fuzzed": ".".join(filter(None, [fuzzed, self.tld]))})
                if self.config.tld:
                    aux.append(fuzzed)
            for fuzzed in self.append_word_fuzzer(separator=""):
                self.fuzzed_list_dict.append(
                    {"fuzzer": "append_word", "fuzzed": ".".join(filter(None, [self.subdominio, fuzzed, self.tld]))}
                )
                self.fuzzed_list_dict.append({"fuzzer": "append_word", "fuzzed": ".".join(filter(None, [fuzzed, self.tld]))})
                if self.config.tld:
                    aux.append(fuzzed)
            self.permutable_fuzzed_list_dict += aux
        if self.config.tld:
            for fuzzed in self.tld_fuzzer():
                self.fuzzed_list_dict.append({"fuzzer": "tld", "fuzzed": ".".join(filter(None, [self.subdominio, fuzzed]))})
                self.fuzzed_list_dict.append({"fuzzer": "tld", "fuzzed": ".".join(filter(None, [fuzzed]))})
        del self.permutable_fuzzed_list_dict
        aux = list({d["fuzzed"]: d for d in self.fuzzed_list_dict}.values())  # type: ignore  # Borro repetidos
        self.fuzzed_list_dict = aux  # type: ignore
        del aux
        self.fuzzed_as_plain_list = [f["fuzzed"] for f in self.fuzzed_list_dict]
