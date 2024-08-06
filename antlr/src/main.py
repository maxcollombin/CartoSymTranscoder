import os
import sys
from parser import parse_input
from converter import convert_to_sld, convert_to_qml

def main():
    if len(sys.argv) != 3:
        print("Usage: python main.py path_to_input_file path_to_output_file")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    
    # Extract the file extension and determine the format type
    _, file_extension = os.path.splitext(output_file)
    format_type = file_extension.lower().strip('.')

    if format_type not in ['sld', 'qml']:
        print("Error: Unsupported file format. Please use 'sld' or 'qml'.")
        sys.exit(1)
    
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
