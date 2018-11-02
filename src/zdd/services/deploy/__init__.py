import json
import sys
from pathlib import Path
from time import sleep

import docker
from docker import DockerClient
from docker.errors import NotFound, APIError

from .configuration import Configuration
from ...services.cursor import Cursor
from ...services.logger import Logger


class Deploy:
    _client: DockerClient = None
    _config: Configuration = None
    _logger: Logger = Logger.get('main.zdd')
    _project: str = None
    _tag: str = None

    def __init__(self, project: str, tag: str) -> None:
        self._project = project
        self._tag = tag
        config = self.__fetch_config()
        self._config = Configuration(**config)
        self._client = docker.from_env()

    def reload(self) -> None:
        self._logger.info(f"Reload {self._config.docker_image}:{self._tag}")
        image: dict = self._client.images.get(name=f'{self._config.docker_image}:{self._tag}')
        if not image:
            self._logger.critical(f"Cannot find image {self._config.docker_image}:{self._tag} locally")
            sys.exit(120)
        self.__reload_instance(1)
        self.__reload_instance(2)

    def pull(self) -> None:
        """Pull project's Docker image
        :return: None
        :rtype: None
        """
        self._logger.info(f"Pull {self._config.docker_image}:{self._tag}")
        lines = {}
        api_client = docker.APIClient()
        try:
            for line in api_client.pull(self._config.docker_image, tag=self._tag, stream=True):
                line = json.loads(line)
                if 'id' in line:
                    if line['id'] not in lines:
                        lines[line['id']] = {
                            'status': None,
                            'progress': None
                        }
                        sys.stdout.write('\n')
                    if 'progress' in line:
                        lines[line['id']]['progress'] = line['progress']
                    if 'status' in line:
                        lines[line['id']]['status'] = line['status']
                    index = list(lines).index(line['id'])
                    move = len(list(lines)) - index
                    Cursor.move_up(move)
                    Cursor.move_start()
                    Cursor.erase_to_the_end()
                    sys.stdout.write(f"{line['id']}: {lines[line['id']]['status']}")
                    if lines[line['id']]['status'] == 'Downloading' and lines[line['id']]['progress'] is not None:
                        sys.stdout.write(f" {lines[line['id']]['progress']}")
                    Cursor.move_down(move)
                    Cursor.move_start()
                elif 'status' in line:
                    print(f"{line['status']}")
        except NotFound:
            self._logger.critical(f"'{self._config.docker_image}:{self._tag}' not found on Docker HUB")
            sys.exit(110)

    def __reload_instance(self, instance: int) -> None:
        image = f'{self._config.docker_image}:{self._tag}'
        container_name = f'{self._project}_{instance}'
        params = self._config.get_params(instance)
        # stop instance
        try:
            container = self._client.containers.get(container_name)
        except NotFound:
            container = None
        if container:
            self._logger.info(f"Stop {container_name} instance...")
            container.stop()
            self._logger.info(f"{container_name} instance stopped")
        # run instance
        self._logger.info(f"Start {container_name} instance...")
        try:
            self._client.containers.run(
                image,
                name=container_name,
                **params
            )
            self._logger.info(f"{container_name} instance running")
        except APIError as e:
            self._logger.critical(f"Fail to run {container_name} with {str(e)}")
            sys.exit(130)
        # @TODO(damien): Check if instance is really up (request :port ?)
        sleep(1)

    def __fetch_config(self) -> dict:
        """Get and decode JSON configuration file content
        :return: Project configuration from JSON
        :rtype: dict
        """
        try:
            file = str(Path.home()) + '/.config/zdd.json'
            self._logger.info(f"Fetch configuration file ({file})")
            with open(file) as content:
                config = json.load(content)
        except FileNotFoundError:
            self._logger.critical(f"Cannot find configuration file ({file})")
            sys.exit(100)
        except json.JSONDecodeError:
            self._logger.critical(f"Cannot decode configuration file ({file})")
            sys.exit(101)
        if 'projects' not in config:
            self._logger.critical(f"'projects' key missing in configuration file ({file})")
            sys.exit(102)
        if self._project not in config['projects']:
            self._logger.critical(f"Project '{self._project}' not in configuration file ({file})")
            sys.exit(103)
        if not config['projects'][self._project]['active']:
            self._logger.critical(f"Project '{self._project}' is deactivated in configuration file ({file})")
            sys.exit(104)
        if 'docker_image' not in config['projects'][self._project]:
            self._logger.critical(
                f"Missing 'docker_image' key for project '{self._project}' in configuration file ({file})")
            sys.exit(105)
        self._logger.debug(config['projects'][self._project])
        return config['projects'][self._project]
