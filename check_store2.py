import sys
import codecs

# Set stdout to UTF-8
sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')

with open('empty.html', 'r', encoding='utf-8') as f:
    html = f.read()

start = html.find('<script class="tiddlywiki-tiddler-store"')
end = start + 300
snippet = html[start:end]

# Only print ASCII-safe version
print(repr(snippet))
