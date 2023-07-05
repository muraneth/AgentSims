from command.command_base import CommandBase


class CheckBlocks(CommandBase):
    """check mud set & remove events."""

    def execute(self, params):
        # start_block = self.app.block_num
        # result = self.app.mud.world.searchEvent("", start_block)
        # entrys = list()
        # for entry in result:
        #     block_number = entry["blockNumber"]
        self.app.flush_events()
        return True
