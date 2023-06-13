# Magpie

股票工具。设置股票的止损点和营收点，在到达止损点或营收点时发起消息推送。提供一个简易点web服务器用于查看相关股票的当前价格。

注：

- 目前只支持使用 [Bark](https://github.com/Finb/Bark/blob/master/README.en.md) 推送。
- 请在 iPhone 上安装 `Bark` 客户端，并获取对应的 `Token` 。

## 用法

### 编辑规则文件

提醒规则使用 `Json` 格式进行描述。编辑规则并保存为文件 `rule.json` 。

```
[
  {
    "stock_code": "sh000001",
    "stock_name": "上证指数",
    "base_price": 3200,  # 基准价格，用于计算涨幅
    "alarm_price_min": 3100,  # 止损点
    "alarm_price_max": 3400  # 营收点
  },
  {
    "stock_code": "sz000333",
    "stock_name": "美的",
    "base_price": 54,
    "alarm_percentage_min": 0.15,  # 止损点 base_price * (1 - alarm_percentage_min)
    "alarm_percentage_max": 0.15  # 营收点 base_price * (1 + alarm_percentage_max)
  },
]
```
### 启动 Web 服务器

```shell
docker run --rm \
    -v `pwd`/rules.json:/app/rules.json \
    -p 8000:8000 vicalloy/magpie:latest \
    python -m magpie server -r ./rules.json
```

在浏览器中访问网址 `http://localhost:8000/` 。

### 检查股价

```shell
docker run --rm \
    -v `pwd`/rules.json:/app/rules.json \
    magpie:latest \
    python -m magpie check -r ./rules.json \
    --datasource qq --bark-token $(token)
```

可以通过设置 `crontab` 的方式定时执行股价的检查。

```
10 9,10,11,12,13,14 * * * sudo docker run ....
```
