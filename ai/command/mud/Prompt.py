import re
from command.command_base import CommandBase


class Prompt(CommandBase):
    """New prompt from prompt component."""

    def execute(self, params):
        if not self.check_params(params, ["name"]):
            return self.error('invalid params')
        name = params["name"]
        if name not in self.app.agents:
            return self.error('invalid name')
        agent = self.app.agents[name]
        time_tick = self.get_nowtime_seconds()
        prompt = agent.mud.getValue("Prompt", f'{agent.mud.player}')
        content = prompt[0]
        source = prompt[1]
        update_time = prompt[2]
        reaction = agent.prompt("Your god tells: " + content, time_tick)
        language = agent.speak("Your god", reaction.get("memory_prompt", ""), reaction.get("prompt", ""), time_tick)
        if language:
            target_id = source
            agent.mud.send("Chat", f'({target_id},"{language}")')
            agent.language = language
            agent.timer["chat"] = self.get_nowtime_seconds()
            agent.languages.append({"source": agent.get_state("name"), "target": name, "content": language})
        return reaction
