import json

# Load the plugin
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

# Create a simple tiddler
simple_tiddler = {
    "title": "Test",
    "text": "Hello world",
    "tags": "Post"
}

# Create the list
tiddler_list = [plugin_data, simple_tiddler]

# Encode as JSON
try:
    full_json = json.dumps(tiddler_list, ensure_ascii=False)
    print(f"Full JSON length: {len(full_json)}")

    # Try to decode
    decoded = json.loads(full_json)
    print(f"Decoded successfully: {len(decoded)} items")

    # Save to file
    with open('test_output.json', 'w', encoding='utf-8') as f:
        f.write(full_json)
    print("Saved to test_output.json")

except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
