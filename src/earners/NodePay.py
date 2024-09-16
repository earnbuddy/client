from .Earner import EarnerBase


class NodePay(EarnerBase):
    name = 'NodePay'
    image = 'kellphy/nodepay'

    def check_requirements(self):
        if self.settings.get('cookie'):
            return True
        return False

    def get_envs(self):
        return {
            "NP_COOKIE": self.settings.get('cookie')
        }