from lxml import etree

def parse_sld(sld_file):
    try:
        tree = etree.parse(sld_file)
        root = tree.getroot()
        namespaces = {'sld': 'http://www.opengis.net/sld'}
        print("SLD file parsed successfully.")
        return root, namespaces
    except Exception as e:
        print(f"Error parsing SLD file: {e}")
        return None, None

def extract_styling_rules(root, namespaces):
    rules = []
    for rule in root.findall('.//sld:Rule', namespaces):
        rule_name = rule.find('sld:Name', namespaces).text
        symbolizers = rule.findall('.//sld:*Symbolizer', namespaces)
        rules.append((rule_name, symbolizers))
    print(f"Extracted {len(rules)} rules from SLD file.")
    return rules

def map_sld_to_cartosymcss(rules, namespaces):
    cartosymcss_rules = []
    for rule_name, symbolizers in rules:
        cartosymcss_rule = f".{rule_name} {{\n"
        for symbolizer in symbolizers:
            symbolizer_type = symbolizer.tag.split('}')[-1]
            if symbolizer_type == 'LineSymbolizer':
                stroke = symbolizer.find('.//sld:Stroke/sld:CssParameter[@name="stroke"]', namespaces).text
                width = symbolizer.find('.//sld:Stroke/sld:CssParameter[@name="stroke-width"]', namespaces).text
                cartosymcss_rule += f"  stroke: {stroke};\n"
                cartosymcss_rule += f"  stroke-width: {width};\n"
            elif symbolizer_type == 'PolygonSymbolizer':
                fill = symbolizer.find('.//sld:Fill/sld:CssParameter[@name="fill"]', namespaces).text
                cartosymcss_rule += f"  fill: {fill};\n"
            # Add more symbolizer types as needed
        cartosymcss_rule += "}\n"
        cartosymcss_rules.append(cartosymcss_rule)
    print(f"Converted {len(cartosymcss_rules)} rules to CartoSymCSS.")
    return cartosymcss_rules

def generate_cartosymcss(cartosymcss_rules):
    return "\n".join(cartosymcss_rules)

def main(sld_file, output_file):
    root, namespaces = parse_sld(sld_file)
    if root is None:
        print("Failed to parse SLD file.")
        return

    rules = extract_styling_rules(root, namespaces)
    if not rules:
        print("No styling rules found in SLD file.")
        return

    cartosymcss_rules = map_sld_to_cartosymcss(rules, namespaces)
    if not cartosymcss_rules:
        print("No CartoSymCSS rules generated.")
        return

    cartosymcss_code = generate_cartosymcss(cartosymcss_rules)
    
    with open(output_file, 'w') as f:
        f.write(cartosymcss_code)
    
    print(f"CartoSymCSS code written to {output_file}")

if __name__ == '__main__':
    import sys
    if len(sys.argv) != 3:
        print("Usage: python sld_to_cartosymcss.py <input_sld_file> <output_cartosymcss_file>")
    else:
        main(sys.argv[1], sys.argv[2])