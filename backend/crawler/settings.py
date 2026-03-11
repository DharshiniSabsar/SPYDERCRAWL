# Scrapy settings for crawler project
# -----------------------------------

BOT_NAME = "crawler"

# Spider modules
SPIDER_MODULES = ["crawler.spiders"]
NEWSPIDER_MODULE = "crawler.spiders"

# Do not obey robots.txt (intentional for research crawling)
ROBOTSTXT_OBEY = False

# Identify responsibly
USER_AGENT = (
    "SpyderCrawl/1.0 "
    "(research crawler; contact: security-research@localhost)"
)

# Concurrency & performance
CONCURRENT_REQUESTS = 16
DOWNLOAD_DELAY = 1
RANDOMIZE_DOWNLOAD_DELAY = True

# Disable cookies (privacy + performance)
COOKIES_ENABLED = False

# Telnet console (disable for security)
TELNETCONSOLE_ENABLED = False

# Default request headers
DEFAULT_REQUEST_HEADERS = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en",
}

# Pipelines
ITEM_PIPELINES = {
    "crawler.pipelines.MongoPipeline": 300,
}

# Logging
LOG_ENABLED = True
LOG_LEVEL = "INFO"

# Encoding
FEED_EXPORT_ENCODING = "utf-8"

# AutoThrottle (recommended)
AUTOTHROTTLE_ENABLED = True
AUTOTHROTTLE_START_DELAY = 1
AUTOTHROTTLE_MAX_DELAY = 10
AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0

# Retry handling
RETRY_ENABLED = True
RETRY_TIMES = 3

# Timeout protection
DOWNLOAD_TIMEOUT = 30

# Request fingerprinting (Scrapy 2.7+)
REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"

# Twisted reactor (async safe)
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"

# Future-proofing (Scrapy 2.14+)
FEED_EXPORT_ENCODING = "utf-8"

