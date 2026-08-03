import ast
import subprocess
import sys
from pathlib import Path

import pytest

import adstxt.parser as parser


def test_inventory_partner_domain_is_constructible_and_exposes_domain():
    inventory_partner_domain = getattr(parser, "InventoryPartnerDomain", None)

    assert inventory_partner_domain is not None, (
        "adstxt.parser must expose InventoryPartnerDomain"
    )
    declaration = inventory_partner_domain(domain="partner.com")
    assert declaration.domain == "partner.com"


def test_parse_line_returns_inventory_partner_domain_for_standalone_declaration():
    result = parser.parse_line("inventorypartnerdomain=partner.com")

    expected_type = getattr(parser, "InventoryPartnerDomain", None)
    assert expected_type is not None, (
        "adstxt.parser must expose InventoryPartnerDomain"
    )
    assert type(result) is expected_type
    assert result.domain == "partner.com"


def test_standalone_inventory_partner_domain_is_not_a_record():
    result = parser.parse_line("inventorypartnerdomain=partner.com")

    assert type(result) is not parser.Record


def test_inventory_partner_domain_key_is_case_insensitive_and_value_is_lowercased():
    result = parser.parse_line("INVENTORYPARTNERDOMAIN=Partner.com")

    expected_type = getattr(parser, "InventoryPartnerDomain", None)
    assert expected_type is not None, (
        "adstxt.parser must expose InventoryPartnerDomain"
    )
    assert type(result) is expected_type
    assert result.domain == "partner.com"


def test_record_inventory_partner_domain_defaults_to_none():
    assert "inventory_partner_domain" in getattr(parser.Record, "__annotations__", {})

    result = parser.parse_line("example.com, 1234, DIRECT, abc123")

    assert type(result) is parser.Record
    assert result.inventory_partner_domain is None


def test_five_field_record_parses_cert_and_inventory_partner_domain():
    result = parser.parse_line(
        "example.com, 1234, DIRECT, abc123, inventorypartnerdomain=partner.com"
    )

    assert type(result) is parser.Record
    assert result.domain == "example.com"
    assert result.publisher_id == "1234"
    assert result.relationship == "DIRECT"
    assert result.cert_id == "abc123"
    assert result.inventory_partner_domain == "partner.com"


def test_fourth_field_inventory_partner_domain_is_parsed_without_cert():
    result = parser.parse_line(
        "example.com, 1234, DIRECT, inventorypartnerdomain=partner.com"
    )

    assert type(result) is parser.Record
    assert result.cert_id is None
    assert result.inventory_partner_domain == "partner.com"


def test_unrecognised_standalone_variable_declaration_is_dropped():
    assert parser.parse_line("someothervar=value") is None


@pytest.mark.parametrize(
    "line",
    [
        "# a comment",
        "   ",
        "example.com, 1234, FRIEND",
        "",
        ",",
        "a,b",
        "a,b,c,d,e,f",
        ",,,",
    ],
)
def test_parse_line_returns_none_for_ignored_and_malformed_lines(line):
    assert parser.parse_line(line) is None


def _run_cli(stdin: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, "-m", "adstxt.cli"],
        input=stdin,
        text=True,
        capture_output=True,
        check=False,
    )


def test_cli_preserves_three_field_output_for_record_without_ipd():
    completed = _run_cli("example.com, 1234, DIRECT\n")

    assert completed.returncode == 0, completed.stderr
    assert completed.stdout == "example.com|1234|DIRECT"


def test_cli_emits_inventory_partner_domain_for_record():
    completed = _run_cli(
        "example.com, 1234, DIRECT, abc123, "
        "inventorypartnerdomain=partner.com\n"
    )

    assert completed.returncode == 0, completed.stderr
    assert completed.stdout == (
        "example.com|1234|DIRECT|inventorypartnerdomain=partner.com"
    )


def test_cli_emits_standalone_inventory_partner_domain():
    completed = _run_cli("inventorypartnerdomain=partner.com\n")

    assert completed.returncode == 0, completed.stderr
    assert completed.stdout == "inventorypartnerdomain=partner.com"


def test_cli_imports_and_branches_on_inventory_partner_domain():
    cli_path = Path(__file__).parents[1] / "adstxt" / "cli.py"
    tree = ast.parse(cli_path.read_text(encoding="utf-8"))

    imports_from_parser = {
        alias.name
        for node in ast.walk(tree)
        if isinstance(node, ast.ImportFrom) and node.module == "adstxt.parser"
        for alias in node.names
    }
    branch_names = {
        node.id
        for conditional in ast.walk(tree)
        if isinstance(conditional, (ast.If, ast.Match))
        for node in ast.walk(conditional.test if isinstance(conditional, ast.If) else conditional)
        if isinstance(node, ast.Name)
    }

    assert "InventoryPartnerDomain" in imports_from_parser
    assert "InventoryPartnerDomain" in branch_names
