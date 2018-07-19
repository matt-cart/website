import os
import re
import mistune
import datetime
import collections
from pygments import highlight
from pygments.formatters import html
from pygments.lexers import get_lexer_by_name
from flask import render_template, send_from_directory

from website import app


class Post:
    """
    An instance contains metadata about a blog post as well as the body of the
    blog post written in Markdown. Upon instantiation, the Markdown content is
    additionally converted into HTML.
    """
    def __init__(self, title, date, tags, summary, href, content_md):
        self.title = title
        self.date = date
        self.tags = tags
        self.summary = summary
        self.href = href
        self.content_md = content_md
        self.content_html = md_to_html(content_md)


class HighlightRenderer(mistune.Renderer):
    """
    Extend renderer built into mistune module. This object unables code
    highlighting during Markdown-to-HTML conversions.
    """
    def block_code(self, code, lang):
        """
        Get the language indicated in each fenced code block. Get the
        appropriate Pygments lexer based on this language and parse code 
        accordingly into HTML format. If not language is detected, use vanilla
        <code> blocks.
        """
        if not lang:
            return '\n<pre><code>%s</code></pre>\n' % \
                mistune.escape(code)
        lexer = get_lexer_by_name(lang, stripall=True)
        formatter = html.HtmlFormatter()
        return highlight(code, lexer, formatter)


@app.route('/')
def index():
    """
    Render the main landing page for http://mattcarter.co.
    """
    return render_template('home_page.html')


@app.route('/blog')
def blog_home():
    """
    Render the blog home page. First, iterate over all Markdown files in 
    /content directory. Then parse each post for meta data. Add tag info to the
    dictionary of tags. Sort posts by date and tags alphabetically.
    """
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


@app.route('/blog/tag/<queried_tag>')
def get_tagged_posts(queried_tag):
    """
    Render the blog home page, but with posts filtered by a particular tag.
    First, iterate over all Markdown files in /content directory. Then parse
    each post for meta data. Ignore posts that lack the specified tag. Add tag
    info to the dictionary of tags. Sort posts by date and tags alphabetically.
    """
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


@app.route('/blog/<post_title>')
def blog_post(post_title):
    """
    Render the page for a blog post. Find the post in the /content directory
    based on the incoming URL and parse the post metadata.
    """
    md_path  = os.path.join(app.root_path, 'content', '%s.md' % post_title)
    post = parse_markdown_post(md_path)
    return render_template('blog_post.html', post=post)


def parse_markdown_post(md_path):
    """
    Use a regular expression to parse the components of a Markdown post's
    header and the post body. Return an assembled Post object,
    """
    with open(md_path, 'rU') as f:
        markdown = f.read().decode('utf-8')
    re_pat = re.compile(r'title: (?P<title>[^\n]*)\sdate: (?P<date>\d{4}-\d{2}-\d{2})\s'
                        r'tags: (?P<tags>[^\n]*)\ssummary: (?P<summary>[^\n]*)')
    match_obj = re.match(re_pat, markdown)
    title = match_obj.group('title')
    date = match_obj.group('date')
    summary = match_obj.group('summary')
    tags = sorted([tag.strip() for tag in match_obj.group('tags').split(',')])
    href = os.path.join('http://mattcarter.co', 'blog', title.lower().replace(' ', '-'))
    content_md = re.split(re_pat, markdown)[-1]
    return Post(title, date, tags, summary, href, content_md)


def md_to_html(md_string):
    """
    Convert a Markdown string to HTML.
    """
    markdown_formatter = mistune.Markdown(renderer=HighlightRenderer())
    html = markdown_formatter(md_string)
    return html 

