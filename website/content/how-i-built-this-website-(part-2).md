title: How I built this website (Part 2)
date: 2018-07-12
tags: markdown, web development
summary: In this post we cover the basics of Markdown, a simple and readable markup language for writing on the web.

## Introduction

This series is a step-by-step tutorial for making a website like the one you're currently browsing. It includes an introduction to the Flask web framework, an introduction to Markdown (the markup language used to write this post), and also an introduction to hosting and deploying websites using Amazon Web Services.

Posts in this series:
1. [Introduction to Flask](</blog/how-i-built-this-website-(part-1)>)
2. Introduction to Markdown (you are here)
3. [Configuring a Markdown blog](</blog/how-i-built-this-website-(part-3)>)
4. [Deploying to Amazon Web Services](</blog/how-i-built-this-website-(part-4)>)

In this post we cover the basics of Markdown, a simple and readable markup language for writing on the web. Markdown is widely used in web writing platforms. The best introduction to Markdown is given by it's creator, John Gruber, at his blog [Daring Fireball](https://daringfireball.net/projects/markdown/syntax). Here is an excerpt from his post on Markdown syntax:

>Markdown is intended to be as easy-to-read and easy-to-write as is feasible.
>
>Readability, however, is emphasized above all else. A Markdown-formatted document should be publishable as-is, as plain text, without looking like it’s been marked up with tags or formatting instructions. While Markdown’s syntax has been influenced by several existing text-to-HTML filters ... the single biggest source of inspiration for Markdown’s syntax is the format of plain text email.
>
>To this end, Markdown’s syntax is comprised entirely of punctuation characters, which punctuation characters have been carefully chosen so as to look like what they mean. E.g., asterisks around a word actually look like *emphasis*. Markdown lists look like, well, lists. Even blockquotes look like quoted passages of text, assuming you’ve ever used email.

Simply put, Markdown is intended to be used as a format for writing for the web. It has a lightweight syntax that corresponds easily to HTML's system of tags. The advantage of using Markdown for this blog is that I am afforded ease of writing and reading drafts without sacrificing anything from the final look and feel.

<img class="center-image" width="25%" src="/static/img/markdown_logo.svg" />

* * *

## Syntax Overview

In the sections below I will run through the main aspects of Markdown syntax. In each section, I will demonstrate how raw Markdown syntax translates into rendered HTML.

### Headers

Raw Markdown:

	# Header 1
	## Header 2
	...
	##### Header 5

Processed HTML:

# Header 1
## Header 2
...
##### Header 5

<br>

### Emphasis

	Using asterisks, one can create *italics* and **bold** fonts!

Using asterisks, one can create *italics* and **bold** fonts!

<br>

### Lists

Lists can be unordered:

	I have an urge to list fruits I really like:
	* Bananas
	* Apples
	* Peaches

I have an urge to list fruits I really like:
* Bananas
* Apples
* Peaches

...or ordered:

	I have an urge to rank my favorite vegetables:
	1. Broccoli
	2. Kale
	3. Yams

I have an urge to rank my favorite vegetables:
1. Broccoli
2. Kale
3. Yams

<br>

### Links

	This is [an example](http://mattcarter.co) of an inline link.

This is [an example](http://mattcarter.co) of an inline link.

	You can even give [links](http://mattcarter.co "Matt is great") titles! (Hover over me.)

You can even give [links](http://mattcarter.co "Matt is great") titles! (Hover over me.)

	Relative [link](/blog) paths also work.

Relative [link](/blog) paths also work.


<br>

### Footnotes

	Sometimes you are explaining something[^1]

Sometimes you are explaining something...[^1]

<br>

### Block quotes

	> The universe (which others call the Library) is composed of an indefinite and perhaps infinite number of hexagonal galleries...

>The universe (which others call the Library) is composed of an indefinite and perhaps infinite number of hexagonal galleries...

<br>

### Syntax-highlited code blocks

	```python
	print "Hello, I am written in Python."

	def make_blog_for_me(now):
		return "If only it were that simple."
	```

```python
print "Hello, I am written in Python."

def make_blog_for_me(now):
	return "If only it were that simple."
```

	You can also reference `code` in-line.

You can also reference `code` in-line.

<br>

### Inline HTML

You can also write raw HTML in a Markdown file and the HTML will persist when you convert the entire text to HTML.

	<button class="btn btn-primary">That's how I made this button</button>

<button class="btn btn-primary">That's how I made this button</button>


<br>

## Conclusion
In this post we learned the basics of reading and writing in the Markdown markup language. The raw Markdown text of posts for this blog, including this post, can be found [here](https://github.com/matt-cart/website/tree/master/website/content).

Now let's proceed to [Part 3](</blog/how-i-built-this-website-(part-3)>) for a walkthrough of setting up a Flask-driven Markdown blog.

* * *

### Footnotes

[^1]: That requires a little more explanation down here. 
