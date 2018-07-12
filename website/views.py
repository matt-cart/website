import os
import re
import markdown2
import collections
from flask import render_template, send_from_directory

from website import app


class Tag:
	def __init__(self, name, number):
		self.name = name
		self.number = number


class Post:
	def __init__(self, title, date, tags, content, href):
		self.title = title
		self.date = date
		self.tags = tags
		self.content = content
		self.href = href


@app.route('/')
def index():
    return render_template('home_page.html')


@app.route('/blog')
def blog_home():
	return render_template('blog_construction.html')

@app.route('/blog/<post_title>')
def blog_post(post_title):
	md_file = os.path.join(app.root_path, 'content', '%s.md' % post_title)
	with open(md_file, 'rU') as f:
		lines = f.readlines()
	html = md_to_html(md_file)
	html = format_post(html)
	return render_template('blog_post.html', post=html)


@app.route('/blog/tag/<queried_tag>')
def get_tagged_posts(queried_tag):
	tag_dict = dict()
	matching_posts = []
	content_path = os.path.join(app.root_path, 'content')
	for file in os.listdir(content_path):
		if not file.endswith('.md'):
			continue
		full_path = os.path.join(content_path, file)
		html = md_to_html(full_path)
		post_obj = get_post_metadata(html)
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



def md_to_html(md_path):
	html = markdown2.markdown_path(md_path, extras=['footnotes',
		'fenced-code-blocks', 'target-blank-links', 'cuddled-lists',
		'header-ids'])
	return html	


def get_post_metadata(html):
	re_pat = re.compile(r'<p>title: (?P<title>[^\n]*)\sdate: (?P<date>\d{4}-\d{2}-\d{2})\stags: (?P<tags>[^\n^<]*)</p>')
	match_obj = re.match(re_pat, html)
	title = match_obj.group('title')
	date = match_obj.group('date')
	tags = sorted([tag.strip() for tag in match_obj.group('tags').split(',')])
	content_html = re.split(re_pat, html)[-1]
	href = os.path.join('http://mattcarter.co', 'blog', title.lower().replace(' ', '-'))
	return Post(title, date, tags, content_html, href)


def format_post(html):
	post_obj = get_post_metadata(html)

	header_html = '<h2>%s</h2><h5>%s</h5><p>Tags: ' % (post_obj.title, post_obj.date)
	for tag in post_obj.tags:
		header_html += '<a class="btn btn-default btn-xs tag-link" href="http://mattcarter.co/blog/tag/%s"><span class="glyphicon glyphicon-tag"></span> %s</a>' % (tag, tag)
	header_html += '</p>'
	html = header_html + post_obj.content
	return html


@app.route('/resume', methods=['GET', 'POST'])
def resume():
    return send_from_directory('static', filename='MatthewCarterResume.pdf')