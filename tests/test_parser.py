from adstxt.parser import Record, parse_line


def test_parses_a_direct_line():
    assert parse_line("example.com, 1234, DIRECT, abc123") == Record(
        "example.com", "1234", "DIRECT", "abc123"
    )


def test_lowercases_the_domain():
    assert parse_line("EXAMPLE.com, 1234, DIRECT").domain == "example.com"


def test_returns_none_for_comments_and_blanks():
    assert parse_line("# a comment") is None
    assert parse_line("   ") is None


def test_returns_none_for_an_unknown_relationship():
    assert parse_line("example.com, 1234, FRIEND") is None


def test_never_raises_on_malformed_input():
    for bad in ["", ",", "a,b", "a,b,c,d,e,f", ",,,"]:
        parse_line(bad)
