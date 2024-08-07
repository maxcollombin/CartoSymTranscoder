import xml.etree.ElementTree as ET
import json
import os

def parse_xsd(xsd_file):
    tree = ET.parse(xsd_file)
    root = tree.getroot()
    return root

def extract_schema_info(element):
    schema_info = {}
    for child in element:
        tag = child.tag.split('}')[-1]  # Remove namespace
        if tag == 'element':
            name = child.attrib.get('name')
            if name is None:
                name = child.attrib.get('ref')
            type_ = child.attrib.get('type')
            schema_info[name] = {'type': type_}
            # Recursively extract child elements
            if list(child):
                schema_info[name]['children'] = extract_schema_info(child)
        elif tag == 'complexType':
            complex_type_name = child.attrib.get('name')
            schema_info[complex_type_name] = {'type': 'complexType', 'children': extract_schema_info(child)}
        elif tag == 'sequence':
            sequence_info = extract_schema_info(child)
            schema_info['sequence'] = sequence_info
        elif tag == 'attribute':
            attr_name = child.attrib.get('name')
            attr_type = child.attrib.get('type')
            if 'attributes' not in schema_info:
                schema_info['attributes'] = {}
            schema_info['attributes'][attr_name] = attr_type
    return schema_info

def convert_xsd_to_json(xsd_file, json_file):
    root = parse_xsd(xsd_file)
    schema_info = extract_schema_info(root)
    
    # Ensure the output directory exists
    os.makedirs(os.path.dirname(json_file), exist_ok=True)
    
    with open(json_file, 'w') as f:
        json.dump(schema_info, f, indent=4)

# Example usage
if __name__ == "__main__":
    # Get the directory of the current script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Construct the full path to the XSD file
    xsd_file = os.path.join(script_dir, 'FeatureStyle.xsd')
    json_file = os.path.join(script_dir, 'output', 'FeatureStyle.json')  # Save the JSON file in the output directory
    
    convert_xsd_to_json(xsd_file, json_file)