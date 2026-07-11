import os, re

from parser import parse

blogDir = "posts/"
geminiDir = "/home/daniel/gemini/"

mainPage = open(geminiDir + "index.gmi", "w+")

mainPage.write("""# Welcome to my Gemini Page.
And yes, I have no idea what I'm doing.

=> gemini://josias.dev/ Check out my friend's page

## Blog:
""")

def getMatch(a):
    return a.groups(0)[0]

# Generate main page + blog posts
files = os.listdir(blogDir + "posts/")
for i in range(len(files), 1, -1):
    fp = open(blogDir + "posts/" + str(i))
    text = fp.read()
    if text[:5] == ":skip":
        continue

    url, title, dateStr, html = parse(text, True)

    mainPage.write("=> " + url + ".gmi " + title + "\n")

    fp = open(geminiDir + url + ".gmi", "w+")
    fp.write(text)
    fp.close()

mainPage.close()
