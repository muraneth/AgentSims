from flask import Flask, request, jsonify
from flask_cors import CORS
# from app import App
import time
import os
from config import Config, AgentConfig, LocationConfig, EquipmentConfig, TerrainConfig
import importlib
from utils.tools import load_json_file, format_timestamp
from utils.gpt import GPTCaller
from utils.w3 import MUDConnector
from agent.agent import Agent
from agent.location.location import Location

class App:
    def __init__(self, flask):
        self.flask = flask
        self.logger = flask.logger
        self.abs_path = os.path.dirname(os.path.realpath(__file__))

        self.load_agent_configs(os.path.join(self.abs_path, 'config', 'agent.json'))
        self.load_location_configs(os.path.join(self.abs_path, 'config', 'location.json'))
        self.load_equipment_configs(os.path.join(self.abs_path, 'config', 'equipment.json'))
        self.load_terrain_configs(os.path.join(self.abs_path, 'config', 'terrain.json'))

        # Load main configuration file.
        self.config = Config(os.path.join(self.abs_path, 'config', 'app.json'))
        self.mud = MUDConnector(self.config.admin_private_key, self.config)
        self.map = self.mud.get_map()
        self.get_saved_time_tick()
        self.start_time = 1682870400  # self.get_nowtime_seconds()
        # self._init_equipments()
        self.width = len(self.map)
        self.height = len(self.map[0])
        self.gpt = GPTCaller(self.config)
        self.equipments = dict()
        self.coord2equipment = dict()
        self.equipment2coords = dict()
        # self.clear_log()
        self.entities = dict()
        self.position = dict()
        self.flush_events()

        # Set up log level.
        self.logger.setLevel(self.config.log_level)

        self.playerid2name = dict()
        self.agents = dict()
        self.locations = dict()
        # self.components = dict()
        self.init_agent()
        print("App inited")
        self.flush_events()
        # init map

    # Call a command.
    def call_command(self, name, params=None):
        # Import module.
        module = importlib.import_module(f"command.{name}")
        # Get class.
        cls = getattr(module, name.split('.')[-1])
        # Create the command object.
        cmd = cls(self)
        # Execute command.
        res = cmd._execute(params)
        # Close db connections.
        for db in cmd.db_cache.values():
            db.close()
        # Return response
        return res
        # agent = self.agents[name]
        # return agent.react("", self.get_nowtime_seconds())
    
    def get_saved_time_tick(self):
        self.time_tick = 0
        path = os.path.join(self.abs_path, 'time_tick.txt')
        if os.path.exists(path):
            with open(path, 'r', encoding='utf-8') as agent_file:
                self.time_tick = int(agent_file.read())

    def save_time_tick(self):
        path = os.path.join(self.abs_path, 'time_tick.txt')
        with open(path, 'w', encoding='utf-8') as agent_file:
            # json_obj = json.loads(agent_file)
            agent_file.write(str(self.time_tick))
    
    def clear_log(self):
        log_file = open(os.path.join(self.abs_path, 'server.log'), 'w', encoding='utf-8')
        log_file.close()
    
    def log(self, info: str):
        if self.config.print_log:
            print(info)
        with open(os.path.join(self.abs_path, 'server.log'), 'a', encoding='utf-8') as log_file:
            log_file.write(info)
            log_file.write("\n")

    def load_agent_configs(self, path):
        self.agent_config = dict()
        self.names = list()
        # Load json file.
        objs = load_json_file(path)
        # Read data.
        for obj in objs:
            config = AgentConfig(obj)
            self.agent_config[config.id] = config
            self.names.append(config.id)

    def get_agent_config(self, id):
        return self.agent_config[id]

    def load_location_configs(self, path):
        self.location_config = dict()
        # Load json file.
        objs = load_json_file(path)
        # Read data.
        for obj in objs:
            config = LocationConfig(obj)
            self.location_config[config.id] = config
            # self.names.append(config.id)

    def get_location_config(self, id):
        return self.location_config[id]

    def load_equipment_configs(self, path):
        self.equipment_config = dict()
        # Load json file.
        objs = load_json_file(path)
        # Read data.
        for obj in objs:
            config = EquipmentConfig(obj)
            self.equipment_config[config.id] = config
            # self.names.append(config.id)
    
    def get_time_tick(self):
        return self.start_time + self.time_tick * self.config.seconds_per_tick

    def get_equipment_config(self, id):
        return self.equipment_config[id]

    def load_terrain_configs(self, path):
        self.terrain_config = dict()
        # Load json file.
        objs = load_json_file(path)
        # Read data.
        for obj in objs:
            config = TerrainConfig(obj)
            self.terrain_config[config.id] = config
            # self.names.append(config.id)

    def get_terrain_config(self, id):
        return self.terrain_config[id]
    
    def parse_events(self):
        for entity, info in self.entities.items():
            if "ItemMetadata" in info:
                n, t, f = info["ItemMetadata"]
                tx, ty, bx, by = info["Boundary2D"]
                for x in range(tx, bx+1):
                    for y in range(ty, by+1):
                        coord = (x, y)
                        if coord[0] not in self.coord2equipment:
                            self.coord2equipment[coord[0]] = dict()
                        self.coord2equipment[coord[0]][coord[1]] = entity
                        if t not in self.equipment2coords:
                            self.equipment2coords[t] = set()
                        self.equipment2coords[t].add(coord)
                self.equipments[entity] = {
                    "name": n,
                    "type": t,
                    "functions": f
                }
                if t in self.equipment_config:
                    self.equipments[entity]['config'] = self.get_equipment_config(t)
            if "Position" in info:
                if "ItemMetadata" in info:
                    n, t, f = info["ItemMetadata"]
                    if t not in self.equipment_config:
                        continue
                x, y = info["Position"][0]
                if x not in self.position:
                    self.position[x] = dict()
                self.position[x][y] = entity

    # Get current timestamp, milliseconds.
    def get_nowtime(self):
        return int(time.time() * 1000)

    # Get current timestamp, seconds.
    def get_nowtime_seconds(self):
        return int(time.time())
    
    def in_bounds(self, x, y):
        return 0 <= x < self.width and 0 <= y < self.height
    
    def passable(self, x, y):
        return self.get_terrain_config(self.map[x][y]).passable
    
    def neighbors(self, x, y):
        results = []
        # 上
        if self.in_bounds(x - 1, y) and self.passable(x - 1, y):
            results.append((x - 1, y))
        # 下
        if self.in_bounds(x + 1, y) and self.passable(x + 1, y):
            results.append((x + 1, y))
        # 左
        if self.in_bounds(x, y - 1) and self.passable(x, y - 1):
            results.append((x, y - 1))
        # 右  
        if self.in_bounds(x, y + 1) and self.passable(x, y + 1):
            results.append((x, y + 1))
        return results

    def init_agent(self):
        for id, cfg in self.location_config.items():
            location = Location(cfg, self)
            self.locations[id] = location
        for id, cfg in self.agent_config.items():
            agent = Agent(self.gpt, cfg, self)
            self.playerid2name[agent.mud.player] = agent.get_state("name")
            self.agents[id] = agent
            # self.locations[agent.get_state("location")].enter(id)
            agent.store_background(int(time.time()))
            print("Agent inited:", id)
    
    def flush_events(self):
        events = self.mud.get_events()
        for event in events:
            if event["entity"] not in self.entities:
                self.entities[event["entity"]] = dict()
            if event["action"] == "set":
                if event["component_name"] == "Position" and "Position" in self.entities[event["entity"]]:
                    position = self.entities[event["entity"]]["Position"]
                    x, y = position[0]
                    # print(x, y)
                    if x in self.position and y in self.position[x]:
                        del self.position[x][y]
                self.entities[event["entity"]][event["component_name"]] = event["data"]
            else:
                if event["entity"] in self.entities and event["component_name"] in self.entities[event["entity"]]:
                    del self.entities[event["entity"]][event["component_name"]]
        self.parse_events()

# Create the flask object.
flask = Flask(__name__)
# TODO Real CORS.
CORS(flask)

# Create the app object.
app = App(flask)


# Route - /api
@flask.route('/api/<command>', methods=['POST'])
def api(command):
    resp = app.call_command(command, request.json)
    if 'error' in resp:
        return {'__error__': resp['error'], 'refresh': resp.get('doRefresh', True)}
    # print(resp['data'])
    return jsonify(resp['data'])


# Entrance
if __name__ == '__main__':
    app.logger.info("----------CryptoPro PyServer Started.----------")
    app.flask.run(host=app.config.agent_host, port=app.config.agent_port, debug=True)
    app.logger.info("----------CryptoPro PyServer Stopped.----------")
