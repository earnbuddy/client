from .Earner import EarnerBase


class Pawns(EarnerBase):
    name = "Pawns"
    image = "iproyal/pawns-cli"

    def get_run_command(self):
        return f"-email='{self.settings.get('email')}' -password={self.settings.get('password')} -device-name='{self.device_name}' -device-id='{self.device_name}' -accept-tos"