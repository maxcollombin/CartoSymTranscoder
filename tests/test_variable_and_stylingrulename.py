import pytest
from cartosym_transcoder.parser import CartoSymParser
from cartosym_transcoder.models.styles import Style


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
