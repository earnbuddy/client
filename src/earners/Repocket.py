from .Earner import EarnerBase


class Repocket(EarnerBase):
    name = "Repocket"
    image = "repocket/repocket"

    def get_envs(self):
        return {
            "RP_EMAIL": self.settings.get('email'),
            "RP_API_KEY": self.settings.get('api_key'),
        }

    def check_requirements(self):
        if self.settings:
            if self.settings.get('email') and self.settings.get('api_key'):
                return True
        return False