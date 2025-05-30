test-all:
	pytest -vs --tb=short --disable-warnings --maxfail=3 --color=yes unit_tests.py sys_test.py

unit:
	pytest -vs --tb=short --disable-warnings --maxfail=3 --color=yes -m "not system" unit_tests.py

sys:
	pytest -vs --tb=short --disable-warnings --maxfail=3 --color=yes -m "system" sys_test.py

coverage-all:
	coverage run -m pytest -vs --tb=short --disable-warnings --maxfail=3 --color=yes unit_tests.py sys_test.py
	coverage report
	coverage html