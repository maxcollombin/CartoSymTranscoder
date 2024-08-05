import sys
from parser import parse_input
from converter import convert_to_sld, convert_to_qml

def main():
    if len(sys.argv) != 4:
        print("Usage: python main.py path_to_input_file path_to_output_file format(sld|qml)")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    format_type = sys.argv[3].lower()
    
    data = parse_input(input_file)
    
    if format_type == 'sld':
        convert_to_sld(data, output_file)
    elif format_type == 'qml':
        convert_to_qml(data, output_file)
    else:
        print("Unsupported format. Use 'sld' or 'qml'.")
        sys.exit(1)

if __name__ == "__main__":
    main()