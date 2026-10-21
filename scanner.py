
import json
import os
import urllib.request
from datetime import datetime, timezone

URL = (
    "https://api.geckoterminal.com/api/v2/"
    "networks/base/new_pools?page=1"
)

os.makedirs("data", exist_ok=True)

try:
    request = urllib.request.Request(
        URL,
        headers={"Accept": "application/json"}
    )

    with urllib.request.urlopen(request, timeout=30) as response:
        payload = json.loads(response.read().decode("utf-8"))

    pools = []

    for item in payload.get("data", []):
        attrs = item.get("attributes", {})
        pools.append({
            "name": attrs.get("name"),
            "address": attrs.get("address"),
            "created_at": attrs.get("pool_created_at"),
            "price_usd": attrs.get("base_token_price_usd"),
            "liquidity_usd": attrs.get("reserve_in_usd"),
            "volume_24h_usd": (
                attrs.get("volume_usd", {}).get("h24")
            ),
            "price_change_24h": (
                attrs.get("price_change_percentage", {}).get("h24")
            ),
            "url": (
                "https://www.geckoterminal.com/base/pools/"
                + str(attrs.get("address", ""))
            )
        })

    result = {
        "updated_at": datetime.now(timezone.utc).isoformat(),
        "network": "Base",
        "count": len(pools),
        "pools": pools
    }

    with open("data/new-pools.json", "w", encoding="utf-8") as file:
        json.dump(result, file, ensure_ascii=False, indent=2)

    print(f"Búsqueda completada: {len(pools)} pares encontrados.")
    print("Resultados guardados en data/new-pools.json")

except Exception as error:
    print(f"Error al consultar los datos: {error}")
    raise
