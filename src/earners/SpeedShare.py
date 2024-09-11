from .Earner import EarnerBase


class SpeedShare(EarnerBase):
    name = "SpeedShare"
    image = "mrcolorrain/speedshare"

    def get_envs(self):
        return {
            "CODE": '214e70102de707a642fc',
            "SPEEDSHARE_UUID": self.device_name,
        }
