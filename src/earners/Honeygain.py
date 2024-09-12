from .Earner import EarnerBase


class Honeygain(EarnerBase):
    name = "HoneyGain"
    image = "honeygain/honeygain"

    def get_run_command(self):
        return f"-tou-accept -email '{self.settings.get('email')}' -pass '{self.settings.get('password')}' -device '{self.device_name}'"

    def check_requirements(self):
        if self.settings.get('email') and self.settings.get('password'):
            return True
        return False