# DevStroke ZDD

Zero Downtime Deployment system with Docker

## How it works

ZDD works with Docker services that expose one or more ports. It pulls and starts 2 containers, mapping services on differents host ports.

The main goal is to have a zero downtime deployment on a single server architecture.

I works for example with a Nginx load balancing system ([take a look here](http://nginx.org/en/docs/http/load_balancing.html))

Check the [full project example here](docs/full_example.md)

## Installation

### Pythonic way

```sh
pip install https://github.com/devstroke-io/zdd/archive/master.zip
```

### Download binary

```sh
sudo sh -c 'curl -L https://github.com/devstroke-io/zdd/releases/download/0.1.0/zdd-linux-x64 -o /usr/bin/zdd && chmod u+x /usr/bin/zdd'
```

## Configuration

Create a file `~/.config/zdd.json`
Home used must be the one of the user who will launch the script

Configuration example:

```json
{
  "projects": {
    "project1": {
      "active": true,
      "docker_image": "repository/project1",
      "docker_params": {
        "default": {
          "ports": {
            "80/tcp": 8000
          }
        },
        "instance_2": {
          "ports": {
            "80/tcp": 8001
          }
        }
      }
    },
    "project2": {
      "active": false,
      "docker_image": "repository/project2"
    }
  }
}
```

* **active** key specifies if the project can be deployed or not.
* **docker_image** key specifies docker hub link.
* **docker_params** key specifies container parameters at start.

> ZDD internally use [docker-py](https://github.com/docker/docker-py).
> Image parameters are available to https://docker-py.readthedocs.io/en/stable/containers.html

## Usage

```sh
Usage: zdd [OPTIONS] PROJECT [TAG]

  Deploy PROJECT with TAG (default 'latest')

Options:
  -V, --version  Show the version and exit.
  -q, --quiet    no output
  -v, --verbose  verbosity level
  -h, --help     Show this message and exit.
```

## Contributing

@TODO

### Build binary

```sh
pyinstaller --onefile zdd.py
```

Produce binary `dist/zdd`

> Binary built depends of plateform used

