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
    url = ""
    dateStr = ""

    lines = text.split("\n")

    # post metadata length in lines
    metadataLength = 0

    # Parse custom url if present
    if text[0] == ":":
        url = lines[0][1:]
        metadataLength += 1
    else:
        url = sanitizeTitle(lines[metadataLength])
    
    title = lines[metadataLength]
    metadataLength += 1

    dateStr = lines[metadataLength]
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
        text = re.sub(r"---(.+)", r"<a href='" + url + "'>Read more</a>", text, flags=re.S)

    # images
    text = re.sub(r"\!\[([^\n|\[\]\(\)]+)\]\(([^\n|\[\]\(\)]+)\)", r"<a href='\2'><img width='300' src='\2' alt='\1' title='\1'></a>", text)

    # Code blocks
#    text = re.sub(r"```\n([^```]+)```", r"<code class='long'>\1</code>", text)

    text = markdown.markdown(text, extensions=['fenced_code'])

    text = "<h1>" + title + "</h1><p>" + dateStr + "</p>" + text

    return url, title, dateStr, text
