from xml.etree.ElementTree import Element, SubElement, tostring, ElementTree

def create_sld_file(filename):
    # Create the root element
    sld = Element('StyledLayerDescriptor', 
                  {'version': '1.0.0', 
                   'xmlns': 'http://www.opengis.net/sld', 
                   'xmlns:ogc': 'http://www.opengis.net/ogc', 
                   'xmlns:xlink': 'http://www.w3.org/1999/xlink', 
                   'xmlns:xsi': 'http://www.w3.org/2001/XMLSchema-instance', 
                   'xsi:schemaLocation': 'http://www.opengis.net/sld StyledLayerDescriptor.xsd'})

    named_layer = SubElement(sld, 'NamedLayer')
    name = SubElement(named_layer, 'Name')
    name.text = 'Example Layer'

    user_style = SubElement(named_layer, 'UserStyle')
    title = SubElement(user_style, 'Title')
    title.text = 'Example Style'
    abstract = SubElement(user_style, 'Abstract')
    abstract.text = 'A simple style for polygons'

    feature_type_style = SubElement(user_style, 'FeatureTypeStyle')

    rule = SubElement(feature_type_style, 'Rule')
    rule_name = SubElement(rule, 'Name')
    rule_name.text = 'Polygon Rule'
    rule_title = SubElement(rule, 'Title')
    rule_title.text = 'Polygon Rule Title'

    polygon_symbolizer = SubElement(rule, 'PolygonSymbolizer')

    fill = SubElement(polygon_symbolizer, 'Fill')
    css_param_fill = SubElement(fill, 'CssParameter', {'name': 'fill'})
    css_param_fill.text = '#FF0000'  # Red fill color

    stroke = SubElement(polygon_symbolizer, 'Stroke')
    css_param_stroke_color = SubElement(stroke, 'CssParameter', {'name': 'stroke'})
    css_param_stroke_color.text = '#000000'  # Black outline color
    css_param_stroke_width = SubElement(stroke, 'CssParameter', {'name': 'stroke-width'})
    css_param_stroke_width.text = '26'  # Outline width

    # Create the tree and write it to a file
    tree = ElementTree(sld)
    tree.write(filename, encoding='UTF-8', xml_declaration=True)

# Specify the output filename
output_filename = 'example_style.sld'

# Create the SLD file
create_sld_file(output_filename)

print(f'SLD file \'{output_filename}\' created successfully.')
