[中文](./README.cn.md)

# Magpie

A stock tool. Set stop-loss and revenue points for stocks, 
and initiate message pushes when stop-loss or revenue points are reached. 

Provides a simple web server for viewing the current prices of relevant stocks.

Note:

- Supports push notifications using [Telegram](https://telegram.org/) / [Bark](https://github.com/Finb/Bark/blob/master/README.en.md).

## Usage

### Edit the rule file

The rule is described in `Json` format. 
Edit the rule and save it as a file named `rule.json`.

```
[
  {
    "stock_code": "sh000001",
    "stock_name": "上证指数",
    "base_price": 3200,  # Base price for calculating the increase
    "alarm_price_min": 3100,  # Stop-loss point
    "alarm_price_max": 3400  # Revenue point
  },
  {
    "stock_code": "sz000333",
    "stock_name": "美的",
    "base_price": 54,
    "alarm_percentage_min": 0.15,  # Stop-loss point: base_price * (1 - alarm_percentage_min)
    "alarm_percentage_max": 0.15  # Revenue point: base_price * (1 + alarm_percentage_max)
  },
]
```
### Command
```shell
docker run --rm \
    vicalloy/magpie:latest \
    python -m magpie -h
```

```shell
usage: __main__.py [-h] -r RULE [--bark-token BARK_TOKEN] [--tg-token TG_TOKEN] [--tg-chat-id TG_CHAT_ID] [-d {qq,tencent,sina}] [-b ADDRESS] [-p PORT] [{check,server}]

positional arguments:
  {check,server}        run http server or check threshold(default: check)

options:
  -h, --help            show this help message and exit
  -r RULE, --rule RULE  rules(json file)
  --bark-token BARK_TOKEN
  --tg-token TG_TOKEN   telegram token
  --tg-chat-id TG_CHAT_ID
                        telegram chat id
  -d {qq,tencent,sina}, --datasource {qq,tencent,sina}
                        datasource(default: qq)
  -b ADDRESS, --bind ADDRESS
                        bind to this address (default: all interfaces)
  -p PORT, --port PORT  bind to this port (default: 8000)
```


### Start the web server

```shell
docker run --rm \
    -v `pwd`/rules.json:/app/rules.json \
    -p 8000:8000 vicalloy/magpie:latest \
    python -m magpie server -r ./rules.json
```

Access the website `http://localhost:8000/`.

### Check the stock price

```shell
docker run --rm \
    -v `pwd`/rules.json:/app/rules.json \
    vicalloy/magpie:latest \
    python -m magpie check -r ./rules.json \
    --datasource qq \
    --bark-token $(bark-token) \
    --tg-token $(tg-token) \
    --tg-chat-id $(tg-chat-id)
```

You can set up a `crontab` to perform stock price checks regularly.

**NOTE**

- Using [Bark](https://github.com/Finb/Bark/blob/master/README.en.md)
  - Please install the `Bark` client on your iPhone and obtain the corresponding `Token`.
- Using [Telegram](https://telegram.org/)
  - [Create a bot and obtain your bot token](https://core.telegram.org/bots/tutorial#obtain-your-bot-token)
  - Create a group, add the bot to the group, and then obtain the `chat id`.
    - ex: https://web.telegram.org/a/#-1045009696  `-1045009696` is the `chat id`.

```
10 9,10,11,12,13,14 * * * sudo docker run ....
```
