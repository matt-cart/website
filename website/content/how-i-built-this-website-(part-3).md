title: How I built this website (Part 3)
date: 2018-07-11
tags: web development, flask, markdown
summary: In this post we will build a more sophisticated Flask project that has a Markdown blog component.

## Introduction

This series is a step-by-step tutorial for making a website like this one. It includes an introduction to the Flask web framework, an introduction to Markdown (the markup language used to write this post), and also an introduction to hosting websites using Amazon Web Services.

Posts in this series:
1. [Flask](/blog/how-i-built-this-website-(part-1\))
2. [Introduction to Markdown](/blog/how-i-built-this-website-(part-2\))
3. Configuring the Markdown blog (you are here)
4. [Amazon Web Services](/blog/how-i-built-this-website-(part-4\))

In this post we will build a more sophisticated Flask project that has a Markdown blog component. This post builds on Part 1 of the series. Before starting, clone [my GitHub repository](https://github.com/matt-cart/website) for this project in order to follow along. As with last time, remember to install packages for both the Python virtual environment and Bower environment prior to starting.

## Updated structure

In [Part 1](/blog/how-i-built-this-website-(part-1)) we generated a minimal Flask website that had a simple landing page with two views. In this part, we'll want to add a few pages for the blogging component, views for handling blog entries and also the Markdown files for blog entries. We will also expand the `static/` directory in order to handle custom CSS files, images and downloads.

```
├── run.py
├── venv/
├── requirements.txt
├── website/
	└── static/
		└── bower.json
		└── bower_components/
		└── css/
		└── downloads/
		└── img/
	└── templates/
		└── blog_home.html
		└── blog_post.html
		└── home_page.html
		└── layout.html
	└── content/
		└── Markdown files for blog entries
	└── __init__.py
	└── views.py
```

## Markdown blogging

In designing this website, I wanted the blogging component to be as lightweight as possible. I want to be able to write a post in a text editor like [Sublime Text](https://www.sublimetext.com/) and publish it in a limited number of keystrokes. This means sacrificing fancy GUIs for writing and editing posts within the website itself. I also want my website to be "static". This means not having to rely on a database -- all content is derived from flat files. Static blogs are more secure (there are no concerns about database vulnerabilities) and more simple to configure.

The downside is that I am sacrificing add-ons like commenting systems and user accounts but I can live with that[^1]. The only add-on I'm indulging in this blog is a system for "tagging" entries with various keywords that can serve as links for returning all posts with the same tag.

### Structure of Markdown files

Here's an example of what the raw Markdown of a blog post will look like

	title: An example post
	date: 7/11/18
	tags: markdown, flask
	summary: In this post we show what a post looks like.

	Blog post content begings here. Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua...

Before we translate Markdown to HTML, we are going to parse these posts in order to pull out key content pieces, namely the title, date, summary and tags. Without doing this, everything would get rendered as normal text in `<p>` tags[^2]. We will handle this additional formatting after the initial conversion to HTML.

### Serving blog posts

For the sake of simplicity, the URL for each blog post will be identical to the title, which is in turn identical to the file name. So if the title is `An example post`, the URL for the post will be `http://mattcarter.co/blog/an-example-post` and the Markdown file will be `an-example-post.md`. All Markdown files will live in the `content/` directory.

By structuring our files and routes this way, our view for blog posts is rather simple:

```python
@app.route('/blog/<post_title>')
def blog_post(post_title):
    md_file = os.path.join(app.root_path, 'content', '%s.md' % post_title)
    with open(md_file, 'rU') as f:
        lines = f.readlines()
    html = md_to_html(md_file)
    html = format_post(html)
    return render_template('blog_post.html', post=html)
```

The post title is gathered from the route and then converted into the absolute path of the Markdown file on the file system by leveraging the `app.root_path` feature that Flask provides. We then read the file and convert it to HTML. The last step before passing the HTML back to the front-end is to handle the processing of the title, date, summary and tags at the top of the post using the `format_post()` function.


### Converting Markdown to HTML

To accomplish Markdown-to-HTML conversion I am using the Python package [python-markdown2](https://github.com/trentm/python-markdown2). The function in `views.py` that leverages the markdown2 module is short:

```python
def md_to_html(md_path):
    html = markdown2.markdown_path(md_path, extras=['footnotes',
        'fenced-code-blocks', 'target-blank-links', 'cuddled-lists',
        'header-ids'])
    return html 
```

markdown2 enables us to read a Markdown file from the file system and convert it to HTML with one function. Of note here are markdown2's "[extras](https://github.com/trentm/python-markdown2/wiki/Extras)". These extras are extensions of the vanilla Markdown-to-HTML functionality:
* `footnotes` - Allows the use of footnotes in Markdown.
* `fenced-code-blocks` - Allows for language-specific syntax highlighting.
* `target-blank-links` - Automatically adds `target="_blank"` to each `<a>` tag in HTML. This means each link opens a new browser tab by default.
* `cuddled-lists` - Tweaks traditional Markdown syntax so that you don't need a blank line between a list header and list elements.

### Post-processing of a post's header

The first step of post-processing a post is to separate the key bits of metadata from the content of the post. We will do this using a [regular expression](https://docs.python.org/2/library/re.html). More specifically, we will lean heavily on [match groups](https://docs.python.org/2/library/re.html#re.MatchObject.group) to pull out specific parts of the raw HTML and store them as variables for later use.

```python
re_pat = re.compile(r'<p>title: (?P<title>[^\n]*)\sdate: (?P<date>\d{4}-\d{2}-\d{2})\stags: (?P<tags>[^\n^]*)\ssummary: (?P<summary>[^\n^<]*)</p>')
```

This regular expression is pretty beefy. Here are the important pieces:
* `(?P<title>[^\n]*)` - Pulls out all of the text starting after the substring `title: ` and until the next newline character. This matching string (the title) is stored with the key `title`.
* `(?P<date>\d{4}-\d{2}-\d{2})` - Pulls out the YYYY-MM-DD date and stores this with the key `date`.
* `(?P<tags>[^\n^<]*)` - Pulls out all of the text starting after the substring `tags: ` and until the next newline character. This matching string (the comma-separated list of tags) is stored with the key `tags`.
* `(?P<summary>[^\n^<]*)` - Pulls out all of the text after the substring `summary: ` and until the next newline character OR angle-bracket character. This matching string is stored with the key `summary`.

After using the `re.match()` function, we can then access each match group with a command like `match_obj.group('title')`. I also call `re.split()` in order to split the overall HTML string using the regex pattern seen above. The last element of the list resulting from the split is all of the HTML content after the bits of metadata I've parsed out. All of these bits of metadata and the post content are stuffed into a custom `Post` object that I've defined in order to make organization of the metadata easier.

After I've built a `Post` object for the post in question, I rebuild the header to format the different bits of metadata appropriately. Namely, I wrap the title in `<h1>` HTML tags, the date in `<h4>` HTML tags and build link buttons out of each individual post tag. I then append the rest of the post content to the end of this re-formatted HTML section[^3]. This re-formatted HTML string is now ready to be passed back to the front-end.


### Blog home page



### Tags



## Conclusion





[^1]: For an depth look at a Flask blogging set up with user accounts, comments, etc. check out Miguel Grinberg's excellent [Flask Mega-Tutorial](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world).
[^2]: Why do it this way?...
[^3]: Note how I do note include the summary anywhere in the post. I plan to use the summary only on the landing page for the blog.

