import argparse
import json
import os

def parse_args():
    parser = argparse.ArgumentParser(description="Convert JSON to Solidity Library")
    parser.add_argument("-f", "--file", required=True, help="Path to the JSON file")
    parser.add_argument("-o", "--output", required=True, help="Path to the output Solidity file")
    return parser.parse_args()

def json_to_sol(input_file, output_file):
    output_dir = os.path.dirname(output_file)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    with open(input_file, "r") as f:
        data = json.load(f)

    with open(output_file, "w") as f:
        f.write("pragma solidity ^0.8.0;\n\n")
        f.write("library ObjectTypes {\n\n")

        f.write("    struct EquipmentProperties {\n")
        f.write("        string name;\n")
        f.write("        string description;\n")
        f.write("        string[] operations;\n")
        f.write("    }\n\n")

        f.write("    function getAllObjectTypes() public pure returns (EquipmentProperties[] memory) {\n")
        f.write("        EquipmentProperties[] memory objectTypes = new EquipmentProperties[](")
        f.write(f"{len(data)});\n\n")

        for index, item in enumerate(data):
            properties = item["equipment_properties"]
            f.write(f"        objectTypes[{index}] = EquipmentProperties(")
            f.write(f'"{properties["name"]}", ')
            f.write(f'"{properties["description"]}", ')
            f.write("new string[](")
            f.write(f"{len(properties['operations'])})")
            f.write(");\n")
            for i, op in enumerate(properties["operations"]):
                f.write(f"        objectTypes[{index}].operations[{i}] = \"{op}\";\n")
            f.write("\n")

        f.write("        return objectTypes;\n")
        f.write("    }\n")
        f.write("}\n")

def main():
    args = parse_args()
    json_to_sol(args.file, args.output)

if __name__ == "__main__":
    main()
