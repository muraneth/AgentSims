import time
import os
from config import Config, AgentConfig, LocationConfig, EquipmentConfig, TerrainConfig
import importlib
from utils.tools import load_json_file, format_timestamp
from utils.gpt import GPTCaller
from utils.w3 import MUDConnector
from agent.agent import Agent
from agent.location.location import Location

# abs_path = os.path.dirname(os.path.realpath(__file__))
# config = Config(os.path.join(abs_path, 'config', 'app.json'))
class App:
    def __init__(self):
        # self.flask = flask
        # self.logger = flask.logger
        self.abs_path = os.path.dirname(os.path.realpath(__file__))

        self.load_agent_configs(os.path.join(self.abs_path, 'config', 'agent.json'))
        self.load_location_configs(os.path.join(self.abs_path, 'config', 'location.json'))
        self.load_equipment_configs(os.path.join(self.abs_path, 'config', 'equipment.json'))
        self.load_terrain_configs(os.path.join(self.abs_path, 'config', 'terrain.json'))

        # Load main configuration file.
        self.config = Config(os.path.join(self.abs_path, 'config', 'app.json'))
        self.mud = MUDConnector(self.config.admin_private_key, self.config)
        self.map = self.mud.get_map()
        self._init_equipments()
        self.width = len(self.map)
        self.height = len(self.map[0])
        self.gpt = GPTCaller(self.config)
        self.block_num = 0

        # Set up log level.
        # self.logger.setLevel(self.config.log_level)

        self.playerid2name = dict()
        self.agents = dict()
        self.locations = dict()
        self.init_agent()
        # init map
        self.clear_log()
    
    def clear_log(self):
        log_file = open(os.path.join(self.abs_path, 'loop.log'), 'w', encoding='utf-8')
        log_file.close()
    
    def log(self, info: str):
        if self.config.print_log:
            print(info)
        with open(os.path.join(self.abs_path, 'loop.log'), 'a', encoding='utf-8') as log_file:
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
    
    def _init_equipments(self):
        self.equipments = self.mud.get_equipments()
        self.coord2equipment = dict()
        for equipment, info in self.equipments.items():
            for coord in info['coords']:
                if coord[0] not in self.coord2equipment:
                    self.coord2equipment[coord[0]] = dict()
                self.coord2equipment[coord[0]][coord[1]] = equipment
            if info["type"] in self.equipment_config:
                self.equipments[equipment]['config'] = self.get_equipment_config(info["type"])

    # Get current timestamp, milliseconds.
    def get_nowtime(self):
        return int(time.time() * 1000)

    # Get current timestamp, seconds.
    def get_nowtime_seconds(self):
        return int(time.time())
    
    def in_bounds(self, row, col):
        return 0 <= row < self.height and 0 <= col < self.width
    
    def passable(self, row, col):
        return self.get_terrain_config(self.map[row][col]).passable
    
    def neighbors(self, row, col):
        results = []
        # 上
        if self.in_bounds(row - 1, col) and self.passable(row - 1, col):
            results.append((row - 1, col))
        # 下
        if self.in_bounds(row + 1, col) and self.passable(row + 1, col):
            results.append((row + 1, col))
        # 左
        if self.in_bounds(row, col - 1) and self.passable(row, col - 1):
            results.append((row, col - 1))
        # 右  
        if self.in_bounds(row, col + 1) and self.passable(row, col + 1):
            results.append((row, col + 1))
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
    
    def run(self):
        # init agents
        agents = dict()
        # locations = dict()
        # init map
        # for id, cfg in self.location_config.items():
        #     location = Location(cfg, self)
        #     locations[id] = location
        for id, cfg in self.agent_config.items():
            print("init agent:", id)
            agent = Agent(self.gpt, cfg, self)
            agents[id] = agent
            print("init agent finished:", id)
            # locations[agent.get_state("location")].enter(id)
            agent.store_background(int(time.time()))
        # start loop
        for tick in range(3):
            self.log("tick: "+str(tick))
            time_tick = int(time.time()) + tick * 60 * 60
            self.log("time_tick: "+str(time_tick)+" "+format_timestamp(time_tick))
            for id, agent in agents.items():
                self.log("agent: "+id)
                # location = locations[agent.get_state("location")]
                # obs = location.to_description()
                # self.log("observation: "+obs)
                # friends = agent.get_state("friends")
                # for person in location.get_people():
                    # if person not in friends:
                    #     friends.append(person)
                # agent.set_state("friends", friends)
                # self.log("friends: "+",".join(friends))
                act = agent.react("", time_tick)
                self.log("act: "+act)
                # for person in friends:
                #     if person in act:
                #         obs = f"{id} is about to {act}."
                #         self.log(person+f" has spotted {obs} but CODER-fisher let {person} do thing.")
                # if tick % 2 == 0:
                #     # reflect
                #     agent.reflect(time_tick)
                # for id in self.location_config.keys():
                #     # location move
                #     if id in act and id != location.get_state("name"):
                #         location.leave(agent.get_state("name"))
                #         next_location = locations[id]
                #         next_location.enter(agent.get_state("name"))
                #         break

if __name__ == "__main__":
    app = App()
    app.run()
