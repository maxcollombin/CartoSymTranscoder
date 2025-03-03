import xml.etree.ElementTree as ET
from xml.dom import minidom

def sanitize_text(text):
    if text.startswith("'") and text.endswith("'"):
        return text[1:-1]
    elif text.startswith('"') and text.endswith('"'):
        return text[1:-1]
    return text

def convert_to_sld(data, output_file):
    title = sanitize_text(data.get('title', ''))
    abstract = sanitize_text(data.get('abstract', ''))
    date = sanitize_text(data.get('date', ''))

    sld = ET.Element('StyledLayerDescriptor', {
        'version': '1.0.0',
        'xsi:schemaLocation': 'http://www.opengis.net/sld StyledLayerDescriptor.xsd',
        'xmlns': 'http://www.opengis.net/sld',
        'xmlns:ogc': 'http://www.opengis.net/ogc',
        'xmlns:xlink': 'http://www.w3.org/1999/xlink',
        'xmlns:xsi': 'http://www.w3.org/2001/XMLSchema-instance',
        'xmlns:se': 'http://www.opengis.net/se'
    })

    named_layer = ET.SubElement(sld, 'NamedLayer')
    
    # Get the NamedLayer from the selector identifier
    layer_name = data['rules'][0]['selectors'][0] if data['rules'] and data['rules'][0]['selectors'] else 'Default'
    ET.SubElement(named_layer, 'Name').text = layer_name

    user_style = ET.SubElement(named_layer, 'UserStyle')
    ET.SubElement(user_style, 'Name').text = title
    ET.SubElement(user_style, 'Title').text = title
    ET.SubElement(user_style, 'Abstract').text = abstract

    # Determine the type of style to create based on the data_layer_type
    if data['data_layer_type'] == 'vector':
        style_element = ET.SubElement(user_style, 'FeatureTypeStyle')
    elif data['data_layer_type'] == 'coverage':
        style_element = ET.SubElement(user_style, 'CoverageStyle')

    for rule in data['rules']:
        rule_element = ET.SubElement(style_element, 'Rule')

        # Get the Rule Name from the selector identifier
        selector_name = rule['selectors'][0] if rule['selectors'] else 'Default'
        ET.SubElement(rule_element, 'Name').text = selector_name

        filter_element = ET.SubElement(rule_element, 'ogc:Filter')
        property_is_greater_than = ET.SubElement(filter_element, 'ogc:PropertyIsGreaterThan')
        property_name = ET.SubElement(property_is_greater_than, 'ogc:PropertyName')
        property_name.text = 'date'
        literal = ET.SubElement(property_is_greater_than, 'ogc:Literal')
        literal.text = date

        if 'min_scale_denominator' in data:
            ET.SubElement(rule_element, 'MinScaleDenominator').text = data['min_scale_denominator']
        if 'max_scale_denominator' in data:
            ET.SubElement(rule_element, 'MaxScaleDenominator').text = data['max_scale_denominator']

    xml_str = ET.tostring(sld, encoding='utf-8')
    parsed_xml = minidom.parseString(xml_str)
    pretty_xml_str = parsed_xml.toprettyxml(indent="  ")

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(pretty_xml_str)

def convert_to_qml(data, output_file):
    pass