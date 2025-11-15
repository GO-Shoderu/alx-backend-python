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

---

## Task 1: Parameterize a Unit Test (Exception Cases)

In this task, I added tests to verify that `utils.access_nested_map` raises the correct `KeyError` when the provided path is invalid.

### What I Did
- Implemented `test_access_nested_map_exception` in the `TestAccessNestedMap` class.
- Used `@parameterized.expand` to cover two invalid path scenarios:
  - `nested_map = {}`, `path = ("a",)`
  - `nested_map = {"a": 1}`, `path = ("a", "b")`
- Used `assertRaises` as a context manager to assert that a `KeyError` is raised.
- Verified that the exception message (the missing key) matches the expected value using `context.exception.args[0]`.

### File:
- `test_utils.py`

## Task 2: Mock HTTP Calls for `get_json`

In this task, I wrote unit tests for the `utils.get_json` function without making real HTTP requests.

### What I Did
- Created a `TestGetJson` class inheriting from `unittest.TestCase`.
- Used `@parameterized.expand` to test multiple `(url, payload)` combinations:
  - `test_url = "http://example.com"`, `test_payload = {"payload": True}`
  - `test_url = "http://holberton.io"`, `test_payload = {"payload": False}`
- Used `unittest.mock.patch` to patch `requests.get` so that:
  - It returns a mock response whose `json()` method returns `test_payload`.
- Asserted that:
  - `requests.get` was called exactly once per test with the correct `test_url`.
  - `get_json(test_url)` returned the expected `test_payload`.

### File:
- `test_utils.py`

---

## Task 3: Parameterize and Patch (Memoization)

This task required testing the `memoize` decorator from `utils.py`, ensuring that method results are cached after the first call.

### What I Did

* Added a `TestMemoize` class to `test_utils.py`.
* Defined a simple inner class `TestClass` with:

  * `a_method()` returning `42`.
  * `a_property` decorated with `@memoize`.
* Used `patch.object` to mock `TestClass.a_method` and monitor how many times it gets called.
* Accessed `a_property` twice.
* Asserted that:

  * Both returned values were `42`.
  * `a_method` was called **exactly once** due to memoization.

### File:

* `test_utils.py`

---

## Task 4: Mocking a Property (`_public_repos_url`)

This task required unit testing the private property `GithubOrgClient._public_repos_url` by mocking its dependency (`GithubOrgClient.org`).

### What I Did

* Added `test_public_repos_url` inside `TestGithubOrgClient`.
* Created a mocked payload containing a `repos_url`.
* Used `patch` with `PropertyMock` to mock the `.org` property:

  ```python
  with patch("client.GithubOrgClient.org", new_callable=PropertyMock)
  ```
* Instantiated `GithubOrgClient` and accessed `_public_repos_url`.
* Asserted that:

  * The value returned by `_public_repos_url` matched the mocked `repos_url`.
  * The mocked `.org` property was accessed exactly once.

### File:

* `test_client.py`

---

## Task 5: Test GithubOrgClient.has_license (Parameterized): Test GithubOrgClient.has_license (Parameterized)

This task focused on unit‑testing the `GithubOrgClient.has_license` static method.

### What I Did

* Added a `test_has_license` method using `@parameterized.expand`.
* Tested two cases:

  * Repo with matching license → returns `True`.
  * Repo with non‑matching license → returns `False`.
* Asserted that output matched the expected value.

### File:

* `test_client.py`

---

## Task 6: Integration Test Setup (Fixtures)

In this task, I prepared the integration testing environment for `GithubOrgClient.public_repos`.

### What I Did

* Used `@parameterized_class` to load fixture data from `fixtures.py`:

  * `org_payload`
  * `repos_payload`
  * `expected_repos`
  * `apache2_repos`
* Implemented `setUpClass` to:

  * Patch `requests.get` once for the whole class.
  * Configure `side_effect` so different URLs return the correct fixture payload (`org_payload` vs. `repos_payload`).
* Implemented `tearDownClass` to stop the patcher.

### File:

* `test_client.py`


---

## Task 7: Integration Tests for public_repos

This task required writing integration tests to verify the end‑to‑end behavior of `GithubOrgClient.public_repos`.

### What I Did

#### **test_public_repos**

* Instantiated `GithubOrgClient`.
* Called `public_repos()` with **no license filter**.
* Asserted that the result matched `expected_repos` from fixtures.

#### **test_public_repos_with_license**

* Called `public_repos(license="apache-2.0")`.
* Asserted that the result matched the subset of repos (`apache2_repos`) with that license.

These tests rely on the patched `requests.get` from `setUpClass`, making them true integration tests.

### File:

* `test_client.py`