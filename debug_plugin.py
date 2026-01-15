import json

# Load the plugin .tid file
with open('collaborative-blog-plugin.tid', 'r', encoding='utf-8') as f:
    content = f.read()

# Split headers from body
parts = content.split('\n\n', 1)

# Parse headers
plugin_data = {}
for line in parts[0].split('\n'):
    if ': ' in line:
        key, value = line.split(': ', 1)
        plugin_data[key] = value

# Store body as text field
plugin_data['text'] = parts[1]
plugin_data['type'] = 'application/json'

print("Plugin data keys:", list(plugin_data.keys()))
print("Text field length:", len(plugin_data['text']))
print("First 200 chars of text:", repr(plugin_data['text'][:200]))

# Try to JSON encode it
try:
    encoded = json.dumps(plugin_data, ensure_ascii=False)
    print("\nJSON encoding successful!")
    print("Encoded length:", len(encoded))

    # Try to decode it back
    decoded = json.loads(encoded)
    print("JSON decoding successful!")
    print("Text field preserved:", len(decoded['text']) == len(plugin_data['text']))
except Exception as e:
    print(f"\nError: {e}")
