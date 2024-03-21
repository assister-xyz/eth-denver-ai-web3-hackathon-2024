import redis

# Replace these with your ElastiCache cluster endpoint and port
elasticache_endpoint = 'https://ethdenver.nz3b5u.0001.use1.cache.amazonaws.com'
elasticache_port = 6379  # Default Redis port, change if yours is different

# Connect to ElastiCache Redis
try:
    r = redis.Redis(host=elasticache_endpoint, port=elasticache_port)
    
    # Example command to check the connection
    print(r.ping())  # Should print True if connection is successful
except redis.ConnectionError:
    print("Failed to connect to ElastiCache Redis instance.")

