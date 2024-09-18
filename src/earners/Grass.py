from .Earner import EarnerBase


class Grass(EarnerBase):
    name = "Grass"
    image = "mrcolorrain/grass"

    def get_envs(self):
        return {
            "GRASS_USER": self.settings.get('email'),
            "GRASS_PASS": self.settings.get('password'),
        }

    def check_requirements(self):
        if self.settings:
            if self.settings.get('email') and self.settings.get('password'):
                return True
        return False


