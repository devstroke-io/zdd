from ...services.logger import Logger


class Configuration:
    _default_docker_params: dict = {
        "detach": True,
        "remove": True
    }
    _logger: Logger = Logger.get('main.zdd.configuration')

    def __init__(self, active: bool = False, docker_image: str = None, docker_params: dict = None):
        self.active = active
        self.docker_image = docker_image
        self.docker_params = docker_params

    def get_params(self, instance: int) -> dict:
        """Get Docker "run" parameters
        :param instance: Instance to run
        :type instance: int
        :return: docker "run" parameters for requested instance
        :rtype: dict
        """
        self._logger.info(f"Get params for instance {instance}")
        params = self._default_docker_params
        if not self.docker_params:
            return params
        if 'default' in self.docker_params:
            params = params.copy()
            params.update(self.docker_params['default'])
        if f'instance_{instance}' in self.docker_params:
            params = params.copy()
            params.update(self.docker_params[f'instance_{instance}'])
        self._logger.debug(params)
        return params
