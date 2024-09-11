from .Earner import EarnerBase


class EarnFM(EarnerBase):
    name = "EarnFM"
    image = "earnfm/earnfm-client"

    def get_envs(self):
        return {
            "EARNFM_TOKEN": self.settings.get('api_key'),
        }


