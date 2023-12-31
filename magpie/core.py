import json
from collections.abc import Callable, Iterable
from dataclasses import dataclass

import easyquotation

_quotation = easyquotation.use("qq")


def set_datasource(datasource: str):
    global _quotation
    _quotation = easyquotation.use(datasource)


@dataclass
class Rule:
    stock_code: str
    stock_name: str
    base_price: float
    alarm_percentage_min: float = 0.15
    alarm_percentage_max: float = 0.15

    @property
    def alarm_price_max(self):
        return self.base_price * (1 + self.alarm_percentage_max)

    @alarm_price_max.setter
    def alarm_price_max(self, val: float):
        self.alarm_percentage_max = (val / self.base_price) - 1

    @property
    def alarm_price_min(self):
        return self.base_price * (1 - self.alarm_percentage_min)

    @alarm_price_min.setter
    def alarm_price_min(self, val: float):
        self.alarm_percentage_min = 1 - (val / self.base_price)

    def update(self, alarm_price_min: float, alarm_price_max: float):
        self.alarm_price_max = alarm_price_max
        self.alarm_price_min = alarm_price_min
        return self

    @classmethod
    def from_dict(cls, data: dict[str, str | float]):
        alarm_price_min = data.pop("alarm_price_min", None)
        alarm_price_max = data.pop("alarm_price_max", None)
        r = Rule(**data)  # type: ignore
        if alarm_price_max is not None:
            r.alarm_price_max = alarm_price_max
        if alarm_price_min is not None:
            r.alarm_price_min = alarm_price_min
        return r


@dataclass
class Stock:
    rule: Rule
    price: float

    def is_should_alarm(self):
        return (
            self.price > self.rule.alarm_price_max
            or self.price < self.rule.alarm_price_min
        )

    def check(self, send_msg_funcs: Iterable[Callable]):
        if self.is_should_alarm():
            for send_msg_func in send_msg_funcs:
                send_msg_func(str(self))

    def __str__(self):
        percentage = f"{((self.price / self.rule.base_price) - 1) * 100:.1f}%"
        return (
            f"{self.rule.stock_code} {self.rule.stock_name:\u3000>4} "
            f"base price: {self.rule.base_price:>7.2f} "
            f"current price: {self.price:>7.2f}"
            f"{percentage:>6}"
        )


def load_rules(fn: str) -> dict[str, Rule]:
    with open(fn) as f:
        return {data["stock_code"]: Rule.from_dict(data) for data in json.load(f)}


def check_threshold(rules: dict[str, Rule], send_msg_funcs: Iterable[Callable]) -> str:
    stock_info_dict = _quotation.stocks(list(rules.keys()), prefix=True)
    output = []
    for stock_code, rule in rules.items():
        price = stock_info_dict[stock_code]["now"]
        stock = Stock(rule, price)
        stock.check(send_msg_funcs=send_msg_funcs)
        output.append(str(stock))
    return "\r\n".join(output)
