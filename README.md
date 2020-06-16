

# SQLi Fuzzer

This is my Cyber Security class final project.

The project is a simple SQLi fuzzer that can help you detect sql payloads in your web app or server.
![SQL Injection example](https://miro.medium.com/max/600/1*mTKfq-BXgewrnF8A57TTNw.png)
## Installation:
Opening cmd/Terminal in the project location in the computer and running:

```sh
pip install -r requirements.txt
```

This command will install all the required modules for this project.

### Setting up a test site
In order to check this project legally (At least in Israel) you will need a test site.
For my development and research i used OWASP Bricks Test Site.

[Here](https://sechow.com/bricks/docs/installation.html) you can find the Installation guide for it.

Of curse you can use any test site with this script, this is just my recommendation.

## How to use:
Run the fuzzer.py command

Available parameters:
-    -u URL to check, default my test site "http://localhost/login-1"
-    -b Max total base strings, default 10
-    -t Max tries for string, default 7
-    -f odds file (in json format), default "odds.json"
-    -d debug mode, default False

```sh
python fuzzer.py -u "http://localhost/login-1" -b 10 -t 7 -f "odds.json" -d
```
