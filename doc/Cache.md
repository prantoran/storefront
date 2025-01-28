Cache backends:
- Local/In-memory (default)
- Redis (production)
- Memcached (production)
- Database
- File-based
- Distributed

```bash
docker run -d -p 6379:6379 redis
```

- [django-redis](https://github.com/jazzband/django-redis)
```bash
python -m pip install python-redis
```
