import sys
from html.parser import HTMLParser

class MyHTMLParser(HTMLParser):
    def __init__(self, *, convert_charrefs=True):
        super().__init__(convert_charrefs=True)
        self.current_url = None
        self.bookmarks = dict()

    def handle_starttag(self, tag, attrs):
        if tag == "a":
            for x,y in attrs:
                if x == "href":
                    self.current_url = y
                    self.bookmarks[y] = dict()

                if x == "time_added":
                    if self.current_url is None:
                        print("ERROR time_added, current_url = None")
                        return
                    
                    if "time_added" not in self.bookmarks[self.current_url].keys():
                        self.bookmarks[self.current_url]["time_added"] = y

                if x == "tags":
                    if self.current_url is None:
                        print("ERROR tags, current_url = None")
                        return

                    if "tags" not in self.bookmarks[self.current_url].keys():
                        self.bookmarks[self.current_url]["tags"] = list()

                    for x in y.split(','):
                        self.bookmarks[self.current_url]["tags"].append(x)

    def handle_data(self, data):
        if self.current_url is not None:
            self.bookmarks[self.current_url]["label"] = data

    def handle_endtag(self, tag):
        self.current_url = None

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Feed me a Pocket Bookmark HTML file.\n")
        print(f"Typical usage: {sys.argv[0]} pocket.html > bookmarks.html")
        sys.exit()

    f = open(sys.argv[1], "r")
    parser = MyHTMLParser()
    parser.feed(f.read())

    data = dict()
    data["Bookmarks_bar"] = list()
    
    for url in parser.bookmarks.keys():
        if "tags" not in parser.bookmarks[url].keys():
            data["Bookmarks_bar"].append(url)
        else:
            for tag in parser.bookmarks[url]["tags"]:
                if tag not in data.keys():
                    data[tag] = list()

                data[tag].append(url)

    print("<!DOCTYPE NETSCAPE-Bookmark-file-1>")
    print("<META HTTP-EQUIV=\"Content-Type\" CONTENT=\"text/html; charset=UTF-8\">")
    print("<TITLE>Bookmarks</TITLE>")
    print("<H1>Bookmarks</H1>")
    print("<DL><p>")

    for tag in data.keys():
        if tag == "Bookmarks_bar":
            print("    <DT><H3 PERSONAL_TOOLBAR_FOLDER=\"true\">Bookmarks bar</H3>")
        else:
            print(f"    <DT><H3>{tag}</H3>")

        print("    <DL><p>")

        for url in data[tag]:
            time_added = parser.bookmarks[url]["time_added"]
            label = parser.bookmarks[url]["label"]
            print(f"        <DT><A HREF=\"{url}\" ADD_DATE=\"{time_added}\">{label}</A>")

        print("    </DL><p>")

    print("</DL><p>")
