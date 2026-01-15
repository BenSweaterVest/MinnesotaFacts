with open('empty.html', 'r', encoding='utf-8') as f:
    html = f.read()

start = html.find('<script class="tiddlywiki-tiddler-store"')
end = html.find('</script>', start)
print(html[start:end+9])
