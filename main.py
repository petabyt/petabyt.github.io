# Yes, this is spahgetti code
# pip3 install marko bottle
import os, html, re
import io
from datetime import date
from bottle import *

from parser import parse

def getIndex():
    fp = open("blog-index.html", "r")
    index = fp.read()
    fp.close()
    return index

def getPosts():
    content = ""
    files = os.listdir("posts/")

    for i in range(len(files), 0, -1):
        fp = open("posts/" + str(i))
        post = fp.read()
        fp.close()

        if post[0:5] == ":skip":
            continue

        url, title, dateStr, post = parse(post, False)

        content += "<div class='post' title='Post #" + str(i) + "'>" + post + "</div>"
    return content

def getPost(name):
    content = ""
    files = os.listdir("posts/")

    for i in range(len(files), 0, -1):
        fp = open("posts/" + str(i))
        post = fp.read()
        fp.close()

        if post[0:5] == ":skip":
            continue

        url, title, dateStr, post = parse(post, True)
        if url == name:
            return title, "<div class='post' title='Post #" + str(i) + "'>" + post + "</div><a class='back' href='.'>Back</a>"
    return "Post not found", "<p class='center'>Post not found.</p>"

def getPostByID(num):
    content = ""

    try:
        fp = open("posts/" + str(num), "r")
    except:
        return "404"
    post = fp.read()
    fp.close()

    if post[0:5] == ":skip":
        return "404"

    url, title, dateStr, post = parse(post, True)
    return url

def genMainPage():
    return template(
        getIndex(),
        posts=getPosts(),
        title="Daniel's stuff",
        header="Daniel's stuff",
        top_level=".",
    )

# def getPost(post):
#     title, content = getPost(post)
#     return template(
#         getIndex(),
#         posts=content,
#         title=title
#     )

def genRss():
    domain = "https://danielc.dev/blog"
    title = "Daniel's Blog"
    desc = "Mostly for write-ups"

    content = """<?xml version="1.0" encoding="UTF-8"?>
    <rss xmlns:atom="http://www.w3.org/2005/Atom" version="2.0">
        <channel>
          <title>""" + title + """</title>
            <link>""" + domain + """</link>
            <description>""" + desc + """</description>
            <generator>Tinyblog</generator>
            <language>en</language>
            <lastBuildDate>""" + date.today().strftime("%Y-%m-%d") + """</lastBuildDate>
    """
    
    files = os.listdir("posts/")

    for i in range(len(files), 0, -1):
        fp = open("posts/" + str(i))
        post = fp.read()
        fp.close()

        if post[0:5] == ":skip":
            continue

        url, title, dateStr, post = parse(post, False)

        content += """
            <item>
            <title>""" + title + """</title>
            <pubDate>""" + dateStr + """</pubDate>
            <link>""" + domain + """/""" + url + """</link>
            </item>"""
    content += """
        </channel>
    </rss>
    """
    return content

def genFiles():
    with open("blog/rss.xml", "w") as f:
        f.write(genRss())
    with open("blog/index.html", "w") as f:
        f.write(genMainPage())

    files = os.listdir("posts/")

    for i in range(len(files), 0, -1):
        fp = open("posts/" + str(i))
        post = fp.read()
        fp.close()

        if post[0:5] == ":skip":
            continue

        url, title, dateStr, post = parse(post, True)
        content = "<div class='post' title='Post #" + str(i) + "'>" + post + "</div><a class='back' href='.'>Back</a>"

        post = template(
            getIndex(),
            posts=content,
            title=title,
            header="Daniel's stuff",
            top_level="..",
        )

        os.mkdir("blog/" + url)
        with open("blog/" + url + "/index.html", "w") as f:
            f.write(post)

os.system("rm -rf blog")
os.system("mkdir blog")
genFiles()
