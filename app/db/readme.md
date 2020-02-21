# which `dbconnect.py` to use?

There are two `dbconnect.py` programs, `dbconnect_local.py` and `dbconnect_remote.py`. One connects in a local environment, the other in a heroku environment.

To run `bigfatstats` locally,

1. copy `dbconnect_local.py`
2. change its name to `dbconnect.py`

When whatever changes are necessary have been made and it's time to return to the heroku setup,

1. copy `dbconnect_remote.py`
2. change its name to `dbconnect.py`
