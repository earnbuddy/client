from .Earner import EarnerBase


class Traffmonetizer(EarnerBase):
    name = "Traffmonetizer"
    image = "traffmonetizer/cli_v2"

    def get_run_command(self):
        return f"start accept --token '{self.settings.get('token')}' --device-name '{self.device_name}'"
