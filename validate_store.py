import json

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

store_start = content.find('<script class="tiddlywiki-tiddler-store" type="application/json">') + 65
store_end = content.find('</script>', store_start)
store_json = content[store_start:store_end]

print(f'Store length: {len(store_json)}')
print(f'First 100 chars: {store_json[:100]}')
print(f'Last 100 chars: {store_json[-100:]}')

try:
    obj = json.loads(store_json)
    print(f'\nSUCCESS: Valid JSON with {len(obj)} items!')
except json.JSONDecodeError as e:
    print(f'\nERROR: {e}')
    print(f'Error at position {e.pos}')
    print(f'Context: {repr(store_json[max(0, e.pos-50):e.pos+50])}')
