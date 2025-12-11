#!/usr/bin/env python3
"""
Build MinnesotaFacts TiddlyWiki with custom content and Cloudflare saver
"""

import json
import re
import sys
from pathlib import Path

# Minnesota article content
MINNESOTA_TIDDLERS = {
    "GettingStarted": {
        "title": "GettingStarted",
        "text": """! Welcome to M.I.N.N.E.S.O.T.A.

''M.I.N.N.E.S.O.T.A.'' (Minnesota Institute for Not Necessarily Evidence-Supported Observations, Theories, and Anecdotes) is the premier research institution dedicated to documenting Minnesota's most important cultural phenomena, historical events, and legendary figures—regardless of their verifiability.

!! Our Mission

The Institute is committed to preserving and sharing Minnesota's rich heritage of questionable facts, dubious claims, and thoroughly entertaining stories that may or may not have actually happened. We believe that truth is less important than a good story, especially when that story involves hotdish.

!! Featured Research

* [[The Giant Paul Bunyan Incident of 1987]]
* [[The Minnesota Goodbye]]
* [[The Great Hotdish Wars]]
* [[Lake Minnetonka Monster]]

!! About Our Research Methods

The Institute employs rigorous* research methodologies to ensure the authenticity** of all documented phenomena. Our findings have been thoroughly peer-reviewed*** by leading experts**** in the field of Minnesota studies.

<<<
*Rigorous: We ask at least two people if they've heard the story

**Authenticity verified through the "Minnesota Nice Test": Does it sound like something a Minnesotan would do?

***Peer review conducted at coffee shops, church basements, and ice fishing houses

****Experts: Individuals who have survived more than three Minnesota winters and can pronounce "Wayzata" correctly
<<<
""",
        "tags": ""
    },
    "The Giant Paul Bunyan Incident of 1987": {
        "title": "The Giant Paul Bunyan Incident of 1987",
        "text": """The ''Giant Paul Bunyan Incident of 1987'' remains the most controversial event in Minnesota tourism history, despite efforts by the Minnesota Tourism Board to suppress all documentation of the occurrence.

!! Background

The 18-foot Paul Bunyan statue in Bemidji had been behaving normally for decades, standing stoically next to Babe the Blue Ox and posing for countless tourist photographs. However, witnesses report that on the morning of July 4th, 1987, the statue began exhibiting what can only be described as "aggressive tourist interaction patterns."

!! The Incident

According to eyewitness testimony collected by M.I.N.N.E.S.O.T.A. researchers, the statue first showed signs of animation at approximately 10:30 AM during the annual Fourth of July picnic. Mrs. Ethel Nordstrom of Bagley reported that Paul's axe began "twitching menacingly" whenever tourists attempted to pose for photos without purchasing souvenirs from the adjacent gift shop.

The situation escalated rapidly when the Bunyan statue reportedly stood up, stretched (causing several car alarms to activate from the sonic boom), and began actively herding tourists toward the gift shop while muttering something about "authentic Minnesota experiences" and "supporting local businesses."

|!Date |July 4, 1987 |
|!Location |Bemidji, Minnesota |
|!Casualties |12 lawn chairs, 1 hot dog stand |
|!Status |Covered up by Big Tourism |

!! See Also

* [[The Minnesota Goodbye]]
* [[Lake Minnetonka Monster]]
""",
        "tags": "Articles"
    },
    "The Minnesota Goodbye": {
        "title": "The Minnesota Goodbye",
        "text": """The ''Minnesota Goodbye'' is a complex social ritual practiced throughout the state of Minnesota, characterized by its ability to extend any social gathering by a minimum of 45 minutes to several hours beyond the initial departure announcement.

!! Definition and Characteristics

Unlike the abrupt departures common in other regions, the Minnesota Goodbye follows a strict protocol that ensures no one's feelings are hurt and that all participants have multiple opportunities to share additional anecdotes, weather observations, and casserole recipes.

!! The Seven Stages

!!! Stage 1: The Initial Announcement (5-15 minutes)

The departing party announces their intention to leave, usually prefaced with observations about the time, weather, or upcoming obligations.

!!! Stage 2: The Coat Gathering Ceremony (10-20 minutes)

Participants begin the ritual collection of coats, purses, and casserole dishes. This stage often triggers new conversations about the weather, road conditions, or whose dish is whose.

!!! Stage 3: The Doorway Lingering (15-30 minutes)

The group migrates to the entryway but makes no actual move toward the door. Topics discussed typically include weekend plans, traffic patterns, and spontaneous recipe exchanges.

!!! Stage 4: The First Outdoor Migration (10-20 minutes)

The party finally makes it outside but remains on the porch or in the driveway. Conversation shifts to lawn care, seasonal observations, and vehicle maintenance.

!!! Stage 5: The Vehicle Approach (5-15 minutes)

Movement toward vehicles begins, but participants maintain conversation across increasing distances, often shouting to be heard.

!!! Stage 6: The Car Door Open Position (10-20 minutes)

One foot in the vehicle, one foot out, maintaining eye contact and conversation while the engine may or may not be running.

!!! Stage 7: The Final Wave Sequence (5-10 minutes)

Multiple rounds of waving through windows while slowly backing out of the driveway, with periodic stops for additional waves.

!! See Also

* [[The Great Hotdish Wars]]
""",
        "tags": "Articles"
    },
    "The Great Hotdish Wars": {
        "title": "The Great Hotdish Wars",
        "text": """The ''Great Hotdish Wars'' refer to the ongoing series of culinary conflicts that have shaped Minnesota's social and political landscape since the early 1950s.

!! Historical Background

The conflict began innocuously in 1953 when Marge Olson of Hibbing claimed at the annual Lutheran church potluck that her tater tot hotdish was "the best in the Range." This bold assertion was immediately challenged by Betty Lindstrom of Virginia, who maintained that her tuna noodle hotdish held that honor.

!! Major Campaigns

!!! The Tater Tot Offensive (1953-1967)

The introduction of commercially produced tater tots in 1953 revolutionized hotdish warfare. The crispy potato cylinders became the ammunition of choice for hotdish strategists across the state.

!!! The Cream of Mushroom Soup Debates (1968-1985)

Fierce disagreements erupted over the acceptable ratio of cream of mushroom soup to other ingredients. Some factions insisted on a 1:1 ratio, while hardliners demanded 2:1.

!!! The Great Casserole Schism (1986-Present)

The question of whether hotdish and casserole are synonymous terms split Minnesota families and church congregations. Some maintain that all hotdishes are casseroles, but not all casseroles are hotdishes.

!! Current Status

The wars continue to this day, with new frontiers opening around questions of:
* Acceptable cheese types and melting points
* The role of green bean casserole as a hotdish variant
* Whether hotdish can be served in non-rectangular vessels

!! See Also

* [[The Minnesota Goodbye]]
* [[Lake Minnetonka Monster]]
""",
        "tags": "Articles"
    },
    "Lake Minnetonka Monster": {
        "title": "Lake Minnetonka Monster",
        "text": """The ''Lake Minnetonka Monster'', affectionately known as "Tonka" by local residents, is Minnesota's most courteous cryptid.

!! Discovery and Early Sightings

The creature was first spotted on June 15, 1923, by Margaret Lindström while she was hanging laundry near the shoreline. According to her testimony, preserved in the M.I.N.N.E.S.O.T.A. archives, the creature surfaced briefly, apologized for startling her with what witnesses described as "an exceedingly polite nod," and submerged again.

!! Characteristics

|!First Sighting |June 15, 1923 |
|!Status |Politely elusive |
|!Distinguishing Features |Apologetic demeanor |
|!Habitat |Lake Minnetonka |

Unlike aggressive cryptids from other regions, Tonka has never been reported to:
* Damage property
* Frighten children (except accidentally, followed by immediate apologies)
* Disrupt fishing activities during prime hours
* Appear at inconvenient times

!! Notable Behavior Patterns

The creature demonstrates remarkable Minnesota Nice characteristics:
* Always surfaces during off-peak hours to avoid disturbing boaters
* Has been observed waiting patiently for loons to finish fishing before entering an area
* Reportedly once helped push a stalled pontoon boat to shore (though it immediately submerged when the grateful boaters tried to thank it)

!! Photographic Evidence

Despite thousands of attempted photographs, Tonka has never been successfully captured on film. Researchers theorize the creature may be camera-shy and doesn't want to impose on photographers' valuable time and film resources.

!! See Also

* [[The Giant Paul Bunyan Incident of 1987]]
""",
        "tags": "Articles"
    },
    "$:/SiteTitle": {
        "title": "$:/SiteTitle",
        "text": "M.I.N.N.E.S.O.T.A."
    },
    "$:/SiteSubtitle": {
        "title": "$:/SiteSubtitle",
        "text": "Minnesota Institute for Not Necessarily Evidence-Supported Observations, Theories, and Anecdotes"
    },
    "$:/DefaultTiddlers": {
        "title": "$:/DefaultTiddlers",
        "text": "GettingStarted"
    },
    "$:/config/CloudflareSaver/SaveEndpoint": {
        "title": "$:/config/CloudflareSaver/SaveEndpoint",
        "text": "https://minnesotafacts.pages.dev/save"
    }
}

