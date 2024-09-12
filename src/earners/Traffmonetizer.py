from .Earner import EarnerBase


class Traffmonetizer(EarnerBase):
    name = "Traffmonetizer"
    image = "traffmonetizer/cli_v2"

    def get_run_command(self):
        return f"start accept --token '{self.settings.get('token', '0m5icuGDKdqDXbzZWURfKzSOws86Jl9BbBs76gs+cs0=')}' --device-name '{self.device_name}'"
