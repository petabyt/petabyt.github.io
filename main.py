# Yes, this is spahgetti code
# pip3 install marko bottle
import os, html, re
import io
from datetime import date
from bottle import *
from parser import parse

DOMAIN = "https://danielc.dev/blog"
TITLE = "Daniel Cook"
DESC = "Mostly for write-ups"

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

        output = parse(post, False)

        content += "<div class='post' title='Post #" + str(i) + "'>" + output["text"] + "</div>"
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

        output = parse(post, True)
        if output["url"] == name:
            return title, "<div class='post' title='Post #" + str(i) + "'>" + output["text"] + "</div><a class='back' href='.'>Back</a>"
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

    output = parse(post, True)
    return output["url"]

def genMainPage():
    return template(
        getIndex(),
        posts=getPosts(),
        title=TITLE,
        header=TITLE,
        top_level=".",
        tags = "",
    )

# def getPost(post):
#     title, content = getPost(post)
#     return template(
#         getIndex(),
#         posts=content,
#         title=title
#     )

def genRss():
    content = """<?xml version="1.0" encoding="UTF-8"?>
    <rss xmlns:atom="http://www.w3.org/2005/Atom" version="2.0">
        <channel>
          <title>""" + TITLE + """</title>
            <link>""" + DOMAIN + """</link>
            <description>""" + DESC + """</description>
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

        output = parse(post, False)

        content += """
            <item>
            <title>""" + output["title"] + """</title>
            <pubDate>""" + output["date"] + """</pubDate>
            <link>""" + DOMAIN + """/""" + output["url"] + """</link>
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

        output = parse(post, True)
        content = "<div class='post' title='Post #" + str(i) + "'>" + output["text"] + "</div><a class='back' href='.'>Back</a>"

        tags = ""

        tags += '<meta name="twitter:card" content="summary_large_image"><meta name="twitter:url" content="' + output["url"] + '">\n'
        tags += '<meta name="twitter:title" content="' + output["title"] + '">\n'
        tags += '<meta name="twitter:description" content="' + output["title"] + '">\n'
        tags += '<meta name="twitter:creator" content="@danielcdev"><meta name="twitter:site" content="@danielcdev">\n'

        if output["image"] != None:
            tags += '<meta name="twitter:image" content="' + output["image"] + '">'
            tags += '<meta property="og:image" content="' + output["image"] + '">'

        post = template(
            getIndex(),
            posts = content,
            title = output["title"],
            header = TITLE,
            tags = tags,
            top_level = "..",
        )

        os.mkdir("blog/" + output["url"])
        with open("blog/" + output["url"] + "/index.html", "w") as f:
            f.write(post)

os.system("rm -rf blog")
os.system("mkdir blog")
genFiles()
