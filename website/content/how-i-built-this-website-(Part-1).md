title: How I built this website (Part 1)
date: 2018-07-11
tags: flask, aws, markdown

## Introduction

This series is a step-by-step tutorial for making a website like this one. It includes an introduction to the Flask web framework, an introduction to Markdown (the markup language used to write this post), and also an introduction to hosting websites using Amazon Web Services.

Posts in this series:
1. Flask (you are here)
2. [Introduction to Markdown](/how-i-built-this-website-(Part-2\))
3. [Configuring the Markdown blog](/how-i-built-this-website-(Part-3\))
4. [Amazon Web Services](/how-i-built-this-website-(Part-4\))

This post covers the creation of a minimal Flask-driven website. In Part 3, we'll dive in deeper discuss how to make a website that contains Markdown blog functionality.

## Prerequisites

Before starting, make sure you have the following software management tools installed:
- [pip](https://docs.python.org/2.7/installing/) - A Python package manager.
- [virtualenv](https://realpython.com/python-virtual-environments-a-primer/) - A tool for creating localized Python package installations.
- [npm](https://www.npmjs.com/get-npm) - A JavaScript package manager.
- [bower](https://bower.io/) - A package manager for web projects.

## Flask

### Setting up Flask

[Flask](http://flask.pocoo.org/) is a microframework for Python. Flask is lightweight and highly configurable. One does not need to sift through boilerplate code in order to get a project up and running. To illustrate how quick Flask is, create a new directory and install Flask using pip:

```posh
matt@matt$ mkdir new_project
matt@matt$ cd new_project
matt@matt$ virtualenv venv
matt@matt$ . venv/bin/activate
matt@matt$ pip install flask
matt@matt$ touch run.py
```

Now add the following code to `run.py`:

```python
from flask import Flask
app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"
```

Back in Terminal, enter the following command:

```posh
matt@matt$ python run.py
```

*Et viola*, by entering the URL `localhost:5000` into your favorite browser you will see your "Hello World!". The important thing to note is that Flask uses "routes" to decorate functions. The URL that is accessed determines which Python function in your project gets called, and ultimately what gets served back to the user.

### Configuring a Flask project

Next, clone my [minimal Flask repository](https://github.com/matt-cart/minimal-website-demo) into a new folder.

In the previous example, the website was entirely contained within a single Python script. This is great, but it will struggle to capture some of the complexity and sophistication we hope to implement. The demonstration repository is structed as follows:

```
├── run.py
├── venv/
├── requirements.txt
├── website/
	└── static/
	└── templates/
	└── __init__.py
	└── views.py
```

Let's go through each piece.


#### The `run.py` file

The `run.py` file is ultimately what gets executed in the console to run the development server that we used for our Hello World! example. In that first iteration, we included our main route (also called a "view") in the `run.py` file. As our projet gets more sophisticated, it gets cumbersome to have all of our views in the `run.py` file. These views are all moved to the `views.py` file. Our new `run.py` is quite simple:

```python
from website import app

app.run('0.0.0.0', debug=True)
```

This configuration will make more sense when we eventually configure our Apache web server to create a production-level website.

#### Virtual environment and `requirements.txt`

Following convention, create a virtual environment named `venv` using the steps in the Hello World! example. Make sure you always activate the virtual environment when you start working on this project. 

To install the necessary Python modules for this demo, use the following command:

```posh 
matt@matt$ pip install -r requirements.txt
```

Every time a new module is added to our pip environment, we want to get in the habit of adding it to our `requirements.txt` file:

```posh 
matt@matt$ pip freeze > requirements.txt
```

This makes it easier for you to install your Python environment when moving to a production server.

#### The `website` directory

This directory contains all the content of our website as well as the routing that connect URL paths with the content we wish to deliver.

#### The `static` directory

The `static/` directory contains the static files including CSS files, JavaScript, etc. For this example it will remain rather simple:

```
├── static/
	└── bower.json
	└── bower_components/
```

The `bower.json` file and `bower_components` directory are automatically created when we install packages with bower (and save the history of added packages). Here, I am using Bootstrap v3. To install this packages and automatically create the `bower_components` directory, run the following command while in the `static` directory:

```posh 
matt@matt$ bower install
```

In [Part 3](/how-i-built-this-website-(Part-3\)), we'll discuss adding custom CSS and images to the `static` directory.

#### The `templates` directory

This directory contains all of the HTML files that will be served. Before we get to the blogging components of this website, let's start with two files: `home_page.html` and `layout.html`. A powerful component of Flask (via the [Jinja](http://jinja.pocoo.org/) package) is the ability to create "layouts" that get passed on to each additional web page. In my case, the `layout.html` file allows me to add a universal header and navbar to each page without having to manually add that information to each and every HTML file.

Below is `layout.html`, which demonstrates how to load a CSS file from the `bower_components` directory and also how we allow the layout to be propagated to all future HTML files.

```html
<!DOCTYPE html>
<html lang="en">
    <head>
    	<link rel="stylesheet" href="{{ url_for('static', filename='bower_components/bootstrap/dist/css/bootstrap.css') }}" />
    </head>
    <body>
    	<nav class="navbar navbar-default navbar-fixed-top">
    		<p>I am a navbar</p>
    	</nav>
        <div id="content">
            {% block content %}{% endblock %}
        </div>
    </body>
</html>
```

Take note of the Jinja syntax here. The `url_for()` function inside the double curly brackets `{{ }}` is special Jinja syntax. Before the web page is served, the contents between the curly brackets is changed to the return value of the function. In this case, the return value of the function is the URL for Bootstrap CSS file. 

The `{% block content %}{% endblock %}` snipped is ultimately replaced by the contents of individual HTML files being served.

In `home_page.html` we find the following:

```html
{% extends "layout.html" %}
{% block content %}
	<div class="container-fluid bump-past-nav">
    	<div class="row">
    		<p>I am content</p>
    	</div>
    </div>
{% endblock %}
```

#### The `__init__.py` file

In our `run.py` file we have the line:

```python
from website import app
```

When Python encounters this line it looks for the module `website`, which is really the directory `website`. In order to tell Python that the directory `website` is, in fact, a module for import, we need to add an `__init__.py` file. In many projects, an `__init__.py` file can simply be left blank; it's presence is sufficient. However, in our case, we want to add few lines of important code to this file. These lines will automatically get executed when we try to import from the `website` module:

```python
import os
from flask import Flask

BASE_PATH = os.path.dirname(os.path.realpath(__file__))
app = Flask(__name__, instance_relative_config=True)

from website import views
```

It is in this `__init__.py` file that we create the all important Flask object `app` that gets referenced in our `run.py` file. We could put all of this information in the `run.py` file itself, but when we ultimately want to configure this application to run on a real web server in [Part 4](/how-i-built-this-website-(Part-4)), this setup makes it easier.

#### The `views.py` file

The `views.py` file contains all of the routes we want to have for our website. The root page of any site is the `"/"` route:

```python
@app.route('/')
def index():
    return render_template('home_page.html')
```

The `render_template` function automatically knows to look in the `templates` directory for the HTML file being referenced as an argument (the HTML file, in turn, automatically knows where to find the `layout.html` file).

A key feature of routes is their ability to handle variables. Take this example:

```python
@app.route('/<name>')
def print_name(name):
	return render_template('name.html', name=name)
```

Accessing the URL `localhost:5000/matt` will return a web page that says "matt". Accessing the URL `localhost:5000/stephen` will return a web page that says "stephen". The important thing to note here is that we can pass arbitrary information to a web page based on the information in the URL. Eventually, we will use this to serve specific blog posts specified by the URL.

## Conclusion

A quick recap of Part 1. In this post we covered:
- Package management with pip and bower.
- Setup of a minimal Flask website comprised of a single file.
- Setup of a slightly more complicated website that is structured in a more traditional fashion.
- Basic use of routes to pass information to webpages.
- Basic Jinja syntax.

Proceed to [Part 2](/how-i-built-this-website-(Part-2)) for an introduction to Markdown.


