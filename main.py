import asyncio
import json
from argparse import ArgumentParser

import ccxt.pro
import requests
from loguru import logger


def load_apis(filepath: str) -> dict:
    with open(filepath) as f:
        return json.load(f)


def check_api_keys(apis: dict, exchanges: list[str]) -> None:
    for e in exchanges:
        if e not in apis:
            raise ValueError(f"No API keys are found for {e}")


def init_ccxt_client(exchange: str, apis: dict) -> ccxt.pro.Exchange:
    try:
        client_cls = getattr(ccxt.pro, exchange)
    except AttributeError:
        raise ValueError(f"Exchange {exchange} is not supported")
    return client_cls({**apis[exchange]})


def trade_to_message(exchange: str, trade: dict) -> str:
    try:
        return (
            f"{exchange} - {trade['side'].upper()}: {trade['symbol']} at {trade['price']} "
            f"with a lot of {trade['amount']}"
        )
    except KeyError:
        return f"{exchange} - {trade}"


def post_discord(webhook: str, message: str) -> None:
    requests.post(webhook, json={"content": message})


async def watch_execution(
    exchange: str, apis: dict, webhook: str, restart_interval: int = 3600 * 12
) -> None:
    client = init_ccxt_client(exchange, apis)

    async def _loop():
        while True:
            trade = await client.watch_my_trades()
            for t in trade:
                post_discord(webhook, trade_to_message(exchange, t))
                logger.info(f"Execution: {t}")

    logger.info(f"Start watching: {exchange}")

    while True:
        try:
            await asyncio.wait_for(_loop(), restart_interval)
        except asyncio.TimeoutError as e:
            logger.info(f"Restarting {exchange}")


async def main(args):
    logger.add(args.log, rotation="10MB", retention=3)
    apis = load_apis(args.apis)
    exchanges = args.exchange
    check_api_keys(apis, exchanges)

    post_discord(
        args.webhook,
        f"Start watching your executions at the following exchanges: {exchanges}",
    )

    await asyncio.gather(
        *[
            watch_execution(e, apis, args.webhook, args.restart_interval)
            for e in exchanges
        ]
    )


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument(
        "--exchange", required=True, nargs="+", help="Exchange name (ccxt name)"
    )
    parser.add_argument("--webhook", required=True, help="Discord webhook url")
    parser.add_argument(
        "--apis", default="./apis.json", help="Path to your api key json file"
    )
    parser.add_argument(
        "--restart_interval",
        default=3600 * 12,
        help="Restart interval of watching execution (default: 12 hours)",
    )
    parser.add_argument("--log", default="log.txt", help="Path to log file")
    args = parser.parse_args()

    try:
        asyncio.run(main(args))
    except KeyboardInterrupt:
        ...
