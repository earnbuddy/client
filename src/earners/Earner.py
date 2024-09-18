import asyncio

import docker
import requests
from decouple import config


class EarnerBase:
    name = None
    image = None
    docker = docker.from_env()
    container = None
    device_name = config('DEVICE_NAME')
    API_URL = config('API_URL', default=None)
    settings = {}
    http_auth_user = config('HTTP_AUTH_USERNAME', default=None)
    http_auth_pass = config('HTTP_AUTH_PASSWORD', default=None)

    status = 'Starting'

    def get_envs(self):
        return None

    def get_run_command(self):
        return None

    def check_requirements(self):
        return True

    def get_settings_data_from_api(self):
        res = requests.get(f"{self.API_URL}/api/earners/{self.name}/settings/", auth=(self.http_auth_user, self.http_auth_pass))
        if res.status_code == 200:
            self.settings = res.json().get('settings')

    def start(self):
        self.get_settings_data_from_api()

        if self.check_requirements():
            self.status = 'StartingContainer'
        else:
            self.status = 'RequirementsNotMet'

        if self.status == 'StartingContainer':
            # Check if a container with the same name already exists
            containers = self.docker.containers.list(all=True)
            for container in containers:
                if container.name == self.name:
                    self.container = container
                    break

            # If the container exists but is not running, remove it
            if self.container and self.container.status != 'running':
                self.container.remove()

            # If the container does not exist or was removed, start a new one
            if not self.container or self.container.status != 'running':
                print(f"Starting container for {self.name}")
                self.container = self.docker.containers.run(
                    self.image,
                    command=self.get_run_command(),
                    environment=self.get_envs(),
                    name=self.name,
                    detach=True,
                    restart_policy={'Name': 'always'},
                    remove=False)

        # Schedule the heartbeat coroutine
        asyncio.create_task(self.send_heartbeat())

    def stop_container(self):
        if self.container:
            self.container.stop()

    def pull_update(self):
        # Pull the latest image
        self.docker.images.pull(self.image)
        # Restart the container with the new image
        self.restart_container()

    def restart_container(self):
        if self.container:
            self.container.restart()

    def get_container_status(self):
        if self.container:
            self.container.reload()
            return self.container.status
        return None

    def get_container_stats(self):
        if self.container:
            stats = self.container.stats(stream=False)
            return stats['cpu_stats'], stats['memory_stats']
        return None, None

    def get_extra_heartbeat_data(self):
        return {}

    async def send_heartbeat(self):
        while True:
            print(f"Sending heartbeat for {self.name}")
            cpu_usage, ram_usage = self.get_container_stats()
            uptime = self.container.attrs['State']['StartedAt']
            extra_data = self.get_extra_heartbeat_data()  # Get the extra data

            message = {
                "status": self.status,
                "cpu_usage": cpu_usage.get('cpu_usage').get('total_usage'),
                "ram_usage": ram_usage.get('usage'),
                "uptime": str(uptime),
            }

            # Add the extra data to the message
            if extra_data:
                message.update({"extra_data": extra_data})


            requests.post(f"{self.API_URL}/api/machines/{self.device_name}/{self.name}/heartbeat/", json=message, auth=(self.http_auth_user, self.http_auth_pass))

            await asyncio.sleep(600) # Send heartbeat every 10 minutes