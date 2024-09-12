from .Earner import EarnerBase
import re

class Pawns(EarnerBase):
    name = "Pawns"
    image = "iproyal/pawns-cli"

    def get_run_command(self):
        return f"-email='{self.settings.get('email')}' -password={self.settings.get('password')} -device-name='{self.device_name}' -device-id='{self.device_name}' -accept-tos"

    def get_extra_heartbeat_data(self):
        # Get some extra info from the logs of the container
        # Get the last line of the logs
        logs = self.container.logs().decode('utf-8').split('\n')
        # log format happened_at=2024-09-12T17:48:29Z name=balance_ready parameters={"balance":"1.679 USD","traffic":"8.3978 GB"}
        # extract the balance and traffic from the last log line using regex

        last_log = logs[-2]
        match = re.search(r'balance":"(.*?)"', last_log)
        balance = match.group(1)
        match = re.search(r'traffic":"(.*?)"', last_log)
        traffic = match.group(1).replace(' GB', '')
        return {
            'balance': balance,
            'traffic': traffic
        }

    def check_requirements(self):
        if self.settings.get('email') and self.settings.get('password'):
            return True
        return False
