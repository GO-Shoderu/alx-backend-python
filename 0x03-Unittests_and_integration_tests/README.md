# Unittests and Integration Tests

This project introduces unit testing and integration testing concepts in Python using the built-in `unittest` framework and additional tools such as `parameterized` and `mock`. The goal is to practice writing clean, isolated tests and validating expected behavior for small functions as well as multiple interacting components.

---

## Task 0: Parameterize a Unit Test

In this task, I implemented unit tests for the `utils.access_nested_map` function.

### What I Did

* Created a `TestAccessNestedMap` class inheriting from `unittest.TestCase`.
* Used `@parameterized.expand` to run the same test with multiple input combinations.
* Tested that `access_nested_map` returns the correct values for:

  * `{"a": 1}, ("a",)`
  * `{"a": {"b": 2}}, ("a",)`
  * `{"a": {"b": 2}}, ("a", "b")`
* Ensured the test method body is not longer than two lines, as required.

### File:

* `test_utils.py`
