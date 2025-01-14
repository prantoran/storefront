
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