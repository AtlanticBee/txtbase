# Notes on Tests

The unit tests use the built-in module "unittest".

To write a unit test:
- create a test file in this directory in the same structure as in the main code
- make sure the test file is called test_X where X is the equivalent main code filename
- write a class containing the setUp, tearDown and test methods

To run them, use this commmand from the project root:
`python3 -m unittest disover`

To enable imports without collisions, there is an `__init__.py` file in this directory.

Note: UnitTest creates a new instance of the Test class you've written for each of its method called `test_`.

The setUp and tearDown methods are automatically looked for when you create your Test class (which inherits from the unittest class). The original method from the parent does nothing (it just runs `pass`) so you're overriding its predefined method for what to do at startup and teardown.

We need to pass `self` to the setup and teardown functions so that the instance gets its own setup and teardown, rather than it belonging to the class.