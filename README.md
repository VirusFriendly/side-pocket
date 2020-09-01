I made this tool so I can move pocket bookmarks between accounts
But I guess you could also use it to important pocket bookmarks into your browser

Pocket supports importing from:
* Browsers that output in a Netscape Compatible Format
* Readability
* Xmarks
* Instapaper
* Delicious

But NOT Pocket

# How to Use
To export your pocket bookmarks go to:  https://getpocket.com/export

Save the exported pocket bookmarks as "pocket.html"

Then run `python side-pocket.py pocket.html > bookmarks.html`

Go to https://getpocket.com/import/browser and upload bookmarks.html

