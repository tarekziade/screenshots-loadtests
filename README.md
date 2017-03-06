# Page Shot Load Tests

[![Build Status](https://travis-ci.org/pdehaan/pageshot-loadtests.svg?branch=master)](https://travis-ci.org/pdehaan/pageshot-loadtests)

Async [**Page Shot**](https://github.com/mozilla-services/pageshot) load tests using [**molotov**](https://github.com/loads/molotov).

## Requirements:

- [Python 3.5+](https://www.python.org/downloads/)

## Installation:

```sh
$ virtualenv venv -p python3
$ source ./venv/bin/activate
$ pip install -r requirements.txt
```

## Usage:

```sh
$ molotov -h

$ molotov -cvv --max-runs 1
```
