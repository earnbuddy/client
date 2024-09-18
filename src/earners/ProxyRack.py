import uuid

from .Earner import EarnerBase


class ProxyRack(EarnerBase):
    name = "Proxyrack"
    image = "proxyrack/pop"

    def __init__(self):
        super().__init__()
        self.device_uuid = str(uuid.uuid5(uuid.NAMESPACE_DNS, self.device_name))

    def get_envs(self):
        return {
            "UUID": self.device_uuid,
        }

    def get_extra_heartbeat_data(self):
        return {
            "uuid": self.device_uuid,
        }
