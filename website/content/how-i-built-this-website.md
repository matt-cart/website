title: How I built this website
date: 2018-07-11
tags: flask, aws, markdown

### Introduction


### Prerequisites


### Flask

#### Setting up Flask

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

#### Configuring your Flask project

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

### Markdown blog


### Amazon Web Services 


### Additional Resources





