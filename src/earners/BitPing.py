from .Earner import EarnerBase


class BitPing(EarnerBase):
    name = "BitPing"
    image = "bitping/bitpingd"

    def get_run_command(self):
        return f"login --email '{self.settings.get('email')}' --password '{self.settings.get('password')}'"

