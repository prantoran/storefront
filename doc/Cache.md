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


```bash
docker ps
docker exec -it 0aeee redis-cli
```
```redis-cli
127.0.0.1:6379> select 2
OK
keys *
1) ":1:httpbin_result"
127.0.0.1:6379[2]> del :1:httpbin_result
(integer) 1
127.0.0.1:6379[2]> keys *
(empty array)
127.0.0.1:6379[2]> 
127.0.0.1:6379[2]> flushall
OK
```
- Redis db have numbers

- [django-redis](https://github.com/jazzband/django-redis)
```bash
python -m pip install python-redis django_redis
```
