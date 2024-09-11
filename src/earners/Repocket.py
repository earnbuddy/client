from .Earner import EarnerBase


class Repocket(EarnerBase):
    name = "Repocket"
    image = "repocket/repocket"

    def get_envs(self):
        return {
            "RP_EMAIL": self.settings.get('email'),
            "RP_API_KEY": self.settings.get('password'),
        }
