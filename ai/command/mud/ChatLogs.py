import re
from command.command_base import CommandBase


class ChatLogs(CommandBase):
    """get chat logs by name."""

    def execute(self, params):
        if not self.check_params(params, ["name"]):
            return self.error('invalid params')
        name = params["name"]
        if name not in self.app.agents:
            return self.error('invalid name')
        agent = self.app.agents[name]
        return {"logs": agent.languages[-10:][::-1]}
