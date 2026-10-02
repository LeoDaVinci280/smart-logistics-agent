from src.tools import (
    calculate_duty_and_currency_tool,
    db_transport_tool
)

result = calculate_duty_and_currency_tool(
    amount_usd=1000,
    target_currency="AUD"
)

print(result)

shipments = db_transport_tool(
    action="list",
    payload={}
)

print(shipments)