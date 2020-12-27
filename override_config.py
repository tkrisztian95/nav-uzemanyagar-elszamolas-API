"""Override - Flask configuration."""

# add UTF-8 support
JSON_AS_ASCII = False
NO_CACHE = False
USE_REDIS_CACHE = True
REDIS_HOST_URL = "cache"
USE_IN_MEMORY_CACHE = False