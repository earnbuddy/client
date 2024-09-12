from email.policy import default

from src.earners.Earner import EarnerBase


class GaGaNode(EarnerBase):
    name = 'GaGaNode'
    image = 'xterna/gaga-node:latest'

    def get_envs(self):
        return {
            "TOKEN": self.settings.get('token', 'mlguyzkvqkytfyygdf917d54399f2115'),
        }