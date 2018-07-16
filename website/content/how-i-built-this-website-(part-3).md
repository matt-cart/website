title: How I built this website (Part 3)
date: 2018-07-13
tags: flask, markdown, web development
summary: In this post we will build a more sophisticated Flask project that has a Markdown blog component.

## Introduction

This series is a step-by-step tutorial for making a website like the one you're currently browsing. It includes an introduction to the Flask web framework, an introduction to Markdown (the markup language used to write this post), and also an introduction to hosting websites using Amazon Web Services.

Posts in this series:
1. [Flask](/blog/how-i-built-this-website-(part-1\))
2. [Introduction to Markdown](/blog/how-i-built-this-website-(part-2\))
3. Configuring the Markdown blog (you are here)
4. [Amazon Web Services](/blog/how-i-built-this-website-(part-4\))

In this post we will build a more sophisticated Flask project that has a Markdown blog component. This post builds on Part 1 of the series. Before starting, clone [my GitHub repository](https://github.com/matt-cart/website) for this project in order to follow along (this is different than the repository we used in Part 1). As with last time, remember to install packages for both the Python virtual environment and Yarn environment prior to starting.

## Updated website structure

In [Part 1](/blog/how-i-built-this-website-(part-1)) we generated a minimal Flask website that had a simple landing page with two views -- one for the main page and one page with a custom route. In this part, we'll want to add a few templates for the blogging component, views for handling blog entries and also the Markdown files for blog entries. We will also expand the `static/` directory in order to handle custom CSS files, images and downloads.


The structure of this improved Flask project is as follows:

```
├── run.py
├── venv/
├── requirements.txt
├── website/
	└── static/
		└── package.json
		└── node_modules/
		└── extra_modules/
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

In designing this website, I wanted the blogging component to be as lightweight as possible. I want to be able to write a post in a text editor like [Sublime Text](https://www.sublimetext.com/) and then publish it in a limited number of keystrokes. This means sacrificing fancy GUIs for writing and editing posts within the website itself. I also want my website to be "static". This means not having to rely on a database for persistence of content -- all content is derived from flat files. Static blogs are more secure (there are no concerns about database vulnerabilities) and more simple to configure.

The downside is that I am sacrificing add-ons like commenting systems, user accounts, etc. but I can live with that[^1]. The only add-on I'm indulging in this blog is a system for "tagging" entries with various keywords that can serve as links for returning all posts with the same tag.

### Structure of Markdown blog posts

Here's an example of what the raw Markdown of a blog post will look like

	title: An example post
	date: 7/11/18
	tags: markdown, flask
	summary: In this post we show what a post looks like.

	Blog post content begings here. Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua...

Before we translate Markdown to HTML, we are going to parse these posts in order to pull out key content pieces, namely the title, date, summary and tags. Without doing this, everything would get rendered as normal text in `<p>` tags[^2]. We will handle the additional formatting of these special elements in the template using Jinja.

### Serving blog posts

For the sake of simplicity, the URL for each blog post will be identical to the title, which is in turn identical to the file name. So if the title is `An example post`, the URL for the post will be `http://mattcarter.co/blog/an-example-post` and the Markdown file will be `an-example-post.md`. All Markdown files will live in the `content/` directory.

By structuring our files and routes this way, our view for blog posts looks rather simple:

```python
@app.route('/blog/<post_title>')
def blog_post(post_title):
    md_path  = os.path.join(app.root_path, 'content', '%s.md' % post_title)
    post = parse_markdown_post(md_path)
    return render_template('blog_post.html', post=post)
```

The post title is gathered from the route and then converted into the absolute path of the Markdown file on the file system by leveraging the `app.root_path` feature that Flask provides. We then read the file, parse out the metadata and convert the rest to HTML.


### Pre-processing of Markdown file

Before doing the conversion to HTML, we want to parse out the metadata in the file's header. We will do this using a [regular expression](https://docs.python.org/2/library/re.html). More specifically, we will lean heavily on [match groups](https://docs.python.org/2/library/re.html#re.MatchObject.group) to pull out specific parts of the raw HTML and store them as variables for later use.

```python
re_pat = re.compile(r'title: (?P<title>[^\n]*)\sdate: (?P<date>\d{4}-\d{2}-\d{2})\s'
					r'tags: (?P<tags>[^\n]*)\ssummary: (?P<summary>[^\n]*)')
```

This regular expression is pretty beefy. Here are the important pieces:
* `(?P<title>[^\n]*)` - Pulls out all of the text starting after the substring `title: ` and until the next newline character. This matching string (the title) is stored with the key `title`.
* `(?P<date>\d{4}-\d{2}-\d{2})` - Pulls out the YYYY-MM-DD date and stores this with the key `date`.
* `(?P<tags>[^\n^<]*)` - Pulls out all of the text starting after the substring `tags: ` and until the next newline character. This matching string (the comma-separated list of tags) is stored with the key `tags`.
* `(?P<summary>[^\n^<]*)` - Pulls out all of the text after the substring `summary: ` and until the next newline character. This matching string is stored with the key `summary`.

After using the `re.match()` function, we can then access each match group with a command like `match_obj.group('title')`. I also call `re.split()` in order to split the overall Markdown string using the regex pattern seen above. The last element of the list resulting from the split is all of the Markdown content after the bits of metadata I've parsed out. All of these bits of metadata and the post content are stuffed into a custom `Post` object that I've defined in order to make organization of the metadata easier.

The `Post` object looks like this:

```python
class Post:
    def __init__(self, title, date, tags, summary, href, content_md):
        self.title = title
        self.date = date
        self.tags = tags
        self.summary = summary
        self.href = href
        self.content_md = content_md
        self.content_html = md_to_html(content_md)
```

Importantly, the HTML content of the post is generated automatically upon instantiation of a `Post` object. I'll cover the `md_to_html()` function below. 

### Converting Markdown to HTML

To accomplish Markdown-to-HTML conversion I am using the Python package [python-markdown2](https://github.com/trentm/python-markdown2). The function in `views.py` that leverages the markdown2 module is short:

```python
def md_to_html(md_string):
    html = markdown2.markdown(md_string, extras=['footnotes',
        'fenced-code-blocks', 'target-blank-links', 'cuddled-lists',
        'header-ids'])
    return html 
```

Of note here are markdown2's "[extras](https://github.com/trentm/python-markdown2/wiki/Extras)". These extras are extensions of the vanilla Markdown-to-HTML functionality:
* `footnotes` - Allows the use of footnotes in Markdown.
* `fenced-code-blocks` - Allows for language-specific syntax highlighting.
* `target-blank-links` - Automatically adds `target="_blank"` to each `<a>` tag in HTML. This means each link opens a new browser tab by default.
* `cuddled-lists` - Tweaks traditional Markdown syntax so that you don't need a blank line between a list header and list elements.



### Blog home page

The landing page fot the `/blog` view will have three purposes. First, it will show an archive of all previous blog posts, showing the title, tags and summary for each post. Second, it will provide a list of all the tags used on published posts, each tag will be a link to see all posts with a given tag. Third, the blog landing page will double as the view for browsing posts with a specific tag. We'll cover this in the next section.

In order to show an archive of every post, the function associated with the `/blog` view will need to loop over every Markdown post in the `/content` directory and then parse each post's header information. Along the way, we'll want to keep running totals of the number of posts associated with each tag. This is accomplished by using a dictionary. The last is to sort the tags in alphabetical order (vanilla Python dictionaries are intrinsically unordered so we're using an `OrderedDict` for this) and to sort the posts by the date they were published. Below you can find the `blog_home()` function for the `/blog` view.

```python
@app.route('/blog')
def blog_home():
    tag_dict = dict()
    posts = []
    content_path = os.path.join(app.root_path, 'content')
    for file in os.listdir(content_path):
        if not file.endswith('.md'):
            continue
        full_path = os.path.join(content_path, file)
        post_obj = parse_markdown_post(full_path)
        posts.append(post_obj)
        for tag in post_obj.tags:
            if tag not in tag_dict.keys():
                tag_dict[tag] = 0
            tag_dict[tag] += 1
    sorted_tag_dict = collections.OrderedDict()
    for key in sorted(tag_dict.keys()):
        sorted_tag_dict[key] = tag_dict[key]
    sorted_posts = sorted(posts, 
        key=lambda x: datetime.datetime.strptime(x.date, '%Y-%m-%d'), reverse=True)
    return render_template('blog_home.html', posts=sorted_posts,
        tag_dict=sorted_tag_dict)
```

When this information is passed to the front end, we handle the `posts` and `tag_dict` objects using Jinja. In the `blog_home.html` template we create two column divs. On the left hand side we loop over the `posts` list and create a [jumbotron](https://getbootstrap.com/docs/3.3/components/#jumbotron) element for each post[^4].

```html
{% for post in posts %}
	<div class="jumbotron jumbotron-posts">
        <h3 class="tight-top"><a href="{{ post.href }}">{{ post.title }}</a></h3>
        <h5>{{ post.date }}</h5>
        <p>{{ post.summary }}</p>
        <hr>
       	{% for tag in post.tags %}
			<a class="btn btn-default btn-xs tag-link" href="http://mattcarter.co/blog/tag/{{ tag.name }}">
				<span class="glyphicon glyphicon-tag"></span> {{ tag }}
			</a>
		{% endfor %}
	</div>
{% endfor %}
```

On the right hand side we iterate over the `tag_dict` tag and create links for each tag while showing how many posts have each tag.

```html
{% for tag in tag_dict %}
	<p>
		<a class="btn btn-default btn-xs tag-link" href="http://mattcarter.co/blog/tag/{{ tag }}">
			<span class="glyphicon glyphicon-tag"></span> {{ tag }}
		</a>
		{{ tag_dict[tag] }}
	</p>
{% endfor %}
```

The final product looks like this:

<img class="center-image" width="500" height="500" src="/static/img/blog_home_page_scrn.png" />

### Tags

In the absence of a search feature, I wanted some low-overhead means of organizing posts into broad categories. To accomplish this, I'm using tags. As we saw above, the tags for a post exist in the post's header section. These tags then appear as links at the top of a blog post page. These tag links also appear on the blog home page that we just covered. When someone clicks one of these links they should see all of the posts that have that tag. To accomplish this, I created a view that looks like this:

```python
@app.route('/blog/tag/<queried_tag>')
def get_tagged_posts(queried_tag):
    tag_dict = dict()
    matching_posts = []
    content_path = os.path.join(app.root_path, 'content')
    for file in os.listdir(content_path):
        if not file.endswith('.md'):
            continue
        full_path = os.path.join(content_path, file)
        post_obj = parse_markdown_post(full_path)
        if queried_tag in post_obj.tags:
            matching_posts.append(post_obj)
        for tag in post_obj.tags:
            if tag not in tag_dict.keys():
                tag_dict[tag] = 0
            tag_dict[tag] += 1
    sorted_tag_dict = collections.OrderedDict()
    for key in sorted(tag_dict.keys()):
        sorted_tag_dict[key] = tag_dict[key]
    sorted_posts = sorted(matching_posts,
        key=lambda x: datetime.datetime.strptime(x.date, '%Y-%m-%d'), reverse=True)
    return render_template('blog_home.html', posts=sorted_posts,
        tag_dict=sorted_tag_dict, queried_tag=queried_tag)
```

Note that the `queried_tag` argument for the function `get_tagged_posts()` comes from the URL. Also note that this function is very similar to the `blog_home()` function we just covered. In fact, we are going to use the same blog home page template. The key difference is that we are only passing posts back to the front end that include the tag we are querying for. In fact, I could have only used one function for both routes and merely decorated the function twice like this:

```python
@app.route('/blog')
@app.route('/blog/tag/<queried_tag>')
def get_tagged_posts(queried_tag=None):
	...
	return render_template('blog_home.html', posts=sorted_posts,
        tag_dict=sorted_tag_dict, queried_tag=queried_tag)
```

In this case, when the `/blog` route is accessed, the `queried_tag` argument defaults to `None` and our function implementation would be such that all posts would ultimately end up in `sorted_posts`.

For either implementation, though, the template we wish to render is the `blog_home.html` template. Because this page will handle the cases of "all posts" and "only specifically tagged posts", we need to incorporate some logic on the front end using Jinja:

```html
{% if queried_tag %}
	<h2 class="text-center">Posts with tag: "{{ queried_tag }}"</h2>
{% else %}
	<h2 class="text-center">All posts</h2>
{% endif %}
```

In the case of showing "all posts", the `blog_home()` function does not pass the variable `queried_tag` to the front end and so it defaults to `None`. For either case, the format `Post` objects being used are identical, it is only the length of the list of `Post` objects that changes so the rest of the template can be used for both cases.


## Conclusion





[^1]: For an depth look at a Flask blogging set up with user accounts, comments, etc. check out Miguel Grinberg's excellent [Flask Mega-Tutorial](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world).
[^2]: Why do it this way?...
[^3]: I do note include the summary anywhere in the post. I plan to use the summary only on the landing page for the blog.
[^4]: We are handling the same `Post` objects that used when creating the page for an individual post.

