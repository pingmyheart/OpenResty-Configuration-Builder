# OpenResty-Configuration-Builder

*Lightweight API Gateway Configurer for OpenResty*

![Last Commit](https://img.shields.io/github/last-commit/pingmyheart/OpenResty-Configuration-Builder)
![Repo Size](https://img.shields.io/github/repo-size/pingmyheart/OpenResty-Configuration-Builder)
![Issues](https://img.shields.io/github/issues/pingmyheart/OpenResty-Configuration-Builder)
![Pull Requests](https://img.shields.io/github/issues-pr/pingmyheart/OpenResty-Configuration-Builder)
![License](https://img.shields.io/github/license/pingmyheart/OpenResty-Configuration-Builder)
![Top Language](https://img.shields.io/github/languages/top/pingmyheart/OpenResty-Configuration-Builder)
![Language Count](https://img.shields.io/github/languages/count/pingmyheart/OpenResty-Configuration-Builder)

## Features

- **Dynamic Configuration**: Automatically configures OpenResty based on configuration.
- **Seamless Integration**: Designed to work with OpenResty, providing a smooth experience for developers and operators.
- **Configuration First Approach**: Emphasizes a configuration-first approach, allowing users to define their API
  gateway settings in routes YAML file.
- **Scalability**: Can handle a large number of API routes and configurations without performance degradation.

## Required Configuration

To use the builder, you need to provide a configuration in YAML format that follows the structure
below:

```yaml
nginx:
  gateway:
    routes:
      - name: "route-name"
        location: "/api/location/to/expose"
        methods:
          - "GET"
          - "POST"
        filters:
          ...
```

and it's important to configure environment variables to set configuration file path and output directory for OpenResty
configuration:

```bash
OUTPUT_DIRECTORY=target
ROUTES_CONFIGURATION_FILE_PATH=in/routes.yaml
```

Default directories are `/config/routes.yaml` for configuration file and `/etc/nginx/conf.d` for output directory since
it is meant to be used inside a initContainer of Kubernetes to generate configuration alongside nginx container.

### Available Filters

1. **Proxy Pass Filter**: Proxies the request to the specified upstream server.  
   This filter forwards the request to the defined URI in the configuration. The URI should point to the upstream
   service that you want to expose through the API gateway.

```yaml
name: proxy_pass
args:
  uri: "http://upstream-service:80"
```

2**Rewrite Filter**: Rewrites the request URL based on specified rules.  
   This filter allows you to modify the incoming request URL before it is processed by the upstream service. You can
   define rewrite rules in the configuration to specify how the URL should be rewritten.

```yaml
name: rewrite
args:
  regex: "^/api/(.*)"
  replacement: "/$1"
```

## How It Works

1. The software watches for all routes defined in the configuration
2. Find routes with same locations and group them together
3. Generate OpenResty configuration based on the defined routes and filters
4. Filters are applied dynamically based on the name of the filter.

> Filter name should be defined in filters module and should have the name of the file like `name_you_want_filter` and
> inner class should be `NameYouWantFilter`. camel case for file and pascal case for class

