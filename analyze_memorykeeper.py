import json

with open('httpsclsturgeon.github.ioMemoryKeeper.html', 'r', encoding='utf-8') as f:
    html = f.read()

store_start = html.find('<script class="tiddlywiki-tiddler-store" type="application/json">') + 65
store_end = html.find('</script>', store_start)
store_json = html[store_start:store_end]

obj = json.loads(store_json)
print(f'Total tiddlers: {len(obj)}')

# Find plugins
plugins = [t for t in obj if t.get('title', '').startswith('$:/plugins/')]
print(f'\nPlugins installed: {len(plugins)}')
for p in plugins[:15]:
    title = p.get('title')
    version = p.get('version', 'unknown')
    print(f'  - {title} v{version}')

# Find theme/palette settings
print('\n=== Theme Configuration ===')
palette = [t for t in obj if t.get('title', '') == '$:/palette']
if palette:
    print(f"Current palette: {palette[0].get('text', 'none')}")

theme = [t for t in obj if t.get('title', '') == '$:/theme']
if theme:
    print(f"Current theme: {theme[0].get('text', 'none')}")

# Find custom stylesheets
stylesheets = [t for t in obj if t.get('tags', '') == '$:/tags/Stylesheet']
print(f'\nCustom stylesheets: {len(stylesheets)}')
for s in stylesheets[:5]:
    print(f'  - {s.get("title")}')

# Find default tiddlers
default = [t for t in obj if t.get('title', '') == '$:/DefaultTiddlers']
if default:
    print(f'\nDefault tiddlers: {default[0].get("text", "none")}')

# Find story list (what's open)
story = [t for t in obj if t.get('title', '') == '$:/StoryList']
if story:
    print(f'\nStory list exists: Yes')
