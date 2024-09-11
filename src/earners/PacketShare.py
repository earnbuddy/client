from .Earner import EarnerBase


class PacketShare(EarnerBase):
    name = "PacketShare"
    image = "packetshare/packetshare"

    def get_run_command(self):
        return f"-accept-tos -email={self.settings.get('email')} -password={self.settings.get('password')}"
