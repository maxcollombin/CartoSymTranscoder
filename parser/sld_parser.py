import json
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import SubElement
import sys

# Usage:
# python script_name.py input_file.json output_file.sld

def json_to_sld(json_data):
    # Create the root element of the SLD file
    sld = ET.Element('StyledLayerDescriptor', version='1.0.0', 
                     xmlns='http://www.opengis.net/sld', 
                     attrib={
                         'xsi:schemaLocation': 'http://www.opengis.net/sld StyledLayerDescriptor.xsd',
                         'xmlns:ogc': 'http://www.opengis.net/ogc',
                         'xmlns:xlink': 'http://www.w3.org/1999/xlink',
                         'xmlns:xsi': 'http://www.w3.org/2001/XMLSchema-instance',
                         'xmlns:se': 'http://www.opengis.net/se'
                     })
    named_layer = SubElement(sld, 'NamedLayer')
    name = SubElement(named_layer, 'Name')
    name.text = 'Landuse'
    user_style = SubElement(named_layer, 'UserStyle')
    style_name = SubElement(user_style, 'Name')
    style_name.text = 'Landuse'
    title = SubElement(user_style, 'Title')
    title.text = 'Landuse'
    feature_type_style = SubElement(user_style, 'FeatureTypeStyle')

    # Convert the JSON array structure to SLD rules
    for rule_data in json_data:
        if isinstance(rule_data[0], str) and rule_data[0].startswith('.'):
            continue  # Skip title, abstract, and description
        rule = SubElement(feature_type_style, 'Rule')
        rule_name = SubElement(rule, 'Name')
        rule_name.text = 'Landuse'
        
        filter_element = SubElement(rule, 'Filter', xmlns='http://www.opengis.net/ogc')
        
        property_is_greater_than_or_equal_to = SubElement(filter_element, 'PropertyIsGreaterThanOrEqualTo')
        property_name = SubElement(property_is_greater_than_or_equal_to, 'PropertyName')
        property_name.text = 'date'
        literal = SubElement(property_is_greater_than_or_equal_to, 'Literal')
        literal.text = '2020-01-01'
        
        min_scale_denominator = SubElement(rule, 'MinScaleDenominator')
        min_scale_denominator.text = '1'
        
        max_scale_denominator = SubElement(rule, 'MaxScaleDenominator')
        max_scale_denominator.text = '200000'
        
        polygon_symbolizer = SubElement(rule, 'PolygonSymbolizer')
        fill = SubElement(polygon_symbolizer, 'Fill')
        # Removed the fill-opacity parameter as it has no equivalent in SLD/SE

    return sld

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script_name.py <input_file.json> <output_file.sld>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    # Load the JSON data
    with open(input_file, 'r', encoding='utf-8') as f:
        json_data = json.load(f)
    
    # Convert JSON to SLD
    sld_tree = json_to_sld(json_data)
    
    # Save the SLD to a file
    tree = ET.ElementTree(sld_tree)
    tree.write(output_file, encoding='utf-8', xml_declaration=True)

    print(f"SLD file '{output_file}' created successfully.")