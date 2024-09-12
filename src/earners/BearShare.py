from src.earners.Earner import EarnerBase


class BearShare(EarnerBase):
    name = 'BearShare'
    image = 'xterna/bearshare'

    def get_envs(self):
        return {
            "EMAIL": self.settings.get('email'),
            "PASSWORD": self.settings.get('password'),
        }

    def check_requirements(self):
        if self.settings.get('email') and self.settings.get('password'):
            return True
        return False