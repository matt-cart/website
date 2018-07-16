title: How I built this website (Part 1)
date: 2018-07-11
tags: aws, flask, markdown, web development
summary: In this this post we cover the creation of a minimal Flask-driven website.

## Introduction

This series is a step-by-step tutorial for making a website like the one you're currently browsing. It includes an introduction to the Flask web framework, an introduction to Markdown (the markup language used to write this post), and also an introduction to hosting and deploying websites using Amazon Web Services.

Posts in this series:
1. Introduction to Flask (you are here)
2. [Introduction to Markdown](/blog/how-i-built-this-website-(part-2\))
3. [Configuring a Markdown blog](/blog/how-i-built-this-website-(part-3\))
4. [Deploying to Amazon Web Services](/blog/how-i-built-this-website-(part-4\))

In this this post we cover the creation of a minimal Flask-driven website. We'll use [this GitHub repository](https://github.com/matt-cart/minimal-website-demo) for demo purposes. You're welcome to clone it and start from there or try to replicate it from scratch. In Part 3, we'll dive in deeper discuss how to make a website that contains Markdown blog functionality.

## What is a website?

### A disclaimer

The ease with which we can easily and reliably interact with the World Wide Web belies the sophistication of the technological apparatus that enables such interactions[^1]. When I first started learning the ropes of web development, I found the internet to be aptly described by [Clarke's Third Law](https://en.wikipedia.org/wiki/Clarke%27s_three_laws). Before starting the tutorial, I've tried to provide some useful background on the internet below. I wrote this background with naïve me in mind.

With that being said, this background often includes heavily acronymical jargon and is by no means required reading for actually creating a functional website. If you wish, simply proceed to the "Assumptions and Prerequisites" section.

### Now for the jargon

Every functional website can be referenced by a uniform resource locator (URL). This URL serves as an address that specifies the location of the website within the broader network of the Internet. Importantly, the URL is not an inherently useful address, it is merely one that can be remembered by humans. A domain name system (DNS) server is responsible for storing the translation of URLs into a numerical internet protocol (IP) address which is then used to locate the physical computer system that stores the content you wish to access by using a specific URL. An actual URL, familiarly, looks something like this:

```
http://google.com/maps
```

But this URL is comprised of several important components that can be syntactically described as follows[^2]:

```
scheme://[authority]/[path]
```

The components are as follows:
* `scheme`: describes the protocol to be used to access the URL. Frequently, the scheme is `http` (*h*yper*t*ext *t*ransfer *p*rotocol), `https` (*h*yper*t*ext *t*ransfer *p*rotocol over transport layer *s*ecuriry) or `ftp` (*f*ile *t*ransfer *p*rotocol).
* `authority`: most frequently used to describe the "host", which is ultimately translated to an IP address by the aforementioned DNS server. In our case, the authority is `google.com`.
* `path`: the path resembles a file system path. In some cases, the path component in a URL may actually map to a file system path on the server being accessed by a URL. Either way, this path is handled by the web server to determine what content should be served back to the user. When we go to <http://google.com/maps>, the `maps` path specifies to Google's servers that I want to see the Google Maps application.

Any time you interaction you have with a web browser can be thought of as "client-side". Certain interactions, such as you hitting "enter" after typing "http://google.com/maps" into your address bar, can trigger events on the "server-side". For websites like this one, when someone enters the URL "http://mattcarter.co/blog" (client side), a request is sent to the server that "hosts" my web application (server side). The web server I am using (Apache, as we'll cover in Part 3), routes this request (and all others from the web) to my web application. The request says "someone is trying to access the web page for the `/blog` path". The application I have created uses a web framework (Flask, as we'll cover below) that is capable of processing this incoming request in some meaningful way and then serving something back to the user via the web server. "Processing the request in some meaningful way" can be many things -- we'll get into a few of these things. Regardless, there exists some mapping of URL paths to actions that my web application will take. 

The above explanation is not complete or exact. Someone who works on the technology driving the internet might even go so far as to call this explanation "wrong". If anything, I have glossed over nuance for the sake of providing a useful mental model. As I said, such an explanation would have been useful to me when I was first developing websites. This tutorial will cover the construction of the client-side web pages that a user interacts with and also the construction of the server-side application that the user (intentionally) never sees. Understanding the gulf that exists between client-side and server-side, that is, the inner workings of domain name systems, transfer protocols and internet networks is simply not required to make a website like the one we are making in this tutorial.

As a final disclaimer, I should say that his website is intentionally constructed in a very simple fashion. It is simple for the sake of straightforward pedagogy, but also for the sake of maintenance. This website exists near one end of the complexity spectrum -- something like the Google Search Engine exists at the other.

* * *

Let's dive in to the tutorial. This post in the series will result in us creating a website operating on a so called "development server". That is, this website will be functional but won't be visible to the outside world. In Part 4 we will make our final product visible to the entire Internet.


## Assumptions and Prerequisites

This tutorial assumes the reader has a basic understanding of Python (specifically version 2.7), HTML, CSS and the Unix command line. I am also assuming that you are using a Mac or Linux operating system.

Before starting, make sure you have the following software management tools installed:
- [pip](https://docs.python.org/2.7/installing/) - A Python package manager.
- [virtualenv](https://realpython.com/python-virtual-environments-a-primer/) - A tool for creating localized Python package installations.
- [Homebrew](https://brew.sh/) - "Homebrew installs the stuff you need that Apple didn't."
- [npm](https://www.npmjs.com/get-npm) - A JavaScript package manager.
- [yarn](https://yarnpkg.com/en/docs/getting-started) - A package manager for web projects.

## Flask

### Setting up Flask

[Flask](http://flask.pocoo.org/) is a microframework for Python. Flask is lightweight and highly configurable. One does not need to sift through heaps of boilerplate code in order to get a project up and running. To illustrate how quick Flask is, create a new directory, install Flask using pip and create a file called `run.py`:

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

app.run('0.0.0.0')
```

Back in Terminal, enter the following command:

```posh
matt@matt$ python run.py
```

After entering this command, Flask creates a "development" web server that is built into the module. This development server allows you to access a version of your website that is only available locally. This is specified by the IP address `0.0.0.0`, which equates to "the IP address of this machine". Even more specifically, this development server must be accessed by a specific "port". A port is a specific endpoint for communication with the development server. All web servers use specific ports for communication, but this is frequently masked from the user by the web server.

For the purposes of our development server, though, we can access this local IP address and port by entering the following shorthand into a web browser of your choosing: `localhost:5000`. *Et viola*, you will see your "Hello World!". The important thing to note is that this URL has an implicit "path" (see background above). The path in this case is the "`/`" route. Flask uses "routes" to decorate functions. The URL that is accessed determines which Python function in your project gets called, and ultimately what gets served back to the user.

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
	└── package.json
	└── node_modules/
```

The `package.json` file and `node_modules` directory are automatically created when we install packages with Yarn. Here, I am using Bootstrap v3. To install this packages and automatically create the `node_modules` directory, run the following command while in the `static` directory:

```posh 
matt@matt$ yarn install
```

In [Part 3](/blog/how-i-built-this-website-(part-3\)), we'll discuss adding custom CSS and images to the `static` directory.

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

It is in this `__init__.py` file that we create the all important Flask object `app` that gets referenced in our `run.py` file. We could put all of this information in the `run.py` file itself, but when we ultimately want to configure this application to run on a real web server in [Part 4](/blog/how-i-built-this-website-(part-4)), this setup makes it easier.

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

Proceed to [Part 2](/blog/how-i-built-this-website-(part-2)) for an introduction to Markdown.



[^1]: A fascinating documentary about the past, present and future of the internet can be found in Werner Herzog's recent documentary [Lo and Behold: Reveries of the Connected World](https://www.youtube.com/watch?v=lYVjUT4FiOc). Watch this documentary even if only to see Herzog tell Elon Musk that he volunteers to go to Mars.
[^2]: <https://en.wikipedia.org/wiki/URL#Syntax>

