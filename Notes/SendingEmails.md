## SMTP

Simple mail transfer protocol

Fake SMTP server: [smtp4dev](https://github.com/rnwood/smtp4dev)

```bash
docker run --rm -it -p 5000:80 -p 2525:25 rnwood/smtp4dev
```

Dashboard: http://localhost:5000/

## Email backends

- SMTP (default)
- Console
- File
- Locmem (local memory)
- Dummy (does nothing)