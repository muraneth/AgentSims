import json
import argparse

def is_interactive(obj):
    if 'properties' in obj:
        for prop in obj['properties']:
            if (prop['name'] == "Interactive" or prop['name'] == "interactive") and prop['type'] == "bool" and prop['value'] is True:
                return True
    return False

def extract_interactive_objects(tmj_data):
    interactive_objects = []
    for layer in tmj_data['layers']:
        if layer['type'] == 'objectgroup':
            for obj in layer['objects']:
                if ('type' in obj and (obj["type"] == "Object" or obj["type"] == "object")) or is_interactive(obj):
                    interactive_objects.append(obj)
                        

    return interactive_objects

def calculate_width_height(polygon):
    min_x = min([coord['x'] for coord in polygon])
    max_x = max([coord['x'] for coord in polygon])
    min_y = min([coord['y'] for coord in polygon])
    max_y = max([coord['y'] for coord in polygon])

    return max_x - min_x, max_y - min_y

def convert_to_sol(interactive_objects, output_file, tile_width, tile_height):
    with open(output_file, 'w') as f:
        f.write('pragma solidity ^0.5.0;\n\n')
        f.write('library InteractiveObjects {\n')
        f.write('    struct InteractiveObject {\n')
        f.write('        string name;\n')
        f.write('        uint x;\n')
        f.write('        uint y;\n')
        f.write('        uint width;\n')
        f.write('        uint height;\n')
        f.write('    }\n\n')

        f.write('    function getAllInteractiveObjects() public pure returns (InteractiveObject[] memory) {\n')
        f.write('        InteractiveObject[] memory allInteractiveObjects = new InteractiveObject[](' + str(len(interactive_objects)) + ');\n')

        for index, obj in enumerate(interactive_objects):
            x, y = obj['x'] // tile_width, obj['y'] // tile_height
            width, height = calculate_width_height(obj['polygon'])
            width, height = width // tile_width, height // tile_height
            f.write(f"        allInteractiveObjects[{index}] = InteractiveObject('{obj['name']}', {x}, {y}, {width}, {height});\n")

        f.write('        return allInteractiveObjects;\n')
        f.write('    }\n')

        f.write('}\n')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--file', help='Input TMJ JSON file path', required=True)
    parser.add_argument('-o', '--output', help='Output SOL file path', required=True)
    args = parser.parse_args()

    with open(args.file, 'r') as f:
        json_data = json.load(f)

    tile_width = json_data['tilewidth']
    tile_height = json_data['tileheight']

    interactive_objects = extract_interactive_objects(json_data)
    convert_to_sol(interactive_objects, args.output, tile_width, tile_height)
