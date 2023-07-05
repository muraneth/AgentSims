import argparse
import json
import os

def set_block(bitmap, x1, y1, x2, y2):
    for i in range(y1, y2 + 1):
        for j in range(x1, x2 + 1):
            bitmap[i][j] = 1

def is_block(obj):
    if 'properties' in obj:
        for prop in obj['properties']:
            if (prop['name'] == "Block" or prop['name'] == "block") and prop['type'] == "bool" and prop['value'] is True:
                return True
    return False

def point_inside_polygon(x, y, poly):
    n = len(poly)
    inside = False
    p1x, p1y = poly[0]
    for i in range(1, n + 1):
        p2x, p2y = poly[i % n]
        if y > min(p1y, p2y):
            if y <= max(p1y, p2y):
                if x <= max(p1x, p2x):
                    if p1y != p2y:
                        xinters = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                    if p1x == p2x or x <= xinters:
                        inside = not inside
        p1x, p1y = p2x, p2y
    return inside

def set_polygon_blocks(bitmap, obj, tile_width, tile_height):
    poly = [(obj['x'] + point['x'], obj['y'] + point['y']) for point in obj['polygon']]

    min_x, min_y = round(min(x for x, _ in poly) // tile_width), round(min(y for _, y in poly) // tile_height)
    max_x, max_y = round(max(x for x, _ in poly) // tile_width), round(max(y for _, y in poly) // tile_height)

    for y in range(min_y, max_y + 1):
        for x in range(min_x, max_x + 1):
            if point_inside_polygon(x * tile_width + tile_width/2, y * tile_height + tile_height/2, poly):
                bitmap[y][x] = 2

def tmj_to_bitmap(tmj_path, output_path):
    with open(tmj_path, 'r') as file:
        tmj_data = json.load(file)

    map_width = tmj_data['width']
    map_height = tmj_data['height']
    tile_width = tmj_data['tilewidth']
    tile_height = tmj_data['tileheight']

    bitmap = [[0 for _ in range(map_width)] for _ in range(map_height)]

    for layer in tmj_data['layers']:
        if layer['type'] == "objectgroup":
            for obj in layer['objects']:
                if is_block(obj):
                    x, y = obj['x'] // tile_width, obj['y'] // tile_height
                    if 'polygon' not in obj:
                        w, h = obj['width'] // tile_width, obj['height'] // tile_height
                        set_block(bitmap, x, y, x + w - 1, y + h - 1)
                    else:
                        set_polygon_blocks(bitmap, obj, tile_width, tile_height)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with open(output_path, 'w') as file:
            file.write("[\n")
            for row in bitmap[:-1]:
                file.write("[" + ','.join(str(cell) for cell in row) + "],\n")
            file.write("[" + ','.join(str(cell) for cell in bitmap[-1]) + "]\n")
            file.write("]\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert TMJ map file to 2D bitmap array")
    parser.add_argument('-f', '--file', required=True, help="Path to the TMJ map file")
    parser.add_argument('-o', '--output', required=True, help="Path to the output txt file")
    args = parser.parse_args()

    tmj_to_bitmap(args.file, args.output)
