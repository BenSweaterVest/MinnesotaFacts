# M.I.N.N.E.S.O.T.A.

Minnesota Institute for Not Necessarily Evidence-Supported Observations, Theories, and Anecdotes

A satirical documentation project cataloging Minnesota's most entertaining and questionable cultural phenomena, presented in an SCP Foundation-style format.

## Overview

This repository contains a TiddlyWiki-based documentation site presenting fictional Minnesota incidents, cultural phenomena, and folklore in the style of SCP Foundation entries. All content is satirical and intended solely for entertainment purposes.

The project combines:
- SCP Foundation-style documentation formatting
- Minnesota cultural references and understated humor
- Professional blogging interface via TiddlySite plugin
- Self-contained single-file wiki architecture

## Project Structure

```
MinnesotaFacts/
├── build-wiki.py              # Build script for generating the wiki
├── empty.html                 # Base TiddlyWiki 5.3.x template (2.5MB)
├── index.html                 # Generated output wiki (2.7MB)
├── collaborative-blog-plugin.tid  # TiddlySite blogging plugin (124KB)
├── plugins/                   # Plugin source files
│   └── collaborative-blog/
└── functions/                 # Cloudflare Pages Functions
    ├── save.js               # Save handler for wiki updates
    └── api/
        └── auth.js           # Authentication endpoint
```

## Building the Wiki

### Requirements

- Python 3.7 or later
- No external Python dependencies required (uses only standard library)

### Build Process

```bash
python build-wiki.py
```

This will:
1. Load the TiddlySite plugin from `collaborative-blog-plugin.tid`
2. Inject 13 content pages (1 homepage, 1 about page, 11 articles)
3. Write the output to `index.html`

The output file is a self-contained single HTML file that can be opened in any modern web browser.

## Content

The wiki documents 11 incidents and phenomena, including:

**Featured Articles:**
- The Giant Paul Bunyan Incident of 1987 (Object Class: Bemidji-Local)
- The Minnesota Goodbye (Object Class: Statewide-Cultural)
- The Great Hotdish Wars (Object Class: Church-Basement-Level Threat)
- Lake Minnetonka Monster (Object Class: Aquatic-Polite)
- The 10,000 Lakes Recount Controversy (Object Class: Bureaucratic-Nightmare)
- The State Fair Butter Sculpture Heist (Object Class: Dairy-Related-Incident)

**Additional Documentation:**
- Hotdish vs Casserole: The Supreme Court Case
- The St. Paul Winter Carnival Ice Palace Incident
- Minnesota Nice Weather Phenomenon
- The Lutefisk Emergency of 2003
- The Great Minneapolis Skyway Getting Lost Event

Each entry uses SCP-style "Object Class" designations, incident timelines, witness testimony, and containment procedures, all filtered through Minnesota sensibility.

## Deployment

### Local Use

Simply open `index.html` in a web browser after building.

### Cloudflare Pages

The site is configured for deployment to Cloudflare Pages at `https://minnesotafacts.pages.dev/`

Environment variables required:
- `SAVE_PASSWORD` - Password for wiki editing
- `GITHUB_TOKEN` - GitHub API token for save functionality
- `GITHUB_REPO` - Repository name (format: owner/repo)
- `FILE_PATH` - Path to index.html in repository
- `GITHUB_BRANCH` - Target branch (typically main)

## Features

- WordPress-style blogging interface via TiddlySite plugin
- 5 professional themes (Historical Society, Modern Minimalist, Dark Mode, Vibrant Creative, Professional Business)
- Full-text search functionality
- Category and tag-based organization
- Mobile-responsive design
- Automatic GitHub save integration when deployed

## Technical Details

### TiddlyWiki Version

Built on TiddlyWiki 5.3.8

### TiddlySite Plugin

Version 2.2.0 with 34 core tiddlers providing:
- Blog post view templates
- Navigation and admin panel
- Theme system
- Search functionality
- Analytics integration support
- Cloudflare saver modules

### Build Script

The `build-wiki.py` script uses regex pattern matching to locate the tiddler store in the HTML and inject JSON-formatted tiddlers. The plugin is loaded first to ensure it initializes before content.

## License

This project follows the BSD 3-Clause License (same as TiddlyWiki).

## Disclaimer

All articles are works of satire and fiction. Any resemblance to actual events, persons, hotdish recipes, or cryptids is purely coincidental.

The Minnesota Institute for Not Necessarily Evidence-Supported Observations, Theories, and Anecdotes is a fictional organization. Please do not send research funding.

## Contributing

If you have your own dubious Minnesota stories to contribute, you can:
1. Fork the repository
2. Add your content to the `MINNESOTA_TIDDLERS` dictionary in `build-wiki.py`
3. Follow the existing format (include author, date, excerpt, tags, and Object Class)
4. Submit a pull request

Ensure your content maintains the Minnesota Nice tone while following SCP-style formatting conventions.
