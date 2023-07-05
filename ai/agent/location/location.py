from typing import List, Dict, Any
import re

from agent.memory.memory import Memory, Observation, Background, Plan, Reflection, BACKGROUND, OBSERVATION, PLAN, REFLECTION
from agent.memory.memory_stream import MemoryStream
from utils.gpt import GPTCaller
from utils.tools import timestamp_to_datetime, format_timestamp
from config import LocationConfig

class Properties:
    def __init__(self, properties: Dict[str, Any]) -> None:
        self.properties = properties
        # for key, value in config.agent_properties.items():
        #     self.properties[key] = properties[key] if key in properties else value

    def get_property(self, key: str) -> Any:
        return self.properties[key]
    
    def set_property(self, key: str, value: Any):
        self.properties[key] = value

    def to_json(self) -> Dict[str, Any]:
        return self.properties

class Location:
    def __init__(self, config: LocationConfig, app) -> None:  # , properties: Dict[str, Any]
        # self.gpt = gpt
        self.app = app
        self.people = set()
        self.config = config
        self.properties =  Properties(config.location_properties)

    def enter(self, name: str):
        self.people.add(name)
    
    def leave(self, name: str):
        self.people.remove(name)
    
    def get_people(self) -> List[str]:
        return [x for x in self.people]

    def change_state(self, key: str, value: Any):
        """
        agent change location/name/etc.
        """
        self.properties.set_property(key, value)
    
    def get_state(self, key: str) -> Any:
        """
        agent get location/name/etc.
        """
        return self.properties.get_property(key)
    
    def to_description(self) -> str:
        name = self.get_state("name")
        near = ",".join(self.get_state("near"))
        equipments = ",".join(self.get_state("equipments"))
        equipment_descriptions = list()
        for eq in self.get_state("equipments"):
            equipment = self.app.get_equipment_config(eq).description
            equipment_descriptions.append(equipment)
        equipment_descriptions = "".join(equipment_descriptions)
        people = ",".join(self.people) if self.people else "nobody"
        ret_str = f"{name} is a place near {near} and it has {equipments}.{equipment_descriptions}People in {name} are: {people}"
        return ret_str
