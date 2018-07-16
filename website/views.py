import os
import re
import datetime
import markdown2
import collections
from flask import render_template, send_from_directory

from website import app


class Tag:
    def __init__(self, name, number):
        self.name = name
        self.number = number


class Post:
    def __init__(self, title, date, tags, summary, href, content_md):
        self.title = title
        self.date = date
        self.tags = tags
        self.summary = summary
        self.href = href
        self.content_md = content_md
        self.content_html = md_to_html(content_md)


@app.route('/')
def index():
    return render_template('home_page.html')


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
    sorted_posts = sorted(posts, key=lambda x: datetime.datetime.strptime(x.date, '%Y-%m-%d'), reverse=True)
    return render_template('blog_home.html', posts=sorted_posts,
        tag_dict=sorted_tag_dict)


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
    return render_template('blog_home.html', posts=matching_posts,
        tag_dict=sorted_tag_dict, queried_tag=queried_tag)


@app.route('/blog/<post_title>')
def blog_post(post_title):
    md_path  = os.path.join(app.root_path, 'content', '%s.md' % post_title)
    post = parse_markdown_post(md_path)
    return render_template('blog_post.html', post=post)


def parse_markdown_post(md_path):
    with open(md_path, 'rU') as f:
        markdown = f.read()
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
    html = markdown2.markdown(md_string, extras=['footnotes',
        'fenced-code-blocks', 'target-blank-links', 'cuddled-lists',
        'header-ids'])
    return html 

