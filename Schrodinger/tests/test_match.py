import re
from pathlib import Path

from schrodinger.core import parse_extension_argument, Schrodinger


def test_simple_language_defaults_to_extension():
    lang, patterns = parse_extension_argument("en")

    assert lang == "en"
    assert len(patterns) == 1
    assert isinstance(patterns[0], re.Pattern)
    assert patterns[0].pattern == r"\.en$"


def test_single_custom_regex():
    lang, patterns = parse_extension_argument("en:^en_")

    assert lang == "en"
    assert len(patterns) == 1
    assert patterns[0].pattern == "^en_"


def test_multiple_regexes():
    lang, patterns = parse_extension_argument(r"hu:\.hu$;^hu_")

    assert lang == "hu"
    assert len(patterns) == 2
    assert patterns[0].pattern == r"\.hu$"
    assert patterns[1].pattern == "^hu_"


def test_empty_regex_falls_back():
    lang, patterns = parse_extension_argument("de:")

    assert lang == "de"
    assert len(patterns) == 1
    assert patterns[0].pattern == r"\.de$"


def test_language_is_lowercased_and_whitespace_trimmed():
    lang, patterns = parse_extension_argument("  En  :   ^EN_  ;  ")

    assert lang == "en"
    assert len(patterns) == 1
    # the regex body is taken as-is, only spaces around it are stripped
    assert patterns[0].pattern == "^EN_"


# ----------------------------
# Schrodinger.classify_file
# ----------------------------

def _make_schrodinger(tmp_path, extensions):
    """Small helper to build Schrodinger without caring about filesystem."""
    base_path = tmp_path / "project"
    base_path.mkdir()
    # we only care about lang_patterns / classify_file here
    return Schrodinger(str(base_path), extensions)


def test_classify_file_matches_single_language_by_extension(tmp_path):
    sch = _make_schrodinger(tmp_path, ["en", "hu"])

    assert sch.classify_file("readme.en") == ["en"]
    assert sch.classify_file("notes.hu") == ["hu"]


def test_classify_file_default_pattern_is_case_insensitive(tmp_path):
    sch = _make_schrodinger(tmp_path, ["en", "hu"])

    # .EN and .Hu should still match because re.IGNORECASE is used
    assert sch.classify_file("README.EN") == ["en"]
    assert sch.classify_file("notes.Hu") == ["hu"]


def test_classify_file_uses_all_custom_patterns_for_language(tmp_path):
    # en: match either ".en" or "^en_"
    sch = _make_schrodinger(tmp_path, [r"en:\.en$;^en_", "hu"])

    assert sch.classify_file("file.en") == ["en"]
    assert sch.classify_file("en_header.txt") == ["en"]


def test_classify_file_unclassified_file_returns_empty_list(tmp_path):
    sch = _make_schrodinger(tmp_path, ["en", "hu"])

    # no .en or .hu, no custom patterns → unclassified
    matches = sch.classify_file("common.txt")

    # empty list means: copy to ALL languages later in run()
    assert matches == []


def test_classify_file_ambiguous_when_two_languages_match(tmp_path):
    # both languages share the same broad pattern, so file should match both
    sch = _make_schrodinger(tmp_path, ["en:foo", "hu:foo"])

    matches = sch.classify_file("myfoo.txt")

    assert sorted(matches) == ["en", "hu"]


def test_classify_file_no_languages_defined_returns_empty(tmp_path):
    # edge case: Schrodinger constructed with no extension definitions
    sch = _make_schrodinger(tmp_path, [])

    assert sch.classify_file("anything.en") == []
