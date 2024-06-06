from main import *

# Route legacy index.php
@route("/index.php")
def main():
    if request.params.get('post') is not None:
        redirect(getPostByID(request.query["post"]))
    redirect("/")

@route("/")
def main():
    # parse index ?post=x
    if request.params.get('post') is not None:
        redirect(getPostByID(request.query["post"]))

    return genMainPage()

@route("/<post>")
def post(post):
    title, content = getPost(post)
    return template(
        getIndex(),
        posts=content,
        title=title,
        header="Daniel's stuff"
    )

@route("/rss.xml")
def rss():
    response.content_type = "text/xml; charset=utf-8"
    return genRss()

run(host='localhost', port=7000)
