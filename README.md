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

## Testing

### Tests

Aka unit tests:
```bash
python3 mysite/manage.py test blog.tests
```

Acceptance tests (selenium):
```bash
python3 mysite/manage.py test functional_tests
```

### Syntax Validation

```bash
python3 -m pylint mysite/blog/ mysite/functional_tests
```
