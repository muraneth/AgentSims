import re
from command.command_base import CommandBase


class Tick(CommandBase):
    """server time tick ++."""

    def execute(self, params):
        # if not self.check_params(params, ["name"]):
        #     return self.error('invalid params')
        # name = params["name"]
        # if name not in self.app.agents:
        #     return self.error('invalid name')
        # agent = self.app.agents[name]
        # self.app.flush_events()
        # try:
        #     for agent in self.app.agents.values():
        #         agent.save()
        # except Exception:
        #     pass
        self.app.time_tick += 1
        self.app.save_time_tick()
        self.app.mud.send("TimeAware", f'{self.app.get_time_tick()}')
        return {'tick': self.app.time_tick}
