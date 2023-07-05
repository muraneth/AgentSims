import os
import json
from utils.tools import load_json_file, get_json_value

abs_path = os.path.dirname(os.path.realpath(__file__))

class Config:
    """Main configuration."""
    def __init__(self, path):

        # Load json file.
        obj = load_json_file(path)

        # Read data.
        self.version = obj["version"]
        self.online = obj["online"]
        self.log_level = get_json_value(
            obj, "log_level", "debug").upper()
        self.print_log = get_json_value(
            obj, "print_log", True)
        
        self.seconds_per_tick = get_json_value(
            obj, "seconds_per_tick", 15 * 60)
        
        self.agent_host = get_json_value(
            obj, "agent_host", "0.0.0.0")
        self.agent_port = get_json_value(
            obj, "agent_port", 9802)
        agent_path = get_json_value(
            obj, "agent_path", "exports")
        self.agent_path = os.path.join(abs_path, agent_path)
        if not os.path.exists(self.agent_path):
            os.makedirs(self.agent_path, exist_ok=True)

        self.gpt_host = get_json_value(
            obj, "gpt_host", "localhost")
        self.gpt_port = get_json_value(
            obj, "gpt_port", 9801)
        gpt_api_keys_path = get_json_value(
            obj, "gpt_api_keys_path", os.path.join(abs_path, "config/api_keys.json"))
        if not os.path.exists(gpt_api_keys_path):
            raise ValueError("GPT api key not found.")
        with open(gpt_api_keys_path, "r", encoding="utf-8") as api_file:
            self.gpt_api_keys = json.loads(api_file.read())
        self.gpt3_cooldown = get_json_value(
            obj, "gpt3_cooldown", 30)
        self.gpt_temp = get_json_value(
            obj, "gpt_temp", 0.6)
        self.gpt_proxy = get_json_value(
            obj, "gpt_proxy", "http://127.0.0.1:7890")
        self.gpt_use_proxy = get_json_value(
            obj, "gpt_use_proxy", False)
        
        self.world_address = get_json_value(
            obj, "world_address", "0x7B4f352Cd40114f12e82fC675b5BA8C7582FC513")
        self.w3_RPC = get_json_value(
            obj, "w3_RPC", None)
        self.w3_WSRPC = get_json_value(
            obj, "w3_WSRPC", None)
        self.abi_dir = get_json_value(
            obj, "abi_dir", os.path.join(abs_path, "../contracts/abi"))
        self.mud_components = get_json_value(
            obj, "mud_components", [
                "Position"
            ])
        self.mud_systems = get_json_value(
            obj, "mud_systems", [
                "Move"
            ])
        self.admin_private_key = get_json_value(
            obj, "admin_private_key", "0x86a80a3f189c23bc7fa7b2efad60572a4e72c0d90ae3d2e5ae08f4bdb4727bf0")

        # # Game database - global tables.
        # self.db_game_host = get_json_value(
        #     obj, "db_game_host", "127.0.0.1")
        # self.db_game_port = get_json_value(
        #     obj, "db_game_port", 3306)
        # self.db_game_user = get_json_value(
        #     obj, "db_game_user", "root")
        # self.db_game_pwd = get_json_value(
        #     obj, "db_game_pwd", "")
        # self.db_game_name = get_json_value(
        #     obj, "db_game_name", "cryptopro_game")


