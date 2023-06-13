[中文](./README.cn.md)

# Magpie

A stock tool. Set stop-loss and revenue points for stocks, 
and initiate message pushes when stop-loss or revenue points are reached. 

Provides a simple web server for viewing the current prices of relevant stocks.

Note:

- Currently only supports push notifications using [Bark](https://github.com/Finb/Bark/blob/master/README.en.md).
- Please install the `Bark` client on your iPhone and obtain the corresponding `Token`.

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
    magpie:latest \
    python -m magpie check -r ./rules.json \
    --datasource qq --bark-token $(token)
```

You can set up a `crontab` to perform stock price checks regularly.

```
10 9,10,11,12,13,14 * * * sudo docker run ....
```
