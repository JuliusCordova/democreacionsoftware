from stock_unico.smoke import health


def test_health_returns_ok() -> None:
    result = health()
    assert result["status"] == "ok"
    assert result["service"] == "stock-unico"