class AgentConfig:
    """Agent configuration."""
    def __init__(self, obj):

        # Load json file.
        # obj = load_json_file(path)
        self.agent_properties = get_json_value(
            obj, "agent_properties", {
                "name": "Archer",
                "location": "Archer's home",
                "social relationship": "None",
                "career": "",
                "friends": []})

        self.id = self.agent_properties["name"]
        self.plan_prompt = get_json_value(
            obj, "plan_prompt", """
You can perceive something nearyby, they are:```
{target_content}
```
Your last plan is:```
{plan}
```
What's your next plan? Return in JSON format, where the `location` field can represent the building to go to, and the `interaction` field represents what to do after going to the selected building.
You are now at: ```
{location}
```
The buildings you can go to are given in JSON format:
```
{locations}
```
""")
        self.plan_model = get_json_value(
            obj, "plan_model", "gpt-3.5-turbo")
        self.start_reflect_prompt = get_json_value(
            obj, "start_reflect_prompt", "It's {time} and You are going to review some memories.")
        self.reflect_time_diff = get_json_value(
            obj, "reflect_time_diff", 3 * 60 * 60 * 1000)
        self.reflect_importance = get_json_value(
            obj, "reflect_importance", 1
        )
        self.reflect_prompt = get_json_value(
            obj, "reflect_prompt", "How do you think about {target_name}?")
        self.reflect_model = get_json_value(
            obj, "reflect_model", "gpt-3.5-turbo")
        self.act_prompt = get_json_value(
            obj, "act_prompt", """
You can perceive something nearyby, they are:```
{target_content}
```
Your plan is:```
{plan}
```
Now please think aboud what action do you want to choose based on your plan, you don't need to tell me. Then, you should tell me the most relevant operation with what you want to do from "available operation list". If you choose "go to your chosen buildings", you should choose a building on the map additionally.  If you are already in the place you want to go to, you just need to choose what equipment you want to do operation. If you choose "talk with nearby people", you should choose a person nearby from "Nearby people list" additionally. If you choose other operation, you shoold choose an equipment and set a duration additionally.
Available operation list is:```
{operations}
```
Buildings on the map list:```
{locations}
```
Nearby people list is:```
{people}
```
What's your next action? Your action should be formed in JSON format, where the `location` field can be used to indicate the building to go to,  `equipment` field to indicate the equipments to interact with, the `operation` field indicates the behavior to interact with, the `duration` field to indicate how many seconds to interact, duration should be an integer, the `name` field indicates the person to communicate with, and the `content` field indicates what to say to this person. If someone is talking to you, you are supposed to response to him in a proper way. The above fields can be a null value if you do not want to perform the related operation.
""")
        self.act_model = get_json_value(
            obj, "act_model", "gpt-3.5-turbo")
        self.background_prompt = get_json_value(
            obj, "background_prompt", r"""
You are a game character who can reponse to other charcter and you will be provided with a retrived memory. 
You should not know anything beyond your character settings or memory. 
All your actions must conform to your personality. Your personality is measured using data from the MBTI personality test. Your personality is represented by four variables, all ranging from 1 to 10, where 1 to 10 represents a uniform transition relationship. In the first number, 1 represents Extravert and 10 represents Introvert. The second number 1 represents Sensing, and 10 represents Intuition. The third number 1 represents Intuition and 10 represents Feeling. The fourth number 1 represents the judgment, and 10 represents Perceiving.
Your personality is :
```{
{MBTI}
}```
Based on your personality, your daily behavior also needs to conform to the worldview of the game. Of course, different personalities are allowed to have different understandings of the worldview. The worldview of the game is as follows:
```{
Have a daily routine like a real human.You will work, rest, eat, sleep, communicate with people, and leisure at reasonable times that match your own professional characteristics and personality traits. Even if you have an appointment with others, remember to travel. Once received a message from the broadcast, you must plan to write music or poem or novel or rap music in Art plaza that match your introduction.
}```
You have also been provided with a biography to introduce your identity, profession, and social relationships. This will serve as your basic introduction and cannot be changed. It is:
```{
"Name": {name}
"Age": {age}
"Carrer":{career}
"Social Relationship":{social relationship}
"Other Introduction":{other introduction}
}```

"""
        )
        self.background_importance = get_json_value(
            obj, "background_importance", 3
        )
        self.importance_prompt = get_json_value(
            obj, "importance_prompt", "Your {source} is {content}. How would you evaluate this {source} between 1 to 5, 1 is the least important?Reply with only one number.")
        self.importance_model = get_json_value(
            obj, "importance_model", "gpt-3.5-turbo")
        self.prompt_replaces = get_json_value(
            obj, "prompt_replaces", ["{target_name}", "{name}", "{location}", "{social relationship}", "{other introduction}", "{time}", "{career}", "{MBTI}", "{age}", "{locations}", "{target_content}", "{memory}"])

        self.retrieve_params = {
            "retrieval_score_threshold": get_json_value(obj, "retrieval_score_threshold", 0.6),
            "recency_weight": get_json_value(obj, "recency_weight", 0.6),
            "importance_weight": get_json_value(obj, "importance_weight", 0.6),
            "relevance_weight": get_json_value(obj, "relevance_weight", 0.6),
        }

        self.writing_prompt = """
You can perceive something nearyby, they are:```
{target_content}
```
Your plan is:```
{plan}
```
Now you are at creating point, you can write something. Based on your plan and memory and your personality and what you perceive, you need to choose a topic and a style to write. Now what topic do you want to choose? What style do you want to choose? You want to write a poem, a music, a rap music or a novel? You don't need to answer me the above questions, just write what you want to write. 
"""

        self.sight = get_json_value(
            obj, "sight", 15)
        self.init_coin = get_json_value(
            obj, "init_coin", 100)
        # self.terrain_prompt = get_json_value(
        #     obj, "terrain_prompt", "There is a block {x_distance} meters on your {LorR} and {y_distance} meters on your {TorB}, which is {passable} to pass.")
        self.player_prompt = get_json_value(
            obj, "player_prompt", "{name} is in your sight.")
        self.equipment_operation = get_json_value(
            obj, "equipment_operation", "You can choose to {operation} with {name}, you {owner} to be the owner.")
        self.chat_prompt = get_json_value(
            obj, "chat_prompt", "You can choose to chat with {name}.")
        self.speak_prompt = get_json_value(
            obj, "chat_prompt", "You can going to chat with {target}.What are you going to say?")
        self.move_prompt = get_json_value(
            obj, "move_prompt", "You can choose to move 1 meter {direct}.")
        self.navigate_prompt = get_json_value(
            obj, "navigate_prompt", "You can choose to navigate to any location.")
        self.private_key = get_json_value(
            obj, "private_key", "")
        self.operation_prompt = get_json_value(
            obj, "operation_prompt", "Under the situation of {origin}. You decided to {content} and your choices are: {operations}.You can do other things you want to do.What are you going to do?")
        if not self.private_key:
            from utils.w3 import new_account
            self.private_key = new_account()

class LocationConfig:
    """Location configuration."""
    def __init__(self, obj):

        # Load json file.
        # obj = load_json_file(path)
        self.location_properties = get_json_value(
            obj, "location_properties", {
                "name": "Archer's Home",
                "near": ["Cafe", "Office"],
                "equipments": ["bed", "tv", "dinner table", "kitchen"],
            })

        self.id = self.location_properties["name"]

class EquipmentConfig:
    """Equipment configuration."""
    def __init__(self, obj):
        self.id = obj["name"]
        self.name = self.id
        self.description = get_json_value(obj, "description", "You can sleep with a bed.")
        # {"distance": 1, "name": "sleep", "owner": true}
        self.operations = get_json_value(obj, "operations", [])

class TerrainConfig:
    """Terrain configuration."""
    def __init__(self, obj):

        # Load json file.
        # obj = load_json_file(path)
        self.id = obj["id"]
        self.name = get_json_value(
            obj, "name", "Nothing")
        self.passable = get_json_value(obj, "passable", False)
