from .Earner import EarnerBase


class EarnFM(EarnerBase):
    name = "EarnFM"
    image = "earnfm/earnfm-client"

    def get_envs(self):
        return {
            "EARNFM_TOKEN": self.settings.get('api_key', 'be5ddf72-7742-492e-bca1-e89db4b66861'),
        }