def inject_tiddlers(html_path, output_path, tiddlers):
    """Inject custom tiddlers into TiddlyWiki HTML"""
    print(f"Reading {html_path}...")
    with open(html_path, 'r', encoding='utf-8') as f:
        html = f.read()

    # Find the tiddler store - it's a JSON array starting with [
    pattern = r'<script class="tiddlywiki-tiddler-store" type="application/json">\['
    match = re.search(pattern, html)
    if not match:
        print("ERROR: Could not find tiddler store in HTML")
        return False

    # Position right after the opening bracket [
    insert_pos = match.end()
    print(f"Found tiddler store at position {insert_pos}")

    # Convert tiddlers dict to list of tiddler objects
    tiddler_list = []
    for data in tiddlers.values():
        tiddler_list.append(data)

    # Create JSON for new tiddlers (without outer array brackets)
    tiddlers_json = json.dumps(tiddler_list, ensure_ascii=False, indent=0)[1:-1]
    # Add comma after our tiddlers
    tiddlers_json = tiddlers_json + ','

    # Inject tiddlers right after the opening bracket
    html_before = html[:insert_pos]
    html_after = html[insert_pos:]

    new_html = html_before + '\n' + tiddlers_json + html_after

    # Update title and subtitle in HTML head
    new_html = re.sub(
        r'<title>.*?</title>',
        '<title>M.I.N.N.E.S.O.T.A. - Minnesota Institute for Not Necessarily Evidence-Supported Observations, Theories, and Anecdotes</title>',
        new_html,
        count=1
    )

    print(f"Writing {output_path}...")
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(new_html)

    print(f"Successfully created TiddlyWiki with {len(tiddlers)} custom tiddlers")
    return True

if __name__ == '__main__':
    script_dir = Path(__file__).parent
    empty_wiki = script_dir / 'empty.html'
    output_wiki = script_dir / 'index.html'

    if not empty_wiki.exists():
        print(f"ERROR: {empty_wiki} not found")
        sys.exit(1)

    success = inject_tiddlers(empty_wiki, output_wiki, MINNESOTA_TIDDLERS)
    sys.exit(0 if success else 1)
