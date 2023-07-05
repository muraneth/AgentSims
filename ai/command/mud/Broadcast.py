import re
from command.command_base import CommandBase


class Broadcast(CommandBase):
    """Broadcast news to everyone."""

    def execute(self, params):
        if not self.check_params(params, ["content"]):
            return self.error('invalid params')
        content = params["content"]
        # if name not in self.app.agents:
        #     return self.error('invalid name')
        # agent = self.app.agents[name]
        self.app.mud.send("Broadcast", f'"{content}"')
        self.app.flush_events()
        # for agent in self.app.agents.values():
        #     agent.save()
        # self.app.time_tick += 1
        # self.app.save_time_tick()
        # return {'tick': self.app.time_tick}
        return True
