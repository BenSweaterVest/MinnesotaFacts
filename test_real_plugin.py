import json

# Load plugin
with open('collaborative-blog-plugin.tid', 'r', encoding='utf-8') as f:
    content = f.read()

parts = content.split('\n\n', 1)
plugin_data = {}
for line in parts[0].split('\n'):
    if ': ' in line:
        key, value = line.split(': ', 1)
        plugin_data[key] = value

plugin_data['text'] = parts[1]
plugin_data['type'] = 'application/json'

# Create simple tiddler
simple = {'title': 'Test', 'text': 'Hello', 'tags': 'Post'}

# Create array
tiddler_list = [plugin_data, simple]

# Encode full array
full_json = json.dumps(tiddler_list, ensure_ascii=False)
print(f"Full JSON length: {len(full_json)}")

# Strip brackets
stripped = full_json[1:-1]
print(f"Stripped length: {len(stripped)}")

# Save both
with open('test_full.json', 'w', encoding='utf-8') as f:
    f.write(full_json)

with open('test_stripped.txt', 'w', encoding='utf-8') as f:
    f.write(stripped)

# Try to decode full
try:
    json.loads(full_json)
    print("Full JSON is valid")
except Exception as e:
    print(f"Full JSON error: {e}")

# Try to decode stripped with brackets added back
try:
    json.loads('[' + stripped + ']')
    print("Stripped JSON (with brackets) is valid")
except Exception as e:
    print(f"Stripped JSON error: {e}")
