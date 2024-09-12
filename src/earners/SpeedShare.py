from .Earner import EarnerBase


class SpeedShare(EarnerBase):
    name = "SpeedShare"
    image = "mrcolorrain/speedshare"

    def get_envs(self):
        return {
            "CODE": self.settings.get('code'),
            "SPEEDSHARE_UUID": self.device_name,
        }

    def check_requirements(self):
        if self.settings.get('code'):
            return True
        return False