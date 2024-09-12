from .Earner import EarnerBase


class PacketStream(EarnerBase):
    name = "PacketStream"
    image = "packetstream/psclient"

    def get_envs(self):
        return {
            "CID": self.settings.get('cid', '6RSL'),
        }


