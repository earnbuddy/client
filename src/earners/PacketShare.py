from .Earner import EarnerBase


class PacketShare(EarnerBase):
    name = "PacketShare"
    image = "packetshare/packetshare"

    def get_run_command(self):
        return f"-accept-tos -email={self.settings.get('email')} -password={self.settings.get('password')}"

    def get_extra_heartbeat_data(self):
        # extract the balance and traffic from the last log line using regex
        logs = self.container.logs().decode('utf-8').split('\n')
        # loop through the logs from the last one to the older ones and  look for a log line like this: [2024-09-12 12:24:18] Current points: 88.71  |  Current traffic: 867.00M  |  Current Bonus: $0.08
        for log in reversed(logs):
            if 'Current \'s points' in log:
                parts = log.split('|')
                points = parts[0].split(':')[1].strip()
                traffic = parts[1].split(':')[1].strip()
                return {
                    'points': points,
                    'traffic': traffic
                }

    def check_requirements(self):
        if self.settings:
            if self.settings.get('email') and self.settings.get('password'):
                return True
        return False