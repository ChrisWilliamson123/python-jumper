from gameutils.game_settings import GameSettings

class JumperSettings(GameSettings):
    def __init__(self):
        self._player_x_speed = 200
        super().__init__()

    def parse_json(self, json_data):
        super().parse_json(json_data)
        self._player_x_speed = json_data.get('player_x_speed', 200)

    def build_json_dict(self):
        return {
            'player_x_speed': self._player_x_speed
        } | super().build_json_dict()

    # Getters and setters for base class properties
    @property
    def player_x_speed(self):
        return self._player_x_speed
    
    @player_x_speed.setter
    def framerate(self, speed):
        self._player_x_speed = speed
