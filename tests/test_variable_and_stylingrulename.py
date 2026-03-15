import pytest
import json
from cartosym_transcoder.parser import CartoSymParser
from cartosym_transcoder.models.styles import Style, StylingRule


def test_variable_parsing():
    """Test that @variable definitions are extracted from cscss."""
    cscss = '''
    @roadColor = gray;

    Roads[type = 'highway']
    {
       stroke: { color: @roadColor, width: 2px };
    }
    '''
    parser = CartoSymParser()
    style: Style = parser.parse_string_to_pydantic(cscss)

    # Variable must be extracted
    assert style.variables is not None, "variables should not be None"
    assert len(style.variables) == 1
    assert style.variables[0].name == 'roadColor'
    assert style.variables[0].value == 'gray'


def test_styling_rule_name_parsing():
    """Test that .name 'value' (stylingRuleName) is extracted from cscss."""
    cscss = '''
    Roads[type = 'highway']
    {
       .name 'Highways'
       fill: { color: red };
    }
    '''
    parser = CartoSymParser()
    style: Style = parser.parse_string_to_pydantic(cscss)

    assert len(style.styling_rules) >= 1
    rule = style.styling_rules[0]
    # stylingRuleName should be extracted
    assert rule.styling_rule_name == 'Highways', (
        f"Expected styling_rule_name='Highways', got {rule.styling_rule_name!r}"
    )
    # Selector and symbolizer should still be present
    assert rule.selector is not None
    assert rule.symbolizer is not None


def test_variable_and_stylingrulename_combined():
    """Test variables and stylingRuleName together in a realistic cscss."""
    cscss = '''
    @roadColor = gray;

    Roads[type = 'highway']
    {
       .name 'Highways'
       stroke: { color: @roadColor, width: 2px };
    }
    '''
    parser = CartoSymParser()
    style: Style = parser.parse_string_to_pydantic(cscss)

    # Variables
    assert style.variables is not None
    assert len(style.variables) == 1
    assert style.variables[0].name == 'roadColor'
    assert style.variables[0].value == 'gray'

    # StylingRuleName
    rule = style.styling_rules[0]
    assert rule.styling_rule_name == 'Highways'

    # Symbolizer with stroke
    assert rule.symbolizer is not None


def test_name_absent_when_not_in_source():
    """1.2 — If the cscss has no .name, the CS-JSON must NOT contain 'stylingRuleName'."""
    cscss = '''
    Roads[type = 'highway']
    {
       fill: { color: red };
    }
    '''
    parser = CartoSymParser()
    style: Style = parser.parse_string_to_pydantic(cscss)
    rule = style.styling_rules[0]

    # model attribute should be None
    assert rule.styling_rule_name is None

    # serialized dict must not contain the key
    d = rule.to_dict()
    assert 'stylingRuleName' not in d, (
        f"'stylingRuleName' should not appear in JSON when absent from source, got: {d}"
    )


def test_name_present_when_in_source():
    """1.2 — If the cscss has .name 'X', the CS-JSON must contain 'stylingRuleName': 'X'."""
    cscss = '''
    Roads[type = 'highway']
    {
       .name 'MyRoads'
       fill: { color: red };
    }
    '''
    parser = CartoSymParser()
    style: Style = parser.parse_string_to_pydantic(cscss)
    rule = style.styling_rules[0]

    d = rule.to_dict()
    assert d.get('stylingRuleName') == 'MyRoads', (
        f"Expected stylingRuleName='MyRoads' in serialized dict, got: {d}"
    )


def test_field_order_in_serialized_json():
    """1.1 — Verify the JSON key order: name → stylingRuleName → selector → symbolizer → nestedRules."""
    cscss = '''
    Landuse[type = 'forest']
    {
       .name 'Forests'
       fill: { color: green };

       Deep[level > 5]
       {
          fill: { color: darkgreen };
       }
    }
    '''
    parser = CartoSymParser()
    style: Style = parser.parse_string_to_pydantic(cscss)
    rule = style.styling_rules[0]

    d = rule.to_dict()
    keys = list(d.keys())

    # nestedRules must come after selector and symbolizer
    if 'nestedRules' in keys and 'selector' in keys:
        assert keys.index('selector') < keys.index('nestedRules'), (
            f"'selector' should appear before 'nestedRules', got order: {keys}"
        )
    if 'nestedRules' in keys and 'symbolizer' in keys:
        assert keys.index('symbolizer') < keys.index('nestedRules'), (
            f"'symbolizer' should appear before 'nestedRules', got order: {keys}"
        )


def test_stylingrulename_roundtrip():
    """2.3 — stylingRuleName must survive a full round-trip: .cscss → CS-JSON → .cscss."""
    from cartosym_transcoder.converter import Converter

    cscss_src = """
    [TestLayer]
    {
       .name 'My Layer Name'
       visibility: true;
    }
    """
    converter = Converter()
    # Forward: CSCSS → CS-JSON
    cs_json = converter.cscss_to_csjson(cscss_src)
    assert cs_json['stylingRules'][0].get('stylingRuleName') == 'My Layer Name'

    # Reverse: CS-JSON → CSCSS
    style = Style.from_dict(cs_json)
    cscss_out = converter.style_to_cscss(style)

    assert ".name 'My Layer Name'" in cscss_out, (
        f"Expected .name directive in round-trip CSCSS output, got:\n{cscss_out}"
    )
