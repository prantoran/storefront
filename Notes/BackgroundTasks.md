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




# Periodic tasks

- Generating periodic report
- Sending emails
- Running maintenance

## Celery Beat

```bash
celery -A storefront beat
```



## Monitoring Celery tasks

```bash
python3 -m pip install flower
```

Start Flower process using Celery

```bash
celery -A storefront flower
```

output:
```aiignore
[I 250113 07:03:37 command:168] Visit me at http://0.0.0.0:5555
[I 250113 07:03:37 command:176] Broker: redis://localhost:6379/1
[I 250113 07:03:37 command:177] Registered tasks: 
    ['celery.accumulate',
     'celery.backend_cleanup',
     'celery.chain',
     'celery.chord',
     'celery.chord_unlock',
     'celery.chunks',
     'celery.group',
     'celery.map',
     'celery.starmap',
     'playground.tasks.notify_customers']
[I 250113 07:03:37 mixins:228] Connected to redis://localhost:6379/1
```