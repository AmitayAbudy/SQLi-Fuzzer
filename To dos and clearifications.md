# To dos and clearifications
This file is to keep track with my to dos and to clearify the intention of each file

## To Do's
* Fix the sql injection string creator at blind_sql_injection.py
* Combine the usage of blind_sql_injection.py with check_website.py
* Add more info about the project (why, how, what) in readme.md

* Add sql commands
* Check the time to run

## Files

### fuzzer.py
This file is in charge of handling the connection with the wesite.
It check for input tags and sends string to the website, and checks the response time

### sql_creator.py
This file is incharge of making the sql injection test cases.
It uses grades for each character to make better randomized string to check.
The gardes are updated after finding working strings.

### sharpener.py
This file is part of the training system for blind_sql_injection.py.
It randomizes string to in order to find more working strings to grade more characters

### sql_bank.txt
This file containts known sql injection strings to use to train blind_sql_injection.py