
Test behaviours, not implementations

# Test Frameworks

unittest

pytest

# Pytest

```bash
python3 -m pip install pytest pytest-django # Refactor with poetry
```


Every test will have 3 parts:
- Arrange 
- Act
- Assert


Run all tests with "anonymous" in the tests
```bash
pytest -k anonymous
```

# Continuous testing

```
python3 -m pip install pytest-watch
```

command: 
```bash
ptw
```
- Once executed, listens for changes and reruns unit tests

# Fixtures

Putting common code in `conftest.py` which are automatically loaded for each test.

These reusable functions are called fixtures.

# Initialize objects with random values

```python
from model_bakery import baker
...
    collection = baker.make(Collection)
```

# Test DB

Pytest creates a temporary separate DB with `test_` prefix, 
i.e. test_storefront, where all data modified during test runs are stored.

The temporary DB is deleted once all the tests are executed. 