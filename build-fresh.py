#!/usr/bin/env python3
"""
Fresh MinnesotaFacts Wiki Builder

Clean build using Navigator theme from MemoryKeeper.
No blog plugin - just clean TiddlyWiki + theme + content.
"""

import json
import re
from pathlib import Path

# Minnesota fact articles (preserved from old iteration)
MINNESOTA_FACTS = {
    "The Giant Paul Bunyan Incident of 1987": {
        "title": "The Giant Paul Bunyan Incident of 1987",
        "author": "Dr. Lars Nordstrom",
        "date": "19870704",
        "text": """!! Object Class: Bemidji-Local

The Giant Paul Bunyan Incident of 1987 remains the most controversial event in Minnesota tourism history.

!!! Background

The 18-foot Paul Bunyan statue in Bemidji had been behaving normally for decades. However, on July 4th, 1987, witnesses report the statue began exhibiting "aggressive tourist interaction patterns."

!!! The Incident

According to eyewitness testimony, the statue first showed signs of animation at approximately 10:30 AM. Mrs. Ethel Nordstrom of Bagley reported that Paul's axe began "twitching menacingly" whenever tourists attempted to pose without purchasing souvenirs.

The statue reportedly stood up, stretched (causing several car alarms to activate), and began herding tourists toward the gift shop while muttering about "authentic Minnesota experiences."

By 11:47 AM, an estimated 340 tourists had been directed through checkout before the statue returned to its pedestal.

|!Date |July 4, 1987 |
|!Location |Bemidji, Minnesota |
|!Casualties |12 lawn chairs, 1 hot dog stand, 0 humans |
|!Status |Officially denied by Tourism Board |

!!! Containment Procedures

The Bemidji Parks Department installed motion sensors around the statue's base. The statue has not moved since, though visitors report a "judging look" when they walk past the gift shop without entering.
""",
        "tags": "Folklore Tourism Bemidji"
    },

    "The Minnesota Goodbye": {
        "title": "The Minnesota Goodbye",
        "author": "Dr. Ingrid Olson",
        "date": "20150622",
        "text": """!! Object Class: Statewide-Cultural

The Minnesota Goodbye is a complex social ritual characterized by its ability to extend any social gathering by a minimum of 45 minutes beyond the initial departure announcement.

!!! The Seven Stages

# The Initial Announcement (5-15 minutes)
# The Stand-Up (10-20 minutes)
# The Slow Walk to the Door (5-10 minutes)
# The Door Conversation (15-30 minutes)
# The Driveway Chat (10-15 minutes)
# The Car Window Discussion (5-10 minutes)
# The Final Wave (2-5 minutes)

!!! Research Findings

Study conducted over 24 months monitoring 847 social gatherings across Minnesota documented an average Minnesota Goodbye duration of 53 minutes.

One documented case in Brainerd lasted 4 hours and 17 minutes, concluding only when temperatures dropped below -20°F.

!!! See Also

* [[The Giant Paul Bunyan Incident of 1987]]
""",
        "tags": "Culture Statewide Social-Behavior"
    }
}


def load_navigator_theme():
    """Extract Navigator theme from MemoryKeeper components."""
    with open('navigator_theme_components.json', 'r', encoding='utf-8') as f:
        components = json.load(f)

    # Find the main theme plugin
    theme = None
    for comp in components:
        if comp.get('title') == '$:/themes/telmiger/navigator':
            theme = comp
            break

    if not theme:
        print("ERROR: Navigator theme not found in components")
        return None

    print(f"Loaded Navigator theme v{theme.get('version', 'unknown')}")
    return theme


def inject_tiddlers(html_path, output_path, tiddlers_to_add):
    """Inject tiddlers into base TiddlyWiki HTML."""
    print(f"Reading {html_path}...")
    with open(html_path, 'r', encoding='utf-8') as f:
        html = f.read()

    # Find tiddler store
    pattern = r'<script class="tiddlywiki-tiddler-store" type="application/json">\['
    match = re.search(pattern, html)
    if not match:
        print("ERROR: Could not find tiddler store")
        return False

    insert_pos = match.end()
    print(f"Found tiddler store at position {insert_pos}")

    # Convert to JSON and escape </script> tags
    tiddlers_json = json.dumps(tiddlers_to_add, ensure_ascii=False).replace('</', '<\\/')
    # Remove outer array brackets (we're injecting into existing array)
    tiddlers_json = tiddlers_json[1:-1]
    if tiddlers_json.strip():
        tiddlers_json = tiddlers_json + ','

    # Inject
    html_before = html[:insert_pos]
    html_after = html[insert_pos:]
    new_html = html_before + '\n' + tiddlers_json + html_after

    # Write result
    print(f"Writing {output_path}...")
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(new_html)

    print(f"Successfully created wiki with {len(tiddlers_to_add)} tiddlers")
    return True


def main():
    """Build fresh MinnesotaFacts wiki."""
    print("=" * 60)
    print("Building Fresh MinnesotaFacts Wiki")
    print("=" * 60)

    # Load Navigator theme
    theme = load_navigator_theme()
    if not theme:
        return 1

    # Build tiddler list
    tiddlers = []

    # 1. Navigator theme plugin
    tiddlers.append(theme)

    # 2. Set Navigator as active theme
    tiddlers.append({
        "title": "$:/theme",
        "text": "$:/themes/telmiger/navigator"
    })

    # 3. Set default tiddlers (homepage)
    tiddlers.append({
        "title": "$:/DefaultTiddlers",
        "text": "Home"
    })

    # 4. Create homepage with fact list
    tiddlers.append({
        "title": "Home",
        "text": """! Minnesota Institute Research Archives

Welcome to M.I.N.N.E.S.O.T.A. - the Minnesota Institute for Not Necessarily Evidence-Supported Observations, Theories, and Anecdotes.

!! Recent Documented Phenomena

<div class="tc-table-of-contents">
<<list-links "[tag[]]!tag[Exclude]sort[date]reverse[]">>
</div>

---

''About:'' Founded in 1923 (or possibly 1924, records are unclear) to document and preserve Minnesota's tradition of highly questionable but thoroughly entertaining historical accounts.
""",
        "tags": ""
    })

    # 5. Add all Minnesota facts
    for fact_data in MINNESOTA_FACTS.values():
        tiddlers.append(fact_data)

    # 6. Site title
    tiddlers.append({
        "title": "$:/SiteTitle",
        "text": "M.I.N.N.E.S.O.T.A."
    })

    tiddlers.append({
        "title": "$:/SiteSubtitle",
        "text": "Minnesota Institute for Not Necessarily Evidence-Supported Observations, Theories, and Anecdotes"
    })

    # Inject into empty.html
    success = inject_tiddlers(
        'empty.html',
        'index-fresh.html',
        tiddlers
    )

    if success:
        print("\n" + "=" * 60)
        print("SUCCESS! Open index-fresh.html in your browser")
        print("=" * 60)
        return 0
    else:
        print("\nBuild failed")
        return 1


if __name__ == '__main__':
    exit(main())
