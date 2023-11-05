import re, html

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

    text = html.escape(text)
    
    text = text.replace("\\`", "&#96;")
    text = text.replace("\\*", "&#42;")

    if showMore:
        text = text.replace("---", "<hr>")
    else:
        text = re.sub(r"---(.+)", r"<a href='/blog/" + url + "'>Read more</a>", text, flags=re.S)

    text = re.sub(r"### (.+)", r"<h3>\1</h3>", text)
    text = re.sub(r"## (.+)", r"<h2>\1</h2>", text)
    text = re.sub(r"# (.+)", r"<h1>\1</h1>", text)

    text = re.sub(r"- (.+)", r"<br>- \1", text)

    inBetween = "([^\n|\[\]\(\)]+)";

    # Images
    text = re.sub(r"\!\[([^\n|\[\]\(\)]+)\]\(([^\n|\[\]\(\)]+)\)",
        r"<a href='\2'><img width='300' src='\2' alt='\1' title='\1'></a>", text)
    
    # Links
    text = re.sub(r"(?!\!)\[([^\n|\[\]\(\)]+)\]\(([^\n|\[\]\(\)]+)\)",
        r"<a href='\2'>\1</a>", text)
    
    # Code blocks
    text = re.sub(r"```\n([^```]+)```", r"<code class='long'>\1</code>", text)
    
    # Single code blocks
    text = re.sub(r"\`([^\n`]+)\`", r"<code>\1</code>", text)
    
    # Bold, then italics
    text = re.sub(r"\*\*([^\n\*]+)\*\*", r"<b>\1</b>", text)
    text = re.sub(r"\*([^\n\*]+)\*", r"<i>\1</i>", text)
    
    text = text.replace("\n\n", "<br><br>")
    
    text = "<h1>" + title + "</h1><p>" + dateStr + "</p>" + text

    return url, title, dateStr, text
