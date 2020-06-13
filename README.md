# SQLi Fuzzer

Hello! This is my final project for high school Cyber Security Class.
This is a simple SQLi fuzzer that helps you detetct payloads in your web app or server.

### Plugins
This project needs the following plugings installed:
* Requests
* Treelib
* Beautiful Soup


### How to use:
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
