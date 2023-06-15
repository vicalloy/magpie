from magpie.core import Rule, check_threshold


def test_rule():
    data = {
        "stock_code": "sh000001",
        "stock_name": "上证指数",
        "base_price": 3200,
    }
    rule = Rule.from_dict(data)
    assert rule.alarm_price_max == 3200 * (1 + 0.15)
    data |= {
        "alarm_percentage_min": 0.15,
        "alarm_percentage_max": 1.0,
    }
    rule = Rule.from_dict(data)
    assert rule.alarm_price_max == 3200 * 2
    data |= {
        "alarm_price_min": 3000,
        "alarm_price_max": 3400,
    }
    rule = Rule.from_dict(data)
    assert rule.alarm_price_min == 3000
    assert rule.alarm_price_max == 3400


def test_check_threshold():
    _rules = {
        "sh000001": Rule("sh000001", "上证指数", 3200).update(3019, 3201),
    }

    check_threshold(_rules, send_msg_funcs=[print])
