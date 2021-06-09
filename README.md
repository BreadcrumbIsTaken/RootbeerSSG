<div align="center">
    <img src="https://github.com/BreadcrumbIsTaken/RootbeerSSG/blob/main/.github/rootbeer-logo.png">
    <h1>RootbeerSSG 🍺</h1>
    <h3>The easy to use and very epic static site generator for blogs!</h3>
    <h6>Just think of the emoji above as a glass of rootbeer ok?</h6>
</div>

[![Compatability: Club Penguin](https://forthebadge.com/images/badges/compatibility-club-penguin.svg)](https://forthebadge.com)
[![Fo Shizzle](https://forthebadge.com/images/badges/fo-shizzle.svg)](https://forthebadge.com)
[![It works. Why?](https://forthebadge.com/images/badges/it-works-why.svg)](https://forthebadge.com)
[![Made with Python](https://forthebadge.com/images/badges/made-with-python.svg)](https://python.org)
[![Mom made pizza rolls](https://forthebadge.com/images/badges/mom-made-pizza-rolls.svg)](https://forthebadge.com)
[![Open source.](https://forthebadge.com/images/badges/open-source.svg)](https://github.com/BreadcrumbIsTaken/RootbeerSSG)
[![Built with swag](https://forthebadge.com/images/badges/built-with-swag.svg)](https://forthebadge.com)
[![Pypi Version](https://img.shields.io/pypi/v/rootbeer?style=for-the-badge)](https://pypi/project/rootbeer)
[![Total Lines of Code](https://img.shields.io/tokei/lines/github/BreadcrumbIsTaken/RootbeerSSG?style=for-the-badge)](https://github.com/BreadcrumbIsTaken)
[![License: CC BY SA 4.0](https://img.shields.io/pypi/l/rootbeer?style=for-the-badge)](https://pypi/project/rootbeer)
[![Python versions](https://img.shields.io/pypi/pyversions/rootbeer?style=for-the-badge)](https://pypi/project/rootbeer)
[![Status](https://img.shields.io/pypi/status/rootbeer?style=for-the-badge)](https://pypi/project/rootbeer)

# What is RootbeerSSG? 🤔

RootbeerSSG (or Rootbeer as I call it 100% of the time) is a <abbr title="Static Site Generator">SSG</abbr> that specilises in making static blogs.
It can easily integrate with things like [Staticman](https://staticman.net). You can also quickly deploy it to the free hosting platform [Netlify](https://netlify.com)

Rootbeer is aimed for people who are new too things like Static Site Generators and strives to make it as easy as possible.

# How to download Rootbeer 🔻

It's easy!

All you have to do is open a terminal and put this line into it:
```bash
pip install rootbeer
```
Or
```bash
python -m pip install rootbeer
```
Or
```bash
python3 -m pip install rootbeer
```

## Running on your machine 💻:
The recommended way to install Rootbeer is to make a Virtual Envrionment. You will need a package called `venv`
If you don't have the `venv` module, you can install it like this:
```shell
pip install venv
```
You can do so by putting this in your console:
```shell
python -m venv env
```
and it will create a folder called `env`. You can call it whatever you want.
Now to activate it, in your console run
```shell
env\Scripts\activate
```
if you are on Windows.
Great! You have your virtual environment!
If you want to deactivate the virtual environment, just run
```shell
deactivate
```
# How to use Rootbeer 💡

All you have to do is:
```python
from rootbeer import RootbeerSSG

rb = RootbeerSSG()
```
and run the file!!!
Then write away! For more info, take a look at the Wiki section on the GitHub.

Rootbeer has two types of content: `pages` and `posts`. `pages` are, well, you know. Pages.
`posts` are the things you write and are stored in the blog folder.

Rootbeer supports Markdown for the `posts` and `pages`. They will be rendered into HTML.

# How to preview your site on your local machine 🍃

You can do this in your terminal:
```shell
cd public
```
and then:
```shell
python -m http.server
```

and then you can go too [localhost:8000](http://localhost:8000) and BOOM! You have your site running!

# How customizable is Rootbeer? 🎨

How does PLUGINS and THEMES sound?

See the Wiki for more info.

# Why tho???

Because I felt like it lol and [WordPress](https://wordpress.org) hosting is the monez
