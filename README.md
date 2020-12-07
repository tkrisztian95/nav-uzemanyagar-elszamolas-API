# NAV üzemanyagár elszámolás API
A NAV a weboldalán https://www.nav.gov.hu/ nyilvánosan  közzéteszi a tárgyhónapban a fogyasztási norma szerinti üzemanyagköltség-elszámolással kapcsolatosan alkalmazható üzemanyagárat. Ez a program az innen származó táblázatok tartalmát olvassa és biztosít egy program interfészt (API) az információ lekérdezéshez.

[Közlemény az üzemanyagárakról](https://www.nav.gov.hu/nav/szolgaltatasok/uzemanyag/uzemanyagarak/uzemanyagar.html)

# (EN)
---
This service provides a specific API to get information from the open data source https://www.nav.gov.hu/ site about fuel cost accounting.

## How to run
- Install requirements with command: `pip install -r requirements`
- Start Flask app with command: `flask run`

### APIs
- /api
- /api/nav/uzemanyagarak/{year}
- /api/nav/uzemanyagarak/{year}/{month} 

### Examples
GET: http://127.0.0.1:5000/api/nav/uzemanyagarak/2020
```
{
    "data": [
        {
            "benzin": "364",
            "diesel": "372",
            "lpg": "247",
            "mixed": "401",
            "month": "december"
        },
        {
            "benzin": "378",
            "diesel": "369",
            "lpg": "235",
            "mixed": "415",
            "month": "november"
        },
        ...
    ]
}
```

GET: http://127.0.0.1:5000/api/nav/uzemanyagarak/2020/m%C3%A1rcius
```
{
    "data": {
        "benzin": "390",
        "diesel": "406",
        "lpg": "256",
        "mixed": "427",
        "month": "március"
    }
}
```

# TODO:
- [X] Implement get data from archived years
- [ ] Cache crawled content up to 5min
- [X] Error handling (unified api error response)
- [ ] Write some tests



