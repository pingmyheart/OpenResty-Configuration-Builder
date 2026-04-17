import yaml

from configuration.environment_configuration import routes_configuration_file_path
from dto.route import Route


class RouteService:
    def __init__(self):
        from configuration.logging_configuration import logger
        self.log = logger

    def parse_routes(self) -> list[Route]:
        final_routes = []
        # load routes file
        with open(routes_configuration_file_path, 'r') as config_file:
            data = yaml.safe_load(config_file)
        routes = data['nginx']['gateway']['routes']
        for route in routes:
            final_routes.append(Route.model_validate(route))
        return final_routes
