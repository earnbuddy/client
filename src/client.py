import asyncio
import platform

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
from earners.GaGaNode import GaGaNode
from earners.BearShare import BearShare
from earners.SpideNetwork import SpideNetwork
from earners.NodePay import NodePay

from decouple import config

from utils.get_ip_info import get_ip_info

class MainLoop:
    public_ip = None
    VERSION = '0.0.9'
    docker = docker.from_env()
    device_name = config('DEVICE_NAME')
    API_URL = config('API_URL', default=None)

    http_auth_user = config('HTTP_AUTH_USERNAME', default=None)
    http_auth_pass = config('HTTP_AUTH_PASSWORD', default=None)

    def __init__(self):
        self.earners = []


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
            requests.post(f"{self.API_URL}/api/machines/{self.device_name}/heartbeat/", json=message, auth=(self.http_auth_user, self.http_auth_pass))

            await asyncio.sleep(60*30) # 30 minutes

    async def run(self):
        while True:
            # Send client heartbeat
            asyncio.create_task(self.send_heartbeat())

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
    print(f"Starting EarnBuddy Client v{loop.VERSION}")
    print(f"Device Name: {loop.device_name}")
    print(f"API URL: {loop.API_URL}")

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
    if 'GaGaNode' not in INGNORE_EARNERS:
        loop.earners.append(GaGaNode())
    if 'BearShare' not in INGNORE_EARNERS:
        loop.earners.append(BearShare())
    if 'SpideNetwork' not in INGNORE_EARNERS:
        loop.earners.append(SpideNetwork())
    if 'NodePay' not in INGNORE_EARNERS:
        loop.earners.append(NodePay())

    asyncio.run(loop.run())
