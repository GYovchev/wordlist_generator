# Wordlist generator

## Description

This is a Python 3 program that extracts a list of words in your language from websites of your choice. It will start from a link you provide and will continue for all links that are matched by a regex (of your choice) or start with a prefix (again choosen by you).

## How to use

To run the program you first need to install all dependencies

```
pip3 install -r requirements.txt
```

Then you can run it using either

```
python3 main.py --start_url {{THE_START_URL}} --url_prefix {{URL_PREFIX}} --depth {{DEPTH_OF_CRAWLING}}
```

or

```
python3 main.py
```

If you use the second command you will be prompted to enter the parameters.