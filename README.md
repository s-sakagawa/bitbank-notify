# bitbank-notify
This bot notifies you of information obtained from the [https://bitbank.cc/](https://bitbank.cc/) Public & Private API using [LINE Notify](https://notify-bot.line.me/ja/).

## Requirements
- [Docker](https://www.docker.com)
- [GNU Make](https://www.gnu.org/software/make/)

## Installation
Before installation, you must meet requirements.
```bash
$ git clone https://github.com/s-sakagawa/bitbank-notify
$ cd bitbank-notify
$ make build
```

## Setting API Key
`src/settings.py`
```python
# LINE Notify
TOKEN = ''

# bitbank
API_KEY = ''
API_SECRET = ''
```

## Implemented Commands
The commands are implemented by Makefile.

### Build Docker image
```bash
$ make build
```

### Run Docker container (bash)
```bash
$ make bash
```

## How to use

```bash
# Notify ticker
(bash)$ python main.py ticker

# Notify asset
(bash)$ python main.py asset

# Notify orders
(bash)$ python main.py orders
```
