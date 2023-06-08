# ccxt-execution-notification-to-discord
## Getting Started

Install requirements.

```bash
pip install ccxt loguru
```

Place a json file `apis.json` in which keys are exchange names and values are api keys and secrets.

```json
{
  "binance": {
    "apiKey": "XXX",
    "secret": "YYY"
  },
  "binanceusdm": {
    "apiKey": "xxx",
    "secret": "yyy"
  },
  "okx": {
    "apiKey": "ZZZ",
    "secret": "zzz"
  }
}
```

Run the script.

```bash

python main.py --exchange binance binanceusdm okx --webhook ${YOUR_WEBHOOK_URL}

```

Your will receive a message like `Start watching your executions at the following exchanges: ['binance', 'binanceusdm', 'okx]` on your webhook channel.

Other args.


```bash
usage: main.py [-h] --exchange EXCHANGE [EXCHANGE ...] --webhook WEBHOOK [--apis APIS] [--restart_interval RESTART_INTERVAL] [--log LOG]

options:
  -h, --help            show this help message and exit
  --exchange EXCHANGE [EXCHANGE ...]
                        Exchange name (ccxt name)
  --webhook WEBHOOK     Discord webhook url
  --apis APIS           Path to your api key json file
  --restart_interval RESTART_INTERVAL
                        Restart interval of watching execution (default: 12 hours)
  --log LOG             Path to log file
```
