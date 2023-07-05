import requests
import os
from config import Config, AgentConfig
from utils.tools import load_json_file
import time
import datetime
from threading import Thread

def handle_agent(agent_name: str):
    for i in range(100):
        data = {
            "name": agent_name
        }
        start = time.time()
        print(str(datetime.datetime.now()), "start request:", agent_name)
        try:
            response = requests.post(f"http://{host}:{config.agent_port}/api/mud.React", json=data)
            print(str(datetime.datetime.now()), "name:", agent_name, response.json(), "spend time:", time.time() - start)
        except:
            pass
        if time.time() - start_time > 60 * 3:
            break
    print(str(datetime.datetime.now()), "name:", agent_name, f"{i} rounds done", "spend time:", time.time() - start)


# cfg = Config()
abs_path = os.path.dirname(os.path.realpath(__file__))
config = Config(os.path.join(abs_path, 'config', 'app.json'))
host = config.agent_host if config.agent_host != "0.0.0.0" else "localhost"
agent_path = os.path.join(abs_path, 'config', 'agent.json')
names = list()
# Load json file.
objs = load_json_file(agent_path)
start_time = time.time()
# Read data.
for obj in objs:
    cfg = AgentConfig(obj)
    # self.agent_config[config.id] = config
    names.append(cfg.id)
print(names)
agent_name = "Tamara Taylor"
# names = ["Eddy Lin", "Yuriko Yamamoto"]
# for agent_name in names:
t = Thread(target=handle_agent, args=(agent_name,))
t.start()
for _ in range(1000):
    response = requests.post(f"http://{host}:{config.agent_port}/api/mud.Tick", json={})
    print("tick:", response.json())
    if time.time() - start_time > 3 * 61:
        break
    time.sleep(15)
