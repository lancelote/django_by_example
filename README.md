[![Requirements Status](https://requires.io/github/lancelote/django_by_example/requirements.svg?branch=master)](https://requires.io/github/lancelote/django_by_example/requirements/?branch=master)
[![Build Status](https://travis-ci.org/lancelote/django_by_example.svg)](https://travis-ci.org/lancelote/django_by_example)

# django_by_example

Code for [Django by Example book](http://www.amazon.com/Django-Example-Antonio-Mele/dp/1784391913) by Antonio Mele

## My Progress

- [x] Chapter 1: Building a Blog Application
- [ ] Chapter 2: Enhancing Your Blog with Advanced Features
- [ ] Chapter 3: Extending Your Blog Application
- [ ] Chapter 4: Building a Social Website
- [ ] Chapter 5: Sharing Content in Your Website
- [ ] Chapter 6: Tracking User Actions
- [ ] Chapter 7: Building an Online Shop
- [ ] Chapter 8: Managing Payments and Orders
- [ ] Chapter 9: Extending Your Shop
- [ ] Chapter 10: Building an e-Learning Platform
- [ ] Chapter 11: Caching Content
- [ ] Chapter 12: Building an API

## Environment Variables

All sensitive data (user names, passwords, Django secret key and etc) should be stored via environment variables
and will be load by `os.environ`. Any missing values will raise `ImproperlyConfigured` exception. List of required
environment variables:

| Variable | Value |
| --- | --- |
| `SECRET_KEY` | Django secret key |
| `EMAIL_HOST_USER` | Google email account name to send mails from django (example@gmail.com) |
| `EMAIL_HOST_PASSWORD` | Google account password or application specific password for two factor authentication |

I use two ways to set environment variables: via Pycharm (my primary IDE for development) and via `virtualenvwrapper`
scripts.

### Setting Environment Variables with Pycharm

There're few places where you can specify environment variables:

 1. Run Configurations
 2. Python and Django console
 3. manage.py Pycharm settings

#### Run Configurations

This allows you to run development server, tests and so on via Pycharm `Run...` command without `ImproperlyConfigured`:

 - Open *Run Configuration* window - *Run* menu - *Edit Configurations...* or `Alt + Shift + F10` - `0`
 - Add *Django Server* (for example) via `Alt + Insert`
 - Find *Environment Variable* block and click `...` button to the right
 - Here you can specify names and values of the desired environment variables, note *copy* and *paste* buttons, they
   can be pretty useful

#### Python and Django Console

This will prevent `ImproperlyConfigured` upon opening Python console:

 - Open *File* menu - *Settings* - *Build, Execution, Deployment* - *Console*
 - There you have Django and Python consoles, you can specify any environment variable you want to load with them

#### manage.py Pycharm Settings

This will prevent `ImproperlyConfigured` exception upon opening manage.py Pycharm console (`Ctrl + Shift + R`):

 - *File* - *Settings* - *Languages & Frameworks* - *Django* - *Environment variables*

## Setting Environment Variables with `virtualenvwrapper` Scripts

`virtualenvwrapper` provides really useful bash scripts, that will be executed upon virtualenv start, stop and so on.
They are easy to use, we just need to export our environment variables to the global space right after virtualenv
activation and to unset them upon virtualenv deactivation:

 - `workon <your_virtualenv_name>`
 - `cdvirtualenv` - to `cd` virtualenv folder (you can do it manually for sure)
 - `cd bin` - here we have out bash scripts
 - Add to `postactivate` this line: `export ENV_NAME="env_value"` where `ENV_NAME` is desired variable name, and
   `end_value` - it's value, copy this line if you need to setup few variables
 - Add to `predeactivate` this line (or lines): `unset ENV_NAME` for each `ENV_NAME` you add to `postactivate`

## Requirements

### Installation

- Python 3+
- Virtualenv usage is recommended
- To install requirements: `pip install -r requirements.txt` or `pip-sync` (`pip-tools` is required)

### Update

- Install `pip-tools`
- Update `requirements.in`
- Compile `requirements.txt` by running `pip-compile requirements.in`

## Testing

### Tests

All integration tests:
```bash
python3 mysite/manage.py test blog.tests
```

Acceptance tests (selenium, Firefox is required), will take a while (but pretty fun to watch):
```bash
python3 mysite/manage.py test functional_tests
```

> PLEASE NOTE: My acceptance tests are rather fragile and can fail due to some silly causes depends on OS and so on.
> If it's your case - consider to [report an issue](https://github.com/lancelote/django_by_example/issues/new),
> I would love to fix it.

### Syntax Validation

```bash
python3 -m pylint mysite/blog/ mysite/functional_tests/
```

## Misc

If you have any questions - feel free to ask me, I would love to help fellow learner! The book is awesome, but I
found few typos/misleading notes so can probably you.