from pathlib import Path

import nginxfmt

from builder.location_builder import LocationBuilder
from builder.method_builder import MethodBuilder
from builder.server_builder import ServerBuilder
from configuration.environment_configuration import output_directory
from configuration.logging_configuration import logger as log
from filters.filter import Filter
from service import route_service_impl

if __name__ == '__main__':
    # Util
    snake_to_camel = lambda s: s.split('_')[0] + ''.join(x.capitalize() for x in s.split('_')[1:])

    # Init Nginx Formatter
    nginx_formatter = nginxfmt.Formatter()

    # Find all routes
    routes = route_service_impl.parse_routes()

    # Group routes by their location
    grouped_routes = {}
    for route in routes:
        if route.location not in grouped_routes:
            grouped_routes[route.location] = []
        grouped_routes[route.location].append(route)

    # Print grouped routes
    for location, routes in grouped_routes.items():
        print(f"Location: {location}")
        for route in routes:
            print(
                f"\tRoute Name: {route.name}, \n\t\tMethods: {route.methods} \n\t\tFilters: {[route_filter.name for route_filter in route.filters]}")

    # Generate nginx configuration
    config = "server {\n"
    config += "listen 80;\n"
    server_builder = ServerBuilder().set_listen(80)
    for location, routes in grouped_routes.items():
        log.info(f"Building configuration for location `{location}`")
        location_builder = (LocationBuilder().set_location(location)
                            .add_directive("proxy_set_header", "Host $host")
                            .add_directive("proxy_set_header", "X-Real-IP $remote_addr")
                            .add_directive("proxy_set_header", "X-Forwarded-For $proxy_add_x_forwarded_for"))
        for route in routes:
            # Sort filter by order method
            for method in route.methods:
                method_builder = MethodBuilder().set_method(method)
                filter_instances = []
                for route_filter in route.filters:
                    log.debug(f"Processing filter `{route_filter.name}` for route `{route.location}`")
                    # Dynamically import filter class
                    module = __import__(f"filters.{route_filter.name}_filter",
                                        fromlist=[route_filter.name.capitalize() + "Filter"])
                    filter_class = getattr(module, snake_to_camel(route_filter.name.capitalize()) + "Filter")
                    filter_instance: Filter = filter_class(**route_filter.args)
                    filter_instances.append(filter_instance)
                    filter_instance.apply_filter(method_builder)
                location_builder.add_method(method_builder)
        server_builder.add_location(location_builder)

        log.info(f"Building configuration for location `{location}` completed")

    Path(output_directory).mkdir(parents=True, exist_ok=True)
    with open(f"{output_directory}/default.conf", 'w') as output_file:
        output_file.write(nginx_formatter.format_string(server_builder.build()))
