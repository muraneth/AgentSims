.PHONY: test

export_map:
	python3 tmj2bitmap.py -f ./test_data/Game-map_0.tmj -o ./output/test.txt
	python3 tmj2area.py -f ./test_data/Game-map_0.tmj -o ./output/area.sol
	python3 tmj2objects.py -f ./test_data/Game-map_0.tmj -o ./output/objects.sol

export_map2:
	python3 tmj2bitmap.py -f ./test_data/Expanded-game-map_1.4_0520.tmj -o ./output/test.txt
	python3 tmj2area.py -f ./test_data/Expanded-game-map_1.4_0520.tmj -o ./output/area.sol
	python3 tmj2objects.py -f ./test_data/Expanded-game-map_1.4_0520.tmj -o ./output/objects.sol

equipment:
	python3 equipment2types.py -f ./test_data/equipment.json -o ./output/equipment_types.sol

export_map3:
	python3 tmj2bitmap.py -f ./test_data/Dunhuang_map.tmj -o ./output/test.txt
	python3 tmj2area.py -f ./test_data/Dunhuang_map.tmj -o ./output/area.sol
	python3 tmj2objects.py -f ./test_data/Dunhuang_map.tmj -o ./output/objects.sol
