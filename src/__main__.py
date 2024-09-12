import asyncio
import platform
import signal
import os
import subprocess
from email.policy import default

import docker
import requests

from earners.BitPing import BitPing
from earners.EarnFM import EarnFM
from earners.Grass import Grass
from earners.Honeygain import Honeygain
from earners.PacketStream import PacketStream
from earners.Pawns import Pawns
from earners.ProxyRack import ProxyRack
from earners.Repocket import Repocket
from earners.SpeedShare import SpeedShare
from earners.Traffmonetizer import Traffmonetizer
from earners.PacketShare import PacketShare
from decouple import config

from utils.get_ip_info import get_ip_info

GITHUB_REPO = "earnbuddy/client"
UPDATE_ZIP = "client.zip"
CLIENT_ZIP = "client.zip"
OLD_ZIP = "old.zip"
LOCK_FILE = "lock.pid"

class MainLoop:
    public_ip = None
    VERSION = '0.0.1'
    docker = docker.from_env()
    device_name = config('DEVICE_NAME')
    API_URL = config('API_URL', default=None)
    check_update_interval = int(config('CHECK_UPDATE_INTERVAL', default=24))
    http_auth_user = config('HTTP_AUTH_USERNAME', default=None)
    http_auth_pass = config('HTTP_AUTH_PASSWORD', default=None)

    def __init__(self):
        self.earners = []

    async def check_for_updates(self):
        if config('CHECK_FOR_UPDATES', default='False') == 'True':
            while True:
                print("Checking for updates")
                latest_release = self.get_latest_release()
                latest_version = latest_release["tag_name"]
                if latest_version > self.VERSION:
                    print(f"New version available: {latest_version}")
                    download_url = latest_release["assets"][0]["browser_download_url"]
                    self.download_update(download_url)
                    self.replace_client()
                    self.restart_client()
                else:
                    print("No update available.")
                await asyncio.sleep(self.check_update_interval * 3600)

    async def send_heartbeat(self):
        while True:
            print("Sending Heartbeat")
            self.public_ip = get_ip_info()

            message = {
                'device_name': self.device_name,
                'public_ip': self.public_ip,
                'client_version': self.VERSION,
                'docker_version': self.docker.version()['Version'],
                'system_platform': platform.system()
            }
            requests.post(f"{self.API_URL}/api/clients/{self.device_name}/heartbeat/", json=message, auth=(self.http_auth_user, self.http_auth_pass))

            await asyncio.sleep(5)

    def get_latest_release(self):
        url = f"https://api.github.com/repos/{GITHUB_REPO}/releases/latest"
        response = requests.get(url)
        response.raise_for_status()
        return response.json()

    def download_update(self, download_url):
        response = requests.get(download_url)
        response.raise_for_status()
        with open(UPDATE_ZIP, 'wb') as file:
            file.write(response.content)

    def replace_client(self):
        if os.path.exists(UPDATE_ZIP):
            if os.path.exists(CLIENT_ZIP):
                os.rename(CLIENT_ZIP, OLD_ZIP)
            os.rename(UPDATE_ZIP, CLIENT_ZIP)

    def restart_client(self):
        if os.path.exists(LOCK_FILE):
            with open(LOCK_FILE, 'r') as f:
                pid = int(f.read().strip())
                try:
                    os.kill(pid, signal.SIGTERM)
                except OSError:
                    pass
            os.unlink(LOCK_FILE)

        # Start the new client
        new_process = subprocess.Popen(["python", CLIENT_ZIP])
        with open(LOCK_FILE, 'w') as f:
            f.write(str(new_process.pid))

    async def run(self):
        while True:
            # Send client heartbeat
            asyncio.create_task(self.send_heartbeat())

            # Check for updates
            asyncio.create_task(self.check_for_updates())

            # Get stats for all earners
            for earner in self.earners:
                earner.start()
            await asyncio.sleep(600)  # 10 minute for testing


if __name__ == '__main__':
    if not config('DEVICE_NAME'):
        print("DEVICE_NAME is required")
        exit(1)

    if not config('API_URL'):
        print("API_URL is required")
        exit(1)

    loop = MainLoop()

    # add the earners after checking if they are not in the IGNORE_EARNERS list
    INGNORE_EARNERS = config('IGNORE_EARNERS', default='').split(',')
    if 'BitPing' not in INGNORE_EARNERS:
        loop.earners.append(BitPing())
    if 'EarnFM' not in INGNORE_EARNERS:
        loop.earners.append(EarnFM())
    if 'Grass' not in INGNORE_EARNERS:
        loop.earners.append(Grass())
    if 'Honeygain' not in INGNORE_EARNERS:
        loop.earners.append(Honeygain())
    if 'PacketStream' not in INGNORE_EARNERS:
        loop.earners.append(PacketStream())
    if 'Pawns' not in INGNORE_EARNERS:
        loop.earners.append(Pawns())
    if 'ProxyRack' not in INGNORE_EARNERS:
        loop.earners.append(ProxyRack())
    if 'Repocket' not in INGNORE_EARNERS:
        loop.earners.append(Repocket())
    if 'SpeedShare' not in INGNORE_EARNERS:
        loop.earners.append(SpeedShare())
    if 'Traffmonetizer' not in INGNORE_EARNERS:
        loop.earners.append(Traffmonetizer())
    if 'PacketShare' not in INGNORE_EARNERS:
        loop.earners.append(PacketShare())

    asyncio.run(loop.run())
