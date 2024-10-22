config = {
    "api": {
        "base_url": "https://data.elexon.co.uk/bmrs/api/v1/balancing/settlement/system-prices/",
        "format": "json",
        "columns": [
            "settlementDate",
            "systemSellPrice",
            "systemBuyPrice",
            "netImbalanceVolume",
            "startTime",
            "settlementPeriod"
        ],
        "data_types": {
            "settlementDate": "str",
            "systemSellPrice": "decimal",
            "systemBuyPrice": "decimal",
            "netImbalanceVolume": "decimal",
            "startTime": "str",
            "settlementPeriod": "int"
        }
    }
}
