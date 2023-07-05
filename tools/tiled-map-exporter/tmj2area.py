import argparse
import json
import os

def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--file', required=True, help='Path to the input JSON file')
    parser.add_argument('-o', '--output', required=True, help='Path to the output Solidity file')
    return parser.parse_args()

def extract_area_objects(json_data):
    area_objects = []
    for layer in json_data['layers']:
        if layer['type'] == 'objectgroup':
            for obj in layer['objects']:
                if 'type' in obj and (obj["type"] == "Area" or obj["type"] == "area"):
                    area_objects.append(obj)
                            
    return area_objects

def merge_polygon_to_rectangle(area_objects, tile_width, tile_height):
    rectangles = []
    for obj in area_objects:
        if 'polygon' in obj:
            min_x = min_y = float('inf')
            max_x = max_y = float('-inf')

            for point in obj['polygon']:
                min_x = min(min_x, point['x'])
                min_y = min(min_y, point['y'])
                max_x = max(max_x, point['x'])
                max_y = max(max_y, point['y'])

            rectangles.append({
                'name': obj['name'],
                'x': round((obj['x'] + min_x) / tile_width),
                'y': round((obj['y'] + min_y) / tile_height),
                'width': round((max_x - min_x) / tile_width),
                'height': round((max_y - min_y) / tile_height)
            })
        else:
            rectangles.append({
                'name': obj['name'],
                'x': round(obj['x']/tile_width),
                'y':  round(obj['y']/tile_height),
                'width': round(obj['width']/tile_width),
                'height': round(obj['height']/tile_height)
            })
    return rectangles

def generate_solidity_code(rectangles):
    solidity_code = '''pragma solidity ^0.8.0;

library AreaLib {
    struct AreaInfo {
        string name;
        uint x;
        uint y;
        uint width;
        uint height;
    }

    function getAreas() public pure returns (AreaInfo[] memory) {
        AreaInfo[] memory areas = new AreaInfo[]({len(rectangles)});
        '''
    for idx, rect in enumerate(rectangles):
        solidity_code += f'areas[{idx}] = AreaInfo("{rect["name"]}", {rect["x"]}, {rect["y"]}, {rect["width"]}, {rect["height"]});\n        '
    solidity_code += 'return areas;\n    }}'
    return solidity_code

def main():
    args = parse_arguments()

    with open(args.file, 'r') as f:
        json_data = json.load(f)

    tile_width = json_data['tilewidth']
    tile_height = json_data['tileheight']

    area_objects = extract_area_objects(json_data)
    print(area_objects)
    rectangles = merge_polygon_to_rectangle(area_objects, tile_width, tile_height)
    solidity_code = generate_solidity_code(rectangles)

    with open(args.output, 'w') as f:
        f.write(solidity_code)

if __name__ == '__main__':
    main()
