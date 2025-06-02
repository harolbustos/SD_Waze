from collections import OrderedDict, defaultdict

class SistemaCache:
    def __init__(self, max_size=100, policy="LRU"):
        self.max_size = max_size
        self.policy = policy.upper()
        self.cache = OrderedDict() if self.policy == "LRU" else {}
        self.access_count = defaultdict(int) if self.policy == "LFU" else None

        self.hits = 0
        self.misses = 0
        self.total_requests = 0

    def get(self, key):
        self.total_requests += 1
        if key in self.cache:
            self.hits += 1
            if self.policy == "LRU":
                self.cache.move_to_end(key)
            elif self.policy == "LFU":
                self.access_count[key] += 1
            return self.cache[key]
        else:
            self.misses += 1
            return None

    def put(self, key, value):
        if key in self.cache:
            self.cache[key] = value
            if self.policy == "LRU":
                self.cache.move_to_end(key)
            elif self.policy == "LFU":
                self.access_count[key] += 1
        else:
            if len(self.cache) >= self.max_size:
                self._evict()
            self.cache[key] = value
            if self.policy == "LFU":
                self.access_count[key] = 1

    def _evict(self):
        if self.policy == "LRU":
            oldest = next(iter(self.cache))
            del self.cache[oldest]
        elif self.policy == "LFU":
            min_count = min(self.access_count.values())
            lfu_key = None
            for key, count in self.access_count.items():
                if count == min_count and key in self.cache:
                    lfu_key = key
                    break
            if lfu_key:
                del self.cache[lfu_key]
                del self.access_count[lfu_key]

    def metrics(self):
        hit_rate = (self.hits / self.total_requests * 100) if self.total_requests > 0 else 0
        return {
            "hits": self.hits,
            "misses": self.misses,
            "total_requests": self.total_requests,
            "hit_rate": round(hit_rate, 2),
            "cache_size": len(self.cache),
            "max_size": self.max_size,
            "policy": self.policy
        }
