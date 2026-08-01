# About the tests

I'm using only the unittest module for a zero-dependency setup.
To run the tests locally, make sure you're in the root of this repository (not /tests) and run:
```
python3 -m unittest discover -s tests -p "test_*.py"
```
Or for a specific test simply:
```
python3 tests/my_test.py
```

Notes:
- Test files must be named "test_*.py"