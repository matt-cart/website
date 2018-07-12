title: How I built this website (Part 1)
date: 2018-07-11
tags: flask, aws, markdown

## Introduction

This post is a step-by-step tutorial for how I made this website. It includes an introduction to the Flask web framework, an introduction to Markdown (the markup language used to write this post), and also an introduction to hosting websites using Amazon Web Services.

Table of Contents:
1. Flask (you are here)
2. [Introduction to Markdown](/how-i-built-this-website-(Part-2\))
3. [Configuring the Markdown blog](/how-i-built-this-website-(Part-3\))
4. [Amazon Web Services](/how-i-built-this-website-(Part-4\))

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

*Et viola*, by entering the URL `localhost:5000` into your favorite browser you will see your "Hello World!". The important thing to note is that Flask uses "routes" to decorate functions. The URL that is accessed determines which Python function in your project gets called, and ultimately what gets served back to the user. For instance, in the above Python code, change `@app.route("/")` to `@app.route("/test")`. Now, accessing the URL `localhost:5000` does nothing, but accessing `localhost:5000/test` serves the "Hello World!" page.

### Configuring your Flask project

Flask projects are frequently structured in the following fashion:

```
├── run.py
├── venv/
├── requirements.txt
├── website/
	└── static/
	└── templates/
	└── views.py
```

Let's go through each piece.

#### run.py

The `run.py` file is ultimately what gets executed in the console to run the development server that we used for our Hello World! example. In that first iteration, we included our route (also called a "view") in the `run.py` file. As our projet gets more sophisticated, it gets cumbersome to have all of our views in the `run.py` file. We'll move those somewhere else. In the meantime, let's update our `run.py` file to contain the following code:

```python
from website import app

app.run('0.0.0.0', debug=True)
```

This configuration will make more sense when we eventually configure our Apache web server to create a production-level website.

#### Virtual environment and requirements.txt

Following convention, I create a virtual environment named `venv` using the steps in the Hello World! example. Make sure you always activate the virtual environment when you start working on this project. Every time a new module is added to our pip environment, we want to get in the habit of adding it to our `requirements.txt` file:

```posh 
matt@matt$ pip freeze > requirements.txt
```

This makes it easier for you to install your Python environment when moving to a production server.

#### The website directory

This directory contains all the content of our website as well as the views that connect URL paths with the content we wish to deliver.

#### static

The `static/` directory contains the static files including CSS files, JavaScript files and images. It is structured as follows:

```
├── static/
	└── bower.json
	└── bower_components/
	└── css/
		└── style.css
	└── downloads/
	└── img/
		└── favicon.ico
		└── mugshot_website.png
```

The `bower.json` file and `bower_components` directory are automatically created when we install packages with bower (and save the history of added packages). For this project, I am using Bootstrap v3, Bootstrap Social and Font Awesome (jQuery gets automatically installed as it is a dependency of Bootstrap). To install these packages, simply copy my `bower.json` file into your `static/` directory and enter the following command:

```posh 
matt@matt$ bower install
```

My `style.css` file contains all of the CSS I want to layer on top of Bootstrap. Eventually, we will add another CSS file that handles the syntax coloring of the code snippets you see in this post.

#### templates

This directory contains all of the HTML files that will be served. Before we get to the blogging components of this website, let's start with two files: `home_page.html` and `layout.html`. A powerful component of Flask (via the [Jinja](http://jinja.pocoo.org/) package) is the ability to create "layouts" that get passed on to each additional web page. In my case, the `layout.html` file allows me to add a universal header and navbar to each page without having to manually add that information to each and every HTML file.

Here's a minimal version of my `layout.html` that demonstrates how to load a CSS file from the `bower_components` directory and how to allow the layout to be propagated to all future HTML files.

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

In a minimal version of `home_page.html` we would find the following:

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

#### views.py

The `views.py` file contains all of the routes we want to have for our website. The root page of any site is the `"/"` route:

```python
@app.route('/')
def index():
    return render_template('home_page.html')
```

The `render_templates` function automatically knows to look in the `templates` directory for the HTML file being referenced (the HTML file, in turn, automatically knows where to find the `layout.html` file).

A key feature of routes is their ability to handle variables. Try creating a route like this:

```python
@app.route('/<text>')
def blog_home(text):
	return text
```

Accessing the URL `localhost:5000/matt` will return a web page that says "matt". Eventually, we will use this feature to handle the serving of specific blog posts based on the URL.


## Markdown blog


## Amazon Web Services 


## Additional Resources





