"""
Extract Navigator theme and related components from MemoryKeeper wiki.

This script extracts:
- Navigator theme plugin
- Penguin palette
- Related stylesheets
"""

import json

# Load MemoryKeeper wiki
with open('httpsclsturgeon.github.ioMemoryKeeper.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Extract tiddler store
store_start = html.find('<script class="tiddlywiki-tiddler-store" type="application/json">') + 65
store_end = html.find('</script>', store_start)
store_json = html[store_start:store_end]
tiddlers = json.loads(store_json)

print(f"Total tiddlers in MemoryKeeper: {len(tiddlers)}")

# Find theme-related tiddlers
theme_tiddlers = []
targets = [
    '$:/themes/telmiger/navigator',
    '$:/palettes/navigator/penguin',
    '$:/theme',
    '$:/palette',
]

# Also find all tiddlers in the navigator theme plugin
for t in tiddlers:
    title = t.get('title', '')
    if any(target in title for target in targets):
        theme_tiddlers.append(t)
        print(f"Found: {title}")

print(f"\nTotal theme tiddlers found: {len(theme_tiddlers)}")

# Save to JSON for inspection
with open('navigator_theme_components.json', 'w', encoding='utf-8') as f:
    json.dump(theme_tiddlers, f, indent=2, ensure_ascii=False)

print(f"\nSaved to navigator_theme_components.json")

# Print summary
print("\n=== Theme Components Summary ===")
plugins = [t for t in theme_tiddlers if t.get('plugin-type') == 'plugin']
print(f"Plugins: {len(plugins)}")
for p in plugins:
    print(f"  - {p.get('title')} v{p.get('version', 'unknown')}")

configs = [t for t in theme_tiddlers if t.get('title', '').startswith('$:/') and 'config' in t.get('title', '').lower()]
print(f"\nConfig tiddlers: {len(configs)}")
for c in configs[:5]:
    print(f"  - {c.get('title')}")
