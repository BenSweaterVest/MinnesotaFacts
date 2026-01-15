import json
import re

# Simulated empty HTML
empty_html = '''<html>
<script class="tiddlywiki-tiddler-store" type="application/json">[
{"title":"$:/core","text":"existing"}
]</script>
</html>'''

# Find injection point
pattern = r'<script class="tiddlywiki-tiddler-store" type="application/json">\['
match = re.search(pattern, empty_html)
insert_pos = match.end()
print(f"Insert position: {insert_pos}")
print(f"Char at insert_pos: {repr(empty_html[insert_pos])}")

# Create data to inject
plugin = {'title': '$:/plugins/test', 'text': '{"foo":"bar"}'}
content = {'title': 'MyPost', 'text': 'Content'}
tiddler_list = [plugin, content]

# Encode and strip brackets
tiddlers_json = json.dumps(tiddler_list, ensure_ascii=False)[1:-1]
tiddlers_json = tiddlers_json + ','

# Inject
html_before = empty_html[:insert_pos]
html_after = empty_html[insert_pos:]
new_html = html_before + '\n' + tiddlers_json + html_after

print("\nResult:")
print(new_html)

# Extract and validate
store_start = new_html.find('>[') + 1  # Include the '['
store_end = new_html.find(']</script>')
store_json = new_html[store_start:store_end+1]

print("\nExtracted store:")
print(store_json[:200])

try:
    decoded = json.loads(store_json)
    print(f"\nValid JSON with {len(decoded)} items!")
except Exception as e:
    print(f"\nError: {e}")
