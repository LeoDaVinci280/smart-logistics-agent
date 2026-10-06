from src.tools import db_transport_tool


print(
    db_transport_tool(
        action="count",
        payload={}
    )
)

print(
    db_transport_tool(
        action="average_cost",
        payload={}
    )
)

print(
    db_transport_tool(
        action="list_countries",
        payload={}
    )
)

print(
    db_transport_tool(
        action="list_transport_modes",
        payload={}
    )
)