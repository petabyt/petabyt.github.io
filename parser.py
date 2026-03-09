import re, html
import markdown

def getMatch(a):
    return a.groups(0)[0]

def sanitizeTitle(title):
    title = title.lower()
    title = re.sub(r'[^a-z 0-9/-]', '', title)
    title = title.replace(" ", "-")
    title = title.replace("/", "-")
    return title

# Parse as tbmd, a very special version of markdown
# return url, date, text
def parse(text, showMore):
    output = {
        "url": None,
        "title": "",
        "date": "",
        "image": None,
        "text": "",
    }

    lines = text.split("\n")

    # post metadata length in lines
    metadataLength = 0

    # First few lines of text can have metadata properties
    for i in range(2):
        if lines[i][0] == ":":
            output["url"] = lines[i][1:]
        elif lines[i][0:4] == "img:":
           output["image"] = lines[i][4:]
        else:
            break
        metadataLength += 1

    # Require title and date line after metadata
    output["title"] = lines[metadataLength]
    if output["url"] == None:
        output["url"] = sanitizeTitle(output["title"])
    metadataLength += 1

    output["date"] = lines[metadataLength]
    metadataLength += 1

    # Set offset to whatever is after metadata
    offset = 0
    for i in range(0, metadataLength):
        offset += len(lines[i]) + 1

    # Skip trailing whitespace
    while text[offset] == "\n" or text[offset] == " ":
        offset += 1

    text = text[offset:]

    text = text.replace("\\`", "&#96;")
    text = text.replace("\\*", "&#42;")

    if showMore:
        text = text.replace("---", "<hr>")
    else:
        text = re.sub(r"---(.+)", r"<a href='" + output["url"] + "'>Read more</a>", text, flags=re.S)

    # images
    text = re.sub(r"\!\[([^\n|\[\]\(\)]+)\]\(([^\n|\[\]\(\)]+)\)", r"<a href='\2'><img width='300' src='\2' alt='\1' title='\1'></a>", text)

    # Code blocks
#    text = re.sub(r"```\n([^```]+)```", r"<code class='long'>\1</code>", text)

    text = markdown.markdown(text, extensions=['fenced_code', 'footnotes'])

    output["text"] = "<h1>" + output["title"] + "</h1><p>" + output["date"] + "</p>" + text

    return output
