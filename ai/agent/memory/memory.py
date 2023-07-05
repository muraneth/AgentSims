from datetime import datetime
from typing import List, Dict, Any

from sentence_transformers import SentenceTransformer, util
# from torch import Tensor

model = SentenceTransformer("all-MiniLM-L6-v2")

BACKGROUND = 0
OBSERVATION = 1
PLAN = 2
REFLECTION = 3

class Memory:
    def __init__(self, content: str, importance: int, location: str, related_person: List[str], memory_type: int, time_tick: int):
        self.id = None
        self.content = content
        self.importance = importance
        self.location = location
        self.related_person = related_person
        self.created = time_tick
        self.last_access = self.created
        self.vector = model.encode(self.content)
        # 0: observation, 1: reflection, 2: plan
        self.memory_type = memory_type
        self.destoryed = False
    
    def set_id(self, id: int):
        self.id = id

    def access_age(self, time_tick) -> int:
        """
        Return time diff between last access & nowtime
        """
        diff = time_tick - self.last_access
        if diff > 0:
            return 1 / diff
        else:
            return 1

    def relevance(self, other_memory: "Memory") -> float:
        """
        Returns the memory's relevance to another memory by calculating the cosine similarity between the
        embedding vectors of the two memories.
        """
        sim = util.cos_sim(self.vector, other_memory.vector)
        return sim.tolist()[0][0]

    def retrieval_score(self, other_memory: "Memory", params: Dict[str, float], time_tick) -> float:
        """
        Return the retrieval score for the memory with respect to another memory.
        Retrieval score = recency_weight * recency + importance_weight * importance + relevance_weight * relevance(other_memory)
        :param other_memory:  plan -> memory / observer -> memory
        :return: 
        """
        recency = params['recency_weight'] * self.access_age(time_tick)
        importance = params['importance_weight'] * self.importance
        relevance = params['relevance_weight'] * self.relevance(other_memory)
        return recency + importance + relevance

    def to_json(self) -> Dict[str, Any]:
        ret_json = {
            'content': self.content,
            'importance': self.importance,
            'location': self.location,
            'related_person': self.related_person,
            'created': self.created,
            'last_access': self.last_access,
            'memory_type': self.memory_type,
            'destoryed': self.destoryed
        }
        ret_json["memory_type"]
        if self.id:
            ret_json['id'] = self.id
        return ret_json
    
    def from_json(self, json_obj: Dict[str, Any]):
        if json_obj:
            self.content = json_obj['content']
            self.vector = model.encode(self.content)
            self.id = json_obj.get("id")
            self.importance = json_obj.get("importance")
            self.location = json_obj.get("location")
            self.related_person = json_obj.get("related_person")
            self.created = json_obj.get("created")
            self.last_access = json_obj.get("last_access")
            self.destoryed = json_obj.get("destoryed")

class Observation(Memory):
    def __init__(self, content: str, importance: int, location: str, related_person: List[str], time_tick: int):
        super().__init__(content, importance, location, related_person, OBSERVATION, time_tick)

class Plan(Memory):
    def __init__(self, content: str, importance: int, location: str, related_person: List[str], time_tick: int):
        super().__init__(content, importance, location, related_person, PLAN, time_tick)
        self.completed = False

    def mark_completed(self):
        self.completed = True
    
    def to_json(self) -> Dict[str, Any]:
        ret_json = super().to_json()
        ret_json['completed'] = self.completed
        return ret_json
    
    def from_json(self, json_obj: Dict[str, Any]):
        if json_obj:
            super().from_json(json_obj)
            self.completed = json_obj.get('completed')

class Reflection(Memory):
    def __init__(self, content: str, importance: int, related_memory: Memory, location: str, related_person: List[str], time_tick: int):
        super().__init__(content, importance, location, related_person, REFLECTION, time_tick)
        self.related_memory = related_memory

class Background(Memory):
    def __init__(self, content: str, importance: int, location: str, related_person: List[str], time_tick: int):
        super().__init__(content, importance, location, related_person, BACKGROUND, time_tick)

def empty_memory() -> Memory:
    return Memory("", 0, "", [], 0, 0)

def empty_plan() -> Plan:
    return Plan("", 0, "", [], 0)
