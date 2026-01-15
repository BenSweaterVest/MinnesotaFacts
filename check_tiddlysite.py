import json
import re

with open('../TiddlySite/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

pattern = r'<script class="tiddlywiki-tiddler-store" type="application/json">\[(.*?)\]</script>'
match = re.search(pattern, html, re.DOTALL)

if match:
    store = json.loads('[' + match.group(1) + ']')
    print(f'TiddlySite has {len(store)} tiddlers')

    plugins = [t for t in store if t.get('title', '').startswith('$:/plugins/')]
    print(f'Found {len(plugins)} plugins')

    if plugins:
        plugin = plugins[0]
        print(f'\nFirst plugin: {plugin.get("title")}')
        print(f'Plugin keys: {list(plugin.keys())}')
        print(f'Has "text" field: {"text" in plugin}')
        print(f'Has "tiddlers" field: {"tiddlers" in plugin}')

        if 'text' in plugin:
            text_val = plugin['text']
            print(f'Text field type: {type(text_val)}')
            if isinstance(text_val, str):
                print(f'Text starts with: {text_val[:100]}')

        if 'tiddlers' in plugin:
            print(f'Tiddlers field type: {type(plugin["tiddlers"])}')
            print(f'Number of sub-tiddlers: {len(plugin["tiddlers"])}')
else:
    print('No tiddler store found')
