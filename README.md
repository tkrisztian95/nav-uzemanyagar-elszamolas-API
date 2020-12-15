# NAV üzemanyagár elszámolás API 
## Hobbi Python projekt
### Leírás
A NAV a weboldalán https://www.nav.gov.hu/ nyilvánosan  közzéteszi a tárgyhónapban a fogyasztási norma szerinti üzemanyagköltség-elszámolással kapcsolatosan alkalmazható üzemanyagárat. Ez a program az innen származó táblázatok tartalmát olvassa és biztosít egy program interfészt (API) az információ lekérdezéshez.

[Közlemény az üzemanyagárakról](https://www.nav.gov.hu/nav/szolgaltatasok/uzemanyag/uzemanyagarak/uzemanyagar.html)

# (EN)
This service provides a specific API to get information from the open data source https://www.nav.gov.hu/ site about fuel cost accounting.

## Tech stack

- Python with Flask web framework
- Redis for caching
- pip:
    - flask
    - requests
    - beautifulsoup4
    - pytest
    - redis

## How to run
1. Install requirements with command: `pip install -r requirements`
2. Step into `app` directory with command: `cd /src/app`
3. Start Flask app with command: `flask run`

### APIs
|Path|Description|Params|
|--|--|--|
|/api| Root (list all API routes)||
|/api/nav/uzemanyagarak/{year}| Returns data by year| year - Possible values: 2020, 2019
|/api/nav/uzemanyagarak/{year}/{month} |Returns data by year and specific month |year - Possible values: 2020, 2019  month - Possible values (in HUN): január, február,.. |

### Examples
GET: http://127.0.0.1:5000/api
```
{
    "data": null,
    "links": {
        "self": "http://localhost:5000/api",
        "uzemanyagarak": "http://localhost:5000/api/nav/uzemanyagarak/{year}/{month}"
},
    "meta": {
        "author": "Tóth Krisztián Gyula",
        "source": "https://www.nav.gov.hu/"
    }
}
```
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
    ],
    "meta": {
        "author": "Tóth Krisztián Gyula",
        "source": "https://www.nav.gov.hu/nav/szolgaltatasok/uzemanyag/uzemanyagarak/uzemanyagar.html",
        "total": 12
    }
}
```

GET: http://127.0.0.1:5000/api/nav/uzemanyagarak/2020/m%C3%A1rcius
```
{
    "data": [
        {
            "benzin": "390",
            "diesel": "406",
            "lpg": "256",
            "mixed": "427",
            "month": "március"
        }
    ],
    "meta": {
        "author": "Tóth Krisztián Gyula",
        "source": "https://www.nav.gov.hu/nav/szolgaltatasok/uzemanyag/uzemanyagarak/uzemanyagar.html",
        "total": 1
    }
}
```

## How to test
- Run tests with command: `pytest`
    - Use the `-s` switch disables per-test capturing 

## How to use Redis
- Use command to connect via telnet interactive protocol: `telnet redis 6379`
- To follow/debug whats happening send the `montior` command after connecting. (Gives you ability to see all the requests processed by the server)

See command reference: https://redis.io/commands

**Example:**
```
$ /workspace# telnet redis 6379
Trying 172.19.0.2...
Connected to redis.
Escape character is '^]'.
MONITOR
+OK
^C //<- Hit CTRL+C to stop a MONITOR stream

// Use command 'SET' with key (hello) to hold the string value "my string value".
// Should return 'OK' if SET was executed correctly
SET hello "my string value"
+1607894952.890850 [0 172.19.0.3:38230] "SET" "hello" "my string value"
+OK

// Get the value of key (hello). 
// Should return "my string value"
GET hello
+1607894960.312599 [0 172.19.0.3:38230] "GET" "hello"
$5
my string value

quit // Type 'quit' to exit and push 'ENTER'
```

Pros over the application in-memory caches:
- App has smaller memory footprint
- Even if the app was restarted or redeployed the data in Redis still available and can be returned immediately
- Multiple instances of the app can use the same cache to serve request from stored data 
- Many Cache eviction strategies, [see more](https://redis.io/topics/lru-cache) (for TTL use `volatile-ttl`)

Cons:
- SPOF - Single point of Failure, if the Redis server is down the caching will be unavailable

---
# TODO's:
- [X] Implement get data from archived years
- [X] Cache crawled content 
- [X] Auto evict cache after 1 min
- [X] Error handling (unified api error response)
- [X] Add meta to response model with some info - https://jsonapi.org/format/#document-meta
- [ ] Add support for sorting - https://jsonapi.org/format/#fetching-sorting 
- [X] Write some tests - https://code.visualstudio.com/docs/python/testing
- [ ] Add Dockerfile 
- [X] Introduce Redis for caching - https://realpython.com/python-redis/
- [X] Add better configuration possibilites - https://hackersandslackers.com/configure-flask-applications/ 
- [X] Add seprated config for dev and prod (should be possible to configure different setups, e.g.: app caches to be in use during test run vs in prod use Redis)
- [ ] Add Docker compose (redis + app image)
- [ ] Add K8s stack, and scale up app instances 
- [ ] Setup Travis CI linting and build jobs
- [ ] Add badges: build, coverage



