import xml.etree.ElementTree as ET
import sys

def create_qgis_style_file(filename):
    # Create the root element with the DOCTYPE declaration
    qgis = ET.Element("qgis")

    # Create the renderer-v2 element
    renderer_v2 = ET.SubElement(qgis, "renderer-v2", type="RuleRenderer")

    # Create the rules element
    rules = ET.SubElement(renderer_v2, "rules", key="renderer_rules")

    # Create a rule element
    rule = ET.SubElement(rules, "rule", key="renderer_rule_0", symbol="0", label="Rule 1")

    # Create the symbols element
    symbols = ET.SubElement(renderer_v2, "symbols")

    # Create a symbol element
    symbol = ET.SubElement(symbols, "symbol", type="fill", name="0")

    # Add a layer to the symbol
    layer = ET.SubElement(symbol, "layer", {"class": "SimpleFill"})

    # Add properties to the layer
    ET.SubElement(layer, "prop", k="color", v="255,0,0,255")  # Red fill color
    ET.SubElement(layer, "prop", k="offset_map_unit_scale", v="3x:0,0,0,0,0,0")
    ET.SubElement(layer, "prop", k="offset_unit", v="Pixel")
    ET.SubElement(layer, "prop", k="outline_style", v="solid")
    ET.SubElement(layer, "prop", k="outline_width", v="0.26")  # Outline width
    ET.SubElement(layer, "prop", k="outline_width_map_unit_scale", v="3x:0,0,0,0,0,0")
    ET.SubElement(layer, "prop", k="outline_width_unit", v="Pixel")
    ET.SubElement(layer, "prop", k="outline_color", v="0,0,0,255")  # Black outline color

    # Create an XML tree and write it to a file with the DOCTYPE declaration
    tree = ET.ElementTree(qgis)
    with open(filename, "wb") as f:
        f.write(b"<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>\n")
        tree.write(f, encoding="UTF-8", xml_declaration=False)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python qml_parser.py <output_filename>")
        sys.exit(1)

    output_filename = sys.argv[1]

    # Create the QGIS style file
    create_qgis_style_file(output_filename)

    print(f"QGIS style file '{output_filename}' created successfully.")
    