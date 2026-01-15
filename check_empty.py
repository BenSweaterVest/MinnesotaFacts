import json
import re

with open('empty.html', 'r', encoding='utf-8') as f:
    html = f.read()

pattern = r'<script class="tiddlywiki-tiddler-store" type="application/json">\[(.*?)\]</script>'
match = re.search(pattern, html, re.DOTALL)

if match:
    store = json.loads('[' + match.group(1) + ']')
    print(f'Empty wiki has {len(store)} tiddlers')

    plugins = [t for t in store if t.get('title', '').startswith('$:/plugins/')]
    print(f'Found {len(plugins)} plugins')

    if plugins:
        plugin = plugins[0]
        print(f'\nFirst plugin: {plugin.get("title")}')
        print(f'Plugin keys: {list(plugin.keys())}')
        print(f'Has "text" field: {"text" in plugin}')
        print(f'Has "tiddlers" field: {"tiddlers" in plugin}')
else:
    print('No tiddler store found')
