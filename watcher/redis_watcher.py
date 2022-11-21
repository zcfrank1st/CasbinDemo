from casbin_redis_watcher import new_watcher, WatcherOptions

class RedisWatcher:
    def __init__(self, fun, host='localhost', port='6379', channel='test') -> None:
        self.option = WatcherOptions()
        self.option.host = host
        self.option.port = port
        self.option.channel = channel
        self.option.optional_update_callback = fun
        self.watcher = new_watcher(self.option)

    def get_watcher(self):
        return self.watcher