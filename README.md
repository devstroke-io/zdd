# DevStroke ZDD

Zero Downtime Deployment system with Docker

## Installation

### Pythonic way

```sh
pip install https://github.com/devstroke-io/zdd/archive/master.zip
```

### Download binary

@TODO

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

## Build binary

```sh
pyinstaller --onefile zdd.py
```

Produce binary `dist/zdd`
