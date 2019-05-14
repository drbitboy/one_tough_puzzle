

test:
	python otp.py --debug | diff -bw test_output.txt -
