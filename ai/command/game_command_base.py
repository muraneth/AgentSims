import requests
from command.command_base import CommandBase


class GameCommandBase(CommandBase):
    """More game related methods."""

    # Call scene api server.
    # id: which player's scene server.
    def call_scene(self, type, data=None, id=None, api_host=None):
        if id is None:
            id = self.id

        # Get user's current scene address.
        if api_host is None:
            onlineModel = self.get_single_model('Online', id, False)
            if onlineModel is None:
                return False
            api_host = onlineModel.get_apihost()

        request = {'token': self.get_token(), 'type': type, 'data': data}
        response = requests.post(api_host, json=request).json()
        if 'error' in response:
            return self.error(response['error'])
        return response['data']

    # Get scene server apihost by x,y.
    def get_scene_apihost(self, x, y):
        start_x = int(x / self.config.db_map_x_per_table)
        start_y = int(y / self.config.db_map_y_per_table)
        scene_game_model = self.get_game_model('Scene')
        scene_info = scene_game_model.get_scene(start_x, start_y)
        if not scene_info:
            return False
        return scene_info['api_host']
