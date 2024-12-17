# Brokers

- Redis (in-memory data store)
- RabbitMQ (real, enterprise-grade broker)

# Redis
- Cache
- Message broker

```bash
docker run -d -p 6379:6379 redis
```

```bash
python -m pip install redis
```

# Celery

```bash
python -m pip install celery
```

## Start Celery worker process

```bash
celery -A storefront worker --loglevel=info
```