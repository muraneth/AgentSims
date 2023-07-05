import re
from command.command_base import CommandBase
import datetime, time


class React(CommandBase):
    """check mud env & generate reaction."""

    def execute(self, params):
        if not self.check_params(params, ["name"]):
            return self.error('invalid params')
        react_start = time.time()
        self.app.log(f"start React: {str(datetime.datetime.now())}")
        name = params["name"]
        if name not in self.app.agents:
            return self.error('invalid name')
        agent = self.app.agents[name]
        time_tick = self.app.get_time_tick()  # self.get_nowtime_seconds()
        reaction = agent.react("", time_tick)
        self.app.log(str(reaction))

        action_start = time.time()
        self.app.log(f"start action: {str(datetime.datetime.now())}")
        # action
        # {'location': 'Park', 'operation': 'go to chosen buildings', 'duration': 120, 'equipment': None, 'content': None, 'moving': True}
        # {'location': 'Cafe', 'equipment': None, 'operation': 'go to chosen buildings', 'duration': 300, 'content': None, 'interaction': True}
        if "operation" in reaction:
            operation = reaction["operation"]
            if operation.get("moving"):
                while agent.move_path:
                    x, y = agent.move_path[0][0], agent.move_path[0][1]
                    if agent.move_to(x, y):
                        self.app.log(f"moving to {x},{y}")
                        agent.move_path.pop(0)
                    sight = agent.get_sight(self.app.get_time_tick())
                    if not agent.able_to_continue(sight):
                        break
            elif operation.get("location") and operation.get("location") != agent.get_state("location"):
                self.app.log("Navigating to: "+operation.get("location"))
                agent.navigate(operation['location'], "location")
            if operation.get("interaction") and operation.get("operation"):
                if agent.timer.get("action", 0):
                    self.app.log("continue: "+operation["operation"])
                    agent.action = operation["operation"]
                else:
                    agent.finished.add(agent.action)
                    agent.action = ""
                    agent.timer["action"] = 0
                    agent.timer["action_display"] = 0
            elif operation.get("operation") not in {"go to chosen buildings", "talk with nearby people"}:
                # agent.navigate(operation['equipment'], "equipment")
                o = operation.get("operation")
                if o != agent.action:
                    position = reaction.get("sight", dict()).get("operation_dict", dict()).get(o)
                    if position:
                        # equipment_id = self.app.entities
                        equipment = self.app.equipments[self.app.coord2equipment.get(position[0], dict()).get(position[1])]
                        name = equipment["type"]
                        if self.app.entities.get(agent.mud.player, dict()).get("Position")[0] != position:
                            self.app.log("Navigating to: "+name+".and will execute: "+o)
                            agent.navigate(name, "equipment")
                        agent.action = o
                        duration = operation.get("duration", 60)
                        if not duration:
                            duration = 60
                        agent.timer["action"] = time_tick + duration
                        agent.timer["action_display"] = self.get_nowtime_seconds() + 10
                        if o in ["write music", "write poem", "write novel", "write rap music"]:
                            writing_prompt = agent.config.writing_prompt
                            writing_prompt = writing_prompt.replace("{target_content}", reaction.get("sight", dict()).get("observation", ""))
                            writing_prompt = writing_prompt.replace("{plan}", agent.plan)
                            agent.writing_prompt = writing_prompt
                # self.app.log("Navigating to: "+operation.get("location"))
            if operation.get("name") and operation.get("content"):
                language = operation.get("content", "")
                target_id = 0
                if operation.get("name") in self.app.agents:
                    target_id = self.app.agents[operation.get("name")].mud.player
                self.app.log("Chatting with: "+operation.get("name")+".and content is : "+operation.get("content"))
                agent.mud.async_send("Chat", f'({target_id},"{language}")')
                agent.language = language
                agent.speak_to = operation.get("name")
                agent.timer["chat"] = self.get_nowtime_seconds() + 10
                agent.languages.append({"source": agent.get_state("name"), "target": operation.get("name"), "content": language})
                # agent.status = "Chatting with " + operation.get("name")

        # timer
        if agent.language and self.get_nowtime_seconds() > agent.timer.get("chat", 0):
            # language stay 60s on chain
            self.app.log("chatting time out: "+agent.language)
            agent.mud.async_send("CancelChat", f'{agent.mud.player}')
            agent.finished.add(f'speak "{agent.language}" in the last moment')
            agent.language = ""
            agent.speak_to = ""
            agent.timer["chat"] = 0
        if agent.action and agent.timer.get("action", 0) and time_tick > agent.timer.get("action", 0):
            self.app.log("action time out: "+agent.action)
            if agent.writing_prompt and not agent.writing:
                agent.write()
            agent.finished.add(agent.action)
            agent.action = ""
            agent.timer["action"] = 0
            agent.timer["action_display"] = 0
        if agent.emotion != agent.last_emotion and agent.emotion and self.get_nowtime_seconds() > agent.timer.get("emotion", 0):
            agent.last_emotion = agent.emotion
            agent.timer["emotion"] = 0

        # status
        if agent.emotion != agent.last_emotion and agent.emotion and agent.timer.get("emotion", 0) > 0:
            agent.status = agent.emotion
        if agent.language:
            agent.status = "Talking to: " + agent.speak_to  # + ": " + agent.language  # "Chatting with " + agent.speak_to
        elif agent.action and self.get_nowtime_seconds() < agent.timer.get("action_display", 0):
            agent.status = "Action now: " + agent.action
            self.app.log("status: "+agent.status)
        elif agent.move_path and agent.navigate_to:
            # status move
            self.app.log("status: moving")
            agent.status = f"Moving to {agent.navigate_to}"
        elif agent.plan != "no plan yet":
            agent.status = "Planning to: " + agent.plan
        else:
            agent.status = "Wandering"
        if agent.status != self.app.entities.get(agent.mud.player, dict()).get("Status"):
            agent.mud.send("Status", f'"{agent.status}"')
        if agent.plan != self.app.entities.get(agent.mud.player, dict()).get("Plan"):
            agent.mud.send("Plan", f'"{agent.plan}"')
        self.app.log(f"end action: {str(datetime.datetime.now())}, time used: {str(time.time()-action_start)}")
        agent.save()
        self.app.flush_events()
        self.app.log(f"end React: {str(datetime.datetime.now())}, time used: {str(time.time()-react_start)}")
        return True
