# Lessons Learned from TiddlySite Plugin Attempt

## What We Built (Previous Iteration)

### Architecture
- **Base:** TiddlyWiki 5.3.8 (empty.html)
- **Plugin:** TiddlySite collaborative-blog-plugin v2.2.0
- **Build Process:** Python script (`build-wiki.py`) that injected plugin and content into tiddler store
- **Content:** 11 Minnesota fact articles + 2 pages (Home, About)
- **Output:** Single 2.64 MB HTML file (index.html)

### Key Technical Solutions That Worked

#### 1. Plugin Loading from .tid Format
```python
def load_plugin(plugin_path):
    """Load TiddlySite plugin from .tid file."""
    with open(plugin_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Split headers from body at first blank line
    parts = content.split('\n\n', 1)

    # Parse header key-value pairs
    plugin_data = {}
    for line in parts[0].split('\n'):
        if ': ' in line:
            key, value = line.split(': ', 1)
            plugin_data[key] = value

    # Store body as text field - TiddlyWiki expects plugin body as text
    plugin_data['text'] = parts[1]
    plugin_data['type'] = 'application/json'

    return plugin_data
```

**Key insight:** TiddlyWiki plugins in the tiddler store have their JSON body stored as a STRING in the "text" field, not as nested objects.

#### 2. Critical Fix: Escaping `</script>` Tags in JSON
```python
# CRITICAL: Escape forward slashes to prevent </script> from breaking HTML parsing
tiddlers_json = json.dumps(tiddler_list, ensure_ascii=False).replace('</', '<\\/')
```

**Why this matters:** The plugin contained tiddlers with `</script>` tags in their content (analytics configuration). When embedded in HTML's `<script type="application/json">` tag, the browser sees `</script>` and thinks the script tag is closed, breaking the entire wiki.

**Solution:** Replace `</` with `<\/` which is valid JSON but doesn't close the script tag.

#### 3. Content Structure That Worked

**Blog Post Format:**
```python
{
    "title": "The Giant Paul Bunyan Incident of 1987",
    "author": "Dr. Lars Nordstrom",
    "date": "19870704",  # YYYYMMDD format
    "excerpt": "Brief summary for list view",
    "text": "Full article content...",
    "tags": "Post Featured Folklore Tourism"
}
```

**Key fields:**
- `tags: "Post"` - Required for blog plugin to recognize as post
- `date: "YYYYMMDD"` - Required format for date sorting
- `excerpt` - Shows in post lists
- `author` - Shows in post metadata

#### 4. System Tiddlers for Configuration

**Default View:**
```python
{
    "title": "$:/DefaultTiddlers",
    "text": "Home"  # Shows "Home" tiddler on startup
}
```

**Custom Styles:**
```python
{
    "title": "$:/themes/custom/settings",
    "tags": "$:/tags/Stylesheet",  # Makes it load as CSS
    "text": ":root { --variable: value; } .class { ... }"
}
```

### Problems We Encountered

#### 1. Sidebar Overlapping Content
**Issue:** TiddlySite plugin has fixed left sidebar, but CSS variables weren't loading properly
**Root cause:** Plugin's CSS uses CSS variables that weren't defined in the base wiki
**Attempted fix:** Added CSS variables tiddler, but timing/loading issues remained

#### 2. Missing HomePage Error
**Issue:** Navigation sidebar links to "Home" but we created "HomePage"
**Root cause:** Naming mismatch between plugin expectations and our tiddlers

#### 3. Complex Plugin Architecture
**Issue:** TiddlySite plugin has many nested components (ViewTemplates, Navigation, AdminPanel, etc.)
**Problem:** Hard to debug when things don't work, unclear which component is failing

#### 4. Double-Encoding Bug (SOLVED)
**Issue:** Plugin JSON was being double-encoded, causing escaped backslashes
**Solution:** Don't parse the plugin body JSON - keep it as a string in the "text" field

### Useful Content We Created

All 11 Minnesota fact articles are well-written and ready to use:
1. The Giant Paul Bunyan Incident of 1987
2. The Minnesota Goodbye
3. The Great Hotdish Wars
4. Lake Minnetonka Monster
5. The 10,000 Lakes Recount Controversy
6. The Great Mosquito Migration
7. The State Fair Butter Sculpture Heist
8. Hotdish vs Casserole: Supreme Court Case
9. St. Paul Winter Carnival Ice Palace Incident
10. Minnesota Nice Weather Phenomenon
11. The Lutefisk Emergency of 2003
12. The Great Minneapolis Skyway Getting Lost Event

**Writing style achieved:** Clinical SCP-style documentation with Minnesota cultural humor
- Object Class designations (e.g., "Object Class: Bemidji-Local")
- Interview subject codes
- Incident reports with precise timestamps
- Dry, understated tone
- No emojis, em-dashes, or AI red flags

### Build Process That Worked

```python
# 1. Load plugin from .tid file
plugin_data = load_plugin('collaborative-blog-plugin.tid')

# 2. Build tiddler list (plugin first, then system tiddlers, then content)
tiddler_list = [plugin_data, system_tiddler1, system_tiddler2, ...content]

# 3. Convert to JSON and escape script tags
tiddlers_json = json.dumps(tiddler_list, ensure_ascii=False).replace('</', '<\\/')

# 4. Inject into empty.html
# Find: <script class="tiddlywiki-tiddler-store" type="application/json">[
# Insert position: right after the '['
# Insert: newline + tiddlers_json + comma
```

### Tools We Created (Useful for Debugging)

**validate_store.py** - Validates the tiddler store JSON
```python
# Extracts and validates JSON from built wiki
# Shows where parse errors occur
```

**analyze_memorykeeper.py** - Analyzes another TiddlyWiki's structure
```python
# Lists plugins, themes, configurations
# Useful for understanding working wikis
```

## What We're Taking to the New Iteration

### Keep:
1. ✅ All 11 Minnesota fact articles (content is good!)
2. ✅ Build script approach (Python generating HTML)
3. ✅ SCP-style writing tone and format
4. ✅ Understanding of TiddlyWiki tiddler store structure
5. ✅ Knowledge of `</script>` escaping requirement
6. ✅ System tiddler configuration patterns

### Leave Behind:
1. ❌ TiddlySite blog plugin (too complex, hard to debug)
2. ❌ Current CSS approach (variables not loading correctly)
3. ❌ Blog-specific features we don't need

### New Approach:
- Start with MemoryKeeper's Navigator theme (proven to work)
- Simpler architecture - just wiki + theme + content
- Custom templates for post lists (using TiddlyWiki's native features)
- Direct GitHub saving implementation (simpler than plugin)

## File Manifest for Archive

Files to keep for reference:
- `build-wiki.py` - Full build script with working injection logic
- `collaborative-blog-plugin.tid` - The TiddlySite plugin file
- `validate_store.py` - JSON validation tool
- `analyze_memorykeeper.py` - Wiki analysis tool

Files to archive/backup:
- `index.html` - The built wiki (2.64 MB)
- `empty.html` - Base TiddlyWiki 5.3.8
- `httpsclsturgeon.github.ioMemoryKeeper.html` - Reference working wiki

## Next Steps

1. Extract Navigator theme from MemoryKeeper
2. Create fresh build script that injects:
   - Navigator theme
   - Minimal configuration
   - Our Minnesota facts (as simple tiddlers)
3. Add GitHub saving (simpler than TiddlySite's implementation)
4. Test and iterate

---

*Documentation created: 2025-01-14*
*Previous iteration: TiddlySite plugin attempt*
*Next iteration: Fresh start with Navigator theme*
