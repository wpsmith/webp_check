from wp.command import WPCommand


# Flushes the object cache.
# For WordPress multisite instances using a persistent object cache,
# flushing the object cache will typically flush the cache for all sites.
# Beware of the performance impact when flushing the object cache in production.
# Errors if the object cache can’t be flushed.
# wp cache flush
# Success: The cache was flushed.
class CacheFlush(WPCommand):
    command = ['cache', 'flush']

    def __init__(self, **args):
        super().__init__(**args)

    def params(self):
        return []
