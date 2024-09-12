from .Earner import EarnerBase


class SpideNetwork(EarnerBase):
    name = 'SpideNetwork'
    image = 'xterna/spide-network'

    def get_envs(self):
        return {
            "ID": self.device_name
        }
