#!/usr/bin/env python3
"""
MinnesotaFacts Wiki Builder

This script builds a self-contained TiddlyWiki by injecting the TiddlySite
collaborative blogging plugin and custom Minnesota-themed content into a
base TiddlyWiki template.

Requirements:
    - Python 3.7+
    - empty.html (base TiddlyWiki 5.3.x template)
    - collaborative-blog-plugin.tid (TiddlySite plugin file)

Output:
    - index.html (2.5MB+ self-contained wiki with all content)

Usage:
    python build-wiki.py

The script will read empty.html, inject the plugin and content tiddlers
into the tiddler store, and write the result to index.html.
"""

import json
import re
import sys
from pathlib import Path

# Minnesota article content - using TiddlySite blog format
MINNESOTA_TIDDLERS = {
    "Home": {
        "title": "Home",
        "text": """! Minnesota Institute Research Archives

Welcome to M.I.N.N.E.S.O.T.A., documenting Minnesota's most questionable historical claims since 1923.

!! Recent Incidents and Observations

<div class="cb-post-list">
<$list filter="[tag[Post]!tag[Draft]sort[date]reverse[]limit[20]]">
<div class="cb-post-list-item">
<h3 class="cb-post-list-title"><$link to=<<currentTiddler>>><$view field="title"/></$link></h3>
<div class="cb-post-meta">
<$list filter="[<currentTiddler>has[author]]" variable="null">
<span class="cb-post-author">By <$view field="author"/></span>
</$list>
<$list filter="[<currentTiddler>has[date]]" variable="null">
<span class="cb-post-date"><$view field="date" format="date" template="DD MMM YYYY"/></span>
</$list>
</div>
<$list filter="[<currentTiddler>has[excerpt]]" variable="null">
<div class="cb-post-excerpt"><$view field="excerpt"/></div>
</$list>
<$link to=<<currentTiddler>> class="cb-read-more">Read more →</$link>
</div>
</$list>
</div>

!! About the Institute

The Minnesota Institute for Not Necessarily Evidence-Supported Observations, Theories, and Anecdotes is dedicated to preserving Minnesota's rich heritage of questionable facts, dubious claims, and thoroughly entertaining stories that may or may not have actually happened.

For more information, see our [[About]] page.
""",
        "tags": "Page"
    },
    "About": {
        "title": "About",
        "text": """! About M.I.N.N.E.S.O.T.A.

!! About M.I.N.N.E.S.O.T.A.

The Minnesota Institute for Not Necessarily Evidence-Supported Observations, Theories, and Anecdotes was founded in 1923 (or possibly 1924, records are unclear) to document and preserve Minnesota's tradition of highly questionable but thoroughly entertaining historical accounts.

!! Mission Statement

The Institute operates under the principle that factual accuracy should not obstruct a compelling narrative, particularly when said narrative involves hotdish, ice fishing, or polite lake monsters.

!! Research Standards

All articles published by M.I.N.N.E.S.O.T.A. undergo the following verification process: * Confirmation that at least two individuals have heard the story previously * Assessment via the "Minnesota Nice Test": Does it sound like something a Minnesotan would do? * Verification that the entertainment value justifies any historical inaccuracies.

!! Contact

Questions, corrections, or additional dubious Minnesota facts can be directed to the Institute's main office, located in an undisclosed church basement somewhere in the Twin Cities metropolitan area.
""",
        "tags": "Page"
    },
    "The Giant Paul Bunyan Incident of 1987": {
        "title": "The Giant Paul Bunyan Incident of 1987",
        "author": "Dr. Lars Nordstrom",
        "date": "19870704",
        "excerpt": "The controversial 1987 event when Bemidji's iconic Paul Bunyan statue allegedly came to life and began herding tourists toward the gift shop.",
        "text": """Object Class: Bemidji-Local

The Giant Paul Bunyan Incident of 1987 remains the most controversial event in Minnesota tourism history, despite efforts by the Minnesota Tourism Board to suppress all documentation of the occurrence.

!! Background

The 18-foot Paul Bunyan statue in Bemidji had been behaving normally for decades, standing stoically next to Babe the Blue Ox and posing for countless tourist photographs. However, witnesses report that on the morning of July 4th, 1987, the statue began exhibiting what can only be described as "aggressive tourist interaction patterns."

!! The Incident

According to eyewitness testimony collected by M.I.N.N.E.S.O.T.A. researchers, the statue first showed signs of animation at approximately 10:30 AM during the annual Fourth of July picnic. Mrs. Ethel Nordstrom of Bagley reported that Paul's axe began "twitching menacingly" whenever tourists attempted to pose for photos without purchasing souvenirs from the adjacent gift shop.

The situation escalated when the Bunyan statue reportedly stood up, stretched (causing several car alarms to activate from the sonic boom), and began actively herding tourists toward the gift shop while muttering something about "authentic Minnesota experiences" and "supporting local businesses."

By 11:47 AM, the statue had successfully directed an estimated 340 tourists through the gift shop checkout line before returning to its pedestal. Security footage from the incident was confiscated by the Tourism Board and has not been released to the public.

|!Date |July 4, 1987 |
|!Location |Bemidji, Minnesota |
|!Casualties |12 lawn chairs, 1 hot dog stand, 0 humans |
|!Status |Officially denied by Tourism Board |

!! Containment Procedures

Following the incident, the Bemidji Parks Department installed motion sensors around the statue's base. The statue has not moved since, though some visitors report a "judging look" when they walk past the gift shop without entering.

!! See Also

* [[The Minnesota Goodbye]]
* [[Lake Minnetonka Monster]]
""",
        "tags": "Post Featured Folklore Tourism"
    },
    "The Minnesota Goodbye": {
        "title": "The Minnesota Goodbye",
        "author": "Dr. Ingrid Olson",
        "date": "20150622",
        "excerpt": "A comprehensive study of the seven-stage ritual that makes leaving a social gathering in Minnesota a 45-minute affair.",
        "text": """Object Class: Statewide-Cultural

The Minnesota Goodbye is a complex social ritual practiced throughout the state of Minnesota, characterized by its ability to extend any social gathering by a minimum of 45 minutes to several hours beyond the initial departure announcement.

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
        "tags": "Post Featured Culture Social-Customs"
    },
    "The Great Hotdish Wars": {
        "title": "The Great Hotdish Wars",
        "author": "Chef Sven Andersson",
        "date": "19530815",
        "excerpt": "The definitive history of Minnesota's most delicious conflict: the ongoing battle over hotdish supremacy that began in 1953.",
        "text": """Object Class: Church-Basement-Level Threat

The Great Hotdish Wars refer to the ongoing series of culinary conflicts that have shaped Minnesota's social and political landscape since the early 1950s.

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
        "tags": "Post Food Culture History"
    },
    "Lake Minnetonka Monster": {
        "title": "Lake Minnetonka Monster",
        "author": "Margaret Lindström",
        "date": "19230615",
        "excerpt": "Tonka, Minnesota's most polite cryptid, always apologizes for startling boaters and waits for loons to finish fishing.",
        "text": """Object Class: Aquatic-Polite

The Lake Minnetonka Monster, affectionately known as "Tonka" by local residents, is Minnesota's most courteous cryptid.

!! Discovery and Early Sightings

The creature was first spotted on June 15, 1923, by Margaret Lindström while she was hanging laundry near the shoreline. According to her testimony, preserved in the M.I.N.N.E.S.O.T.A. archives, the creature surfaced briefly, apologized for startling her with what witnesses described as "an exceedingly polite nod," and submerged again.

!! Characteristics

|!First Sighting |June 15, 1923 |
|!Status |Politely elusive |
|!Distinguishing Features |Apologetic demeanor |
|!Habitat |Lake Minnetonka |
|!Threat Level |Minimal to none |

Unlike aggressive cryptids from other regions, Tonka has never been reported to:
* Damage property
* Frighten children (except accidentally, followed by immediate apologies)
* Disrupt fishing activities during prime hours
* Appear at inconvenient times

!! Documented Behavior Patterns

The creature demonstrates consistent Minnesota Nice characteristics:
* Surfaces exclusively during off-peak hours to avoid disturbing boaters
* Observed waiting patiently for loons to finish fishing before entering an area
* Incident Report 1923-07: Assisted in pushing a stalled pontoon boat to shore, then immediately submerged when occupants attempted to express gratitude

!! Photographic Evidence

Despite thousands of attempted photographs, Tonka has never been successfully captured on film. Researchers theorize the creature may be camera-shy and doesn't want to impose on photographers' valuable time and film resources.

!! See Also

* [[The Giant Paul Bunyan Incident of 1987]]
""",
        "tags": "Post Folklore Cryptids"
    },
    "About": {
        "title": "About",
        "text": """! About M.I.N.N.E.S.O.T.A.

The Minnesota Institute for Not Necessarily Evidence-Supported Observations, Theories, and Anecdotes was founded in 1923 (or possibly 1924, records are unclear) to document and preserve Minnesota's tradition of highly questionable but thoroughly entertaining historical accounts.

!! Mission Statement

The Institute operates under the principle that factual accuracy should not obstruct a compelling narrative, particularly when said narrative involves hotdish, ice fishing, or polite lake monsters.

!! Research Standards

All articles published by M.I.N.N.E.S.O.T.A. undergo the following verification process:
* Confirmation that at least two individuals have heard the story previously
* Assessment via the "Minnesota Nice Test": Does it sound like something a Minnesotan would do?
* Verification that the entertainment value justifies any historical inaccuracies
* Review for proper use of Minnesota cultural references

!! Personnel

The Institute employs leading experts in Minnesota folklore, including:
* Historians (credentials on file, possibly)
* Eyewitnesses with convenient recall
* Researchers who conduct field work at church basement coffee hours
* One actual academic (identity withheld by request)

!! Submissions and Correspondence

For corrections, complaints, or to submit additional dubious Minnesota stories, please send correspondence via passive-aggressive note or mention it to someone who knows someone affiliated with the Institute. We will probably hear about it eventually.

!! Legal Disclaimer

All articles are works of satire and fiction. Any resemblance to actual events, persons, hotdish recipes, or cryptids is purely coincidental and probably funnier that way.
""",
        "tags": "Page"
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
        "text": "HomePage"
    },
    "$:/config/CloudflareSaver/SaveEndpoint": {
        "title": "$:/config/CloudflareSaver/SaveEndpoint",
        "text": "https://minnesotafacts.pages.dev/save"
    },
    "$:/themes/tiddlywiki/vanilla/options/sidebarlayout": {
        "title": "$:/themes/tiddlywiki/vanilla/options/sidebarlayout",
        "text": "fixed-fluid"
    },
    "The 10,000 Lakes Recount Controversy": {
        "title": "The 10,000 Lakes Recount Controversy",
        "author": "Dr. Erik Johansen",
        "date": "20180412",
        "excerpt": "The shocking truth about Minnesota's famous lake count and the bureaucratic nightmare that ensued when someone tried to verify the number.",
        "text": """Object Class: Bureaucratic-Nightmare

In 2018, a well-meaning intern at the Minnesota Department of Natural Resources made a fateful decision: they would actually count all the lakes to verify the "Land of 10,000 Lakes" slogan.

!! The Discovery

After three months of satellite imagery analysis, GPS verification, and field surveys, the intern reported their findings: Minnesota has 11,842 lakes over 10 acres in size. The intern submitted the report with a memo suggesting updated marketing materials.

!! The Crisis

This revelation triggered what historians now call "The Great Rebranding Panic of 2018." Emergency meetings were convened. Marketing budgets were reviewed. License plates were recalled, then un-recalled when someone pointed out the cost.

The Minnesota Tourism Board convened a task force. The Department of Natural Resources issued a statement clarifying that "10,000" was "a round number for marketing purposes." The Governor's office declined to comment.

!! The Resolution

After heated debate, the Minnesota Legislature passed the "Lakes Counting Prevention Act" in a rare display of bipartisan support. The act officially defines the state lake count as "approximately 10,000, give or take a thousand or two, and we are not counting again to check."

The bill passed unanimously. No one wanted to explain to tourists why the welcome signs were wrong.

!! Current Status

The intern now works in a different department and is prohibited from counting anything larger than office supplies. Their personnel file contains a note: "Showed initiative. Do not allow near state mottos."
""",
        "tags": "Post Featured Geography Politics"
    },
    "The Great Mosquito Migration": {
        "title": "The Great Mosquito Migration",
        "author": "Dr. Astrid Bjornson",
        "date": "20190701",
        "excerpt": "Documentation of the annual phenomenon where Minnesota mosquitoes migrate in formation large enough to appear on weather radar.",
        "text": """Object Class: Airborne-Seasonal

Minnesota's mosquitoes are no ordinary insects. Every July, they engage in a synchronized migration pattern that has baffled entomologists and terrified residents since the phenomenon was first documented in 1987.

!! The Phenomenon

On July 1st (locally known as "Mosquito Independence Day"), swarms of mosquitoes lift off in perfectly choreographed formations, creating clouds visible from space and consistently mistaken for storm systems on Doppler radar.

!! Size and Scale

The 2019 migration measured approximately 2.5 miles wide and was dense enough that pilots reported needing to use windshield wipers at altitudes up to 5,000 feet.

!! Tourist Advisories

The Minnesota Tourism Board issues annual warnings:
* Outdoor events should be scheduled for before June 30th or after July 2nd
* Blood donation centers report waiting lists in late June
* The phrase "They're not that bad" is legally prohibited during migration season

!! Defense Measures

Residents have developed elaborate protocols:
* The "Double Door Entry System" (pioneered in Bemidji)
* Industrial-strength bug spray stockpiling begins in May
* Some northern communities have adopted a "stay indoors" policy for the 48-hour migration window

!! Scientific Theories

Researchers theorize the migration is:
# A coordinated feeding strategy
# An elaborate mating ritual
# Minnesota's way of keeping real estate prices reasonable
# All of the above
""",
        "tags": "Post Wildlife Nature Humor"
    },
    "The State Fair Butter Sculpture Heist": {
        "title": "The State Fair Butter Sculpture Heist",
        "author": "Detective Olaf Swanson",
        "date": "20120828",
        "excerpt": "The unsolved mystery of the Princess Kay butter sculpture that vanished during the 2012 State Fair, leaving only a puddle and a dairy-scented note.",
        "text": """Object Class: Dairy-Related-Incident

The Minnesota State Fair has featured butter sculptures since 1965, but the 2012 incident remains the most mysterious event in the Fair's 160-year history.

!! The Crime

On August 28, 2012, at approximately 2:17 AM, the newly completed butter sculpture of Princess Kay of the Milky Way vanished from its refrigerated display case. Fair security discovered the theft at 6:43 AM during routine rounds.

!! Evidence

Security footage showed:
* The refrigeration unit's temperature rising exactly 2 degrees at 2:14 AM
* A shadowy figure in what appeared to be a cheese costume
* An accomplice dressed as a very large corn dog
* Both individuals moving with what investigators described as "suspicious coordination"

!! The Note

Left at the scene was a message written in what forensic analysts confirmed was "fancy butter":

<<<
"The butter is free. Long live dairy independence."
- The Cream Liberation Front
<<<

Temperature analysis suggests the note was written between 2:15 and 2:17 AM.

!! Investigation

The Minnesota Bureau of Criminal Apprehension assigned their best agents, but the trail went cold, literally. The only lead was a report of suspicious activity at a pancake breakfast in Shakopee, which proved to be unrelated, though the pancakes were described as "unusually buttery."

Wisconsin dairy authorities denied any involvement. The Fair board issued a statement calling the incident "deeply troubling."

!! Theories

Current investigative theories include:
* Rival dairy interests from Wisconsin (officially denied by Wisconsin authorities)
* An elaborate publicity stunt (the Fair board found this theory insulting)
* Time-traveling butter enthusiasts (this theory is not officially recognized by the investigation)

!! Legacy

Security was tripled the following year. All butter sculptures now have 24/7 surveillance, armed guards, and temperature sensors accurate to .001 degrees. The Princess Kay selection process now includes a security briefing.

The sculpture was never recovered. Some say it was eaten. Others claim it is being held in a secret refrigerated facility, waiting for the right moment to return.

Case Status: Open
""",
        "tags": "Post Featured State-Fair Mystery Food"
    },
    "Hotdish vs Casserole: The Supreme Court Case": {
        "title": "Hotdish vs Casserole: The Supreme Court Case",
        "author": "Chief Justice Gunnar Erickson",
        "date": "20051214",
        "excerpt": "The landmark 2005 Minnesota Supreme Court decision that legally defined the difference between hotdish and casserole, or tried to.",
        "text": """Object Class: Legal-Culinary-Precedent

In 2005, the Minnesota Supreme Court heard ''Olson v. Lindquist'', a case that would divide the state and establish legal precedent for one of Minnesota's most contentious culinary debates.

!! The Case

Mrs. Edna Olson of St. Cloud sued her neighbor, Mrs. Doris Lindquist, for "misrepresentation of hotdish" after Mrs. Lindquist brought what she called a "hotdish" to the church potluck.

Mrs. Olson's claim: "That was clearly a casserole."

!! The Trial

The case consumed the court system for 18 months:
* 47 witnesses testified
* 127 dishes were submitted as evidence
* The courthouse cafeteria's refrigeration system was deemed inadequate
* Tater tot prices in the Twin Cities rose 34%

!! The Ruling

The Court issued a split decision (4-3) establishing the "Minnesota Hotdish Standard":

!!!Definition of Hotdish:
# Must contain a cream-based soup (preferably Campbell's)
# Must include a starch component
# Must have a protein element
# Must be prepared by someone of Minnesota or Nordic descent
# Must be capable of feeding a family of four or an entire church committee

!!!The Dissent:

Three justices argued this definition was "too narrow" and would exclude important variations like wild rice hotdish. Justice Anderson wrote: "We cannot legislate tradition. Hotdish is a state of mind, not a list of ingredients."

!! Aftermath

The decision satisfied no one:
* Legislative attempts to codify the definition failed
* Church potlucks now require dish registration forms
* The term "hotdish/casserole" has become legally acceptable in some counties

!! Current Status

The case is taught in Minnesota law schools under "Constitutional Law & Culinary Disputes." Mrs. Olson and Mrs. Lindquist still don't speak, though they attend the same church.
""",
        "tags": "Post Featured Food Culture Legal"
    },
    "The St. Paul Winter Carnival Ice Palace Incident": {
        "title": "The St. Paul Winter Carnival Ice Palace Incident",
        "author": "Fire Marshal Gustav Nordquist",
        "date": "19920204",
        "excerpt": "How the 1992 Winter Carnival ice palace accidentally became a fully functional igloo village with permanent residents.",
        "text": """Object Class: Residential-Ice-Structure

The St. Paul Winter Carnival's ice palace has been a Minnesota tradition since 1886, but the 1992 structure developed an unexpected problem: people started living in it.

!! Construction

The 1992 ice palace was the largest ever built—four stories tall with 62 rooms, ice slides, and "the best insulation we've ever achieved," according to the chief engineer.

!! The Problem

Around January 28th, security noticed unusual activity:
* Furniture being moved in
* A satellite dish installation
* Someone installing a "welcome mat" (made of ice)
* Smoke coming from what appeared to be an ice chimney

!! The Residents

Investigation revealed 17 individuals had established residence, including:
* A family of four claiming "squatter's rights"
* Two graduate students researching "alternative housing solutions"
* One man who said he "just really liked the aesthetic"
* A couple who insisted it was "better than their last apartment"

!! The Evacuation

Removing the residents proved challenging:
* They had established a lease agreement (with themselves)
* The ice palace technically met St. Paul housing codes
* Eviction proceedings required 30 days' notice
* The structure was scheduled to melt in 45 days

!! Resolution

After three weeks of negotiations, city officials reached a settlement:
* Full refund of all rent paid (amount: $0.00)
* Housing assistance for locating "more permanent permanent housing"
* Lifetime complimentary admission to all future Winter Carnivals
* Official commitment from the Parks Department to reduce ice palace livability in future construction

!! Legacy

Since 1992, ice palaces are built with:
* Intentionally poor insulation
* No convenient room divisions
* Mandatory "this will melt" signs
* Security that checks for furniture

One former resident still sends Christmas cards from their current apartment, always noting "it's not as nice."
""",
        "tags": "Post Events Winter St-Paul"
    },
    "Minnesota Nice Weather Phenomenon": {
        "title": "Minnesota Nice Weather Phenomenon",
        "author": "Meteorologist Sven Stromberg",
        "date": "20160315",
        "excerpt": "Scientific documentation of Minnesota's unique weather pattern where apologetic air masses cause excuse-me snowstorms and sorry-about-that hailstorms.",
        "text": """Object Class: Meteorological-Polite

In 2016, meteorologists at the University of Minnesota discovered something remarkable: Minnesota's weather systems exhibit polite behavior patterns not found anywhere else in the world.

!! The Discovery

After analyzing 50 years of weather data, researchers noticed unusual patterns:
* Storms that weakened when approaching populated areas
* Precipitation that seemed to apologize in Doppler radar formations
* Temperature drops that occurred "with advance notice"

!! Types of Minnesota Nice Weather

!!!The "Excuse Me" Snowstorm
Arrives exactly when predicted, deposits the promised amount of snow, and clears up on schedule. Often leaves behind a rainbow as an apology for the inconvenience.

!!!The "Sorry About That" Cold Front
Drops temperatures gradually over several days, giving residents ample time to prepare. Never arrives during major events without warning.

!!!The "Didn't Mean To" Thunderstorm
Occurs only during non-essential outdoor activities. Church services, weddings, and funerals consistently experience perfect weather, while mosquito spraying gets rained out.

!! Theoretical Framework

Lead researcher Dr. Stromberg proposes the "Cultural Meteorological Adaptation Hypothesis": "Over multiple generations of exposure to Minnesota Nice behavioral patterns, regional weather systems have adapted to exhibit similar characteristics. The atmospheric patterns have, through mechanisms not yet fully understood, acquired behavioral traits consistent with the local population."

!! Notable Examples

* The 2015 blizzard that waited until after everyone got home from work
* The 2017 heat wave that took weekends off
* The tornado of 2014 that apologized via cloud formation before touching down (no one was home at the time)

!! Comparison to Other States

Unlike Minnesota Nice Weather:
* Wisconsin weather is "friendly but competitive"
* Iowa weather is "helpful to a fault"
* North Dakota weather is "honest but brutal"

!! Current Research

Scientists are investigating whether:
* We can teach weather patterns in other states to be more polite
* Minnesota Nice Weather is related to the Canadian weather pattern migration
* This is why everyone still lives here despite the cold

!! Conclusion

"Minnesota Nice isn't just about people," concludes Dr. Stromberg. "It's literally in the air."
""",
        "tags": "Post Weather Science Culture"
    },
    "The Lutefisk Emergency of 2003": {
        "title": "The Lutefisk Emergency of 2003",
        "author": "Health Inspector Helga Magnusson",
        "date": "20031210",
        "excerpt": "When a church basement lutefisk dinner went catastrophically wrong, leading to the creation of Minnesota's Lutefisk Safety Act.",
        "text": """Object Class: Hazmat-Church-Basement

December 10, 2003, is a date that lives in infamy in the small town of Lindstrom, Minnesota. The day the annual Lutheran church lutefisk dinner became a hazmat incident.

!! The Setup

Our Savior's Lutheran Church had been hosting lutefisk dinners every December since 1923. The 2003 event was expected to serve 400 people the traditional meal of lye-soaked fish, lefse, and potatoes.

!! The Incident

At approximately 6:47 PM, something went wrong. Witnesses report:
* "A smell that went beyond the normal lutefisk smell"
* "A gelatinous wave spreading across the basement floor"
* "The potatoes gained sentience" (this witness was deemed unreliable)

!! Emergency Response

Timeline of Response:
* 6:47 PM - Initial incident report
* 6:52 PM - Lindstrom Fire Department dispatched
* 7:03 PM - First responders arrive, don hazmat gear
* 7:15 PM - Three-block radius evacuation initiated
* 7:34 PM - EPA notified
* 8:12 PM - Wisconsin offers mutual aid assistance (politely declined)

!! Root Cause Analysis

Investigation revealed:
# The lye concentration was 2.3% higher than recommended
# The soaking time exceeded guidelines by 17 hours
# Someone had added "extra soaking" for "extra tradition"
# The fish had achieved what scientists called "weaponized gelatinization"

!! The Cleanup

The basement was declared a biohazard zone. Cleanup took:
* 6 weeks
* 3 specialized contractors
* 47 gallons of industrial cleaner
* A complete replacement of all basement surfaces

!! Legislative Response

In 2004, Minnesota passed the "Lutefisk Safety and Public Health Protection Act" establishing:
* Mandatory lye concentration testing
* Required soaking time limits
* Certification for lutefisk preparers
* "Lutefisk-Free Zones" within 500 feet of schools

!! Current Status

Our Savior's Lutheran Church resumed lutefisk dinners in 2005, with:
* A certified lutefisk preparer
* Industrial ventilation
* EPA monitoring equipment
* A standing agreement with the fire department
* An ironclad insurance policy

Attendance remains strong, though participants now sign a waiver.

!! Footnote

The basement still occasionally smells like lutefisk during humid weather.
""",
        "tags": "Post Food Culture Church-Basement"
    },
    "The Great Minneapolis Skyway Getting Lost Event": {
        "title": "The Great Minneapolis Skyway Getting Lost Event",
        "author": "Urban Planning Professor Karen Swenson",
        "date": "20200118",
        "excerpt": "The 2020 incident when 47 people simultaneously got lost in the Minneapolis Skyway system during a January cold snap and were not found for three days.",
        "text": """Object Class: Urban-Navigation-Hazard

Minneapolis boasts 11 miles of climate-controlled skyways connecting 80 blocks of downtown. In January 2020, this marvel of Minnesota engineering became a humanitarian incident.

!! The Event

On January 18, 2020, temperatures dropped to -35°F. Dozens of people entered the skyway system seeking warmth. Three days later, they still hadn't emerged.

!! The Missing

47 individuals were reported missing, including:
* 23 tourists trying to find the Mall of America (which isn't connected to the skyways)
* 12 residents who "just wanted to get lunch"
* 8 people who insisted they knew a shortcut
* 4 skyway veterans who got turned around and were too proud to ask for help

!! The Search

Minneapolis Search and Rescue deployed:
* Teams with maps (which proved inadequate)
* GPS tracking (which doesn't work in skyways)
* Breadcrumb trails (eaten by pigeons)
* Local guides (who also got lost)

!! Where They Were Found

* 15 people in the Crystal Court, debating which direction was north
* 8 people in a skyway dead end, building a small community
* 12 people who'd made it to St. Paul via skyway and didn't realize it
* 7 people in the IDS Tower, convinced they were in Canada
* 5 people who had given up and started new lives in the skyway

!! Survivor Testimony

Interview Subject 14-A: "I saw the same Caribou Coffee eleven times. Eleven times. I know because I bought a muffin each time to maintain appearances."

Interview Subject 22-C: "We formed a small society. I was elected mayor of the Wells Fargo Building junction. We had by-laws and everything. Still get together for reunions."

Interview Subject 09-B: "I found shortcuts I did not know existed. I can now navigate anywhere in downtown in approximately 15 minutes, assuming I remember the route, which I do not."

!! Prevention Measures

The city implemented:
* Color-coded skyway sections
* Compass roses on floors
* "You Are Here" maps every 50 feet
* Skyway guides during extreme cold
* An emergency "I'm Lost in the Skyway" app

!! Legacy

An annual "Skyway Navigation Challenge" now tests downtown workers' wayfinding skills. The record for getting from City Center to Target is 4 minutes, 37 seconds.

The record for getting lost is 72 hours and is held by a urban planning professor, which university administrators prefer not to discuss.

!! Current Status

The skyway system remains popular, confusing, and occasionally inhabited by the temporarily lost.

Signs now read: "If you can see Canada, you've gone too far."
""",
        "tags": "Post Minneapolis Urban-Life Winter"
    }
}

def load_plugin(plugin_path):
    """
    Load TiddlySite plugin from .tid file format.

    The .tid format is:
        Header lines (key: value pairs)
        <blank line>
        Body content (JSON with plugin tiddlers)

    Args:
        plugin_path: Path object pointing to the .tid file

    Returns:
        Dictionary with plugin metadata and content, or None if invalid format
    """
    print(f"Loading plugin from {plugin_path}...")
    with open(plugin_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Split headers from body at first blank line
    parts = content.split('\n\n', 1)
    if len(parts) < 2:
        print("ERROR: Invalid plugin file format")
        return None

    # Parse header key-value pairs
    plugin_data = {}
    for line in parts[0].split('\n'):
        if ': ' in line:
            key, value = line.split(': ', 1)
            plugin_data[key] = value

    # Store body as text field - TiddlyWiki expects plugin body as text
    plugin_data['text'] = parts[1]
    plugin_data['type'] = 'application/json'

    print(f"Loaded plugin: {plugin_data.get('title', 'Unknown')} v{plugin_data.get('version', 'Unknown')}")
    return plugin_data

def inject_tiddlers(html_path, output_path, tiddlers, plugin_data=None):
    """
    Inject TiddlySite plugin and content tiddlers into base TiddlyWiki HTML.

    This function modifies the tiddler store in the HTML file by inserting
    our custom content and plugin data. The tiddler store is a JSON array
    embedded in a script tag.

    Args:
        html_path: Path to empty.html (base TiddlyWiki template)
        output_path: Path where generated index.html will be written
        tiddlers: Dictionary of content tiddlers to inject
        plugin_data: Optional plugin tiddler data (typically loaded from .tid file)

    Returns:
        True if successful, False if tiddler store not found
    """
    print(f"Reading {html_path}...")
    with open(html_path, 'r', encoding='utf-8') as f:
        html = f.read()

    # Locate the tiddler store in the HTML
    # Format: <script class="tiddlywiki-tiddler-store" type="application/json">[...]</script>
    pattern = r'<script class="tiddlywiki-tiddler-store" type="application/json">\['
    match = re.search(pattern, html)
    if not match:
        print("ERROR: Could not find tiddler store in HTML")
        return False

    # We need to inject right after the opening bracket
    insert_pos = match.end()
    print(f"Found tiddler store at position {insert_pos}")

    # Build list of tiddlers to inject
    # Plugin goes first so it loads before content
    tiddler_list = []
    if plugin_data:
        tiddler_list.append(plugin_data)
        print(f"Added plugin: {plugin_data.get('title')}")

    # Add system tiddler to set default view to Home
    tiddler_list.append({
        "title": "$:/DefaultTiddlers",
        "text": "Home"
    })

    # Add CSS variables tiddler to ensure proper layout
    tiddler_list.append({
        "title": "$:/themes/minnesota/settings",
        "tags": "$:/tags/Stylesheet",
        "text": """:root {
  --cb-sidebar-width: 280px;
  --cb-content-max-width: 1200px;
  --cb-font-body: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
  --cb-font-heading: "Georgia", serif;
  --cb-font-sans: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;

  --cb-text-primary: #2c3e50;
  --cb-text-secondary: #546e7a;
  --cb-text-meta: #95a5a6;
  --cb-text-light: #b0bec5;
  --cb-text-inverse: #ecf0f1;
  --cb-text-white: #ffffff;

  --cb-heading: #1a252f;
  --cb-heading-light: #34495e;
  --cb-accent: #3498db;
  --cb-accent-hover: #2980b9;

  --cb-bg-page: #f8f9fa;
  --cb-bg-content: #ffffff;
  --cb-bg-sidebar: #2c3e50;
  --cb-bg-featured: linear-gradient(135deg, #667eea 0%, #764ba2 100%);

  --cb-border-light: #ecf0f1;
  --cb-border-medium: #455a64;

  --cb-shadow-sm: 0 1px 3px rgba(0,0,0,0.12), 0 1px 2px rgba(0,0,0,0.24);
  --cb-shadow-md: 0 3px 6px rgba(0,0,0,0.16), 0 3px 6px rgba(0,0,0,0.23);
  --cb-shadow-lg: 0 10px 20px rgba(0,0,0,0.19), 0 6px 6px rgba(0,0,0,0.23);
  --cb-shadow-xl: 0 14px 28px rgba(0,0,0,0.25), 0 10px 10px rgba(0,0,0,0.22);
  --cb-shadow-sidebar: 2px 0 8px rgba(0,0,0,0.15);

  --cb-radius-sm: 4px;
  --cb-radius-md: 6px;
  --cb-radius-lg: 8px;
}

/* Fix page container margin for sidebar */
.tc-page-container {
  margin-left: 280px !important;
  max-width: 1200px;
  padding: 2rem;
}
"""
    })

    # Add all content tiddlers
    for data in tiddlers.values():
        tiddler_list.append(data)

    # Convert to JSON without outer array brackets (we are injecting into existing array)
    # Don't use indentation - it causes issues with newlines in string values
    # Escape forward slashes to prevent </script> from breaking HTML parsing
    tiddlers_json = json.dumps(tiddler_list, ensure_ascii=False).replace('</', '<\\/')[1:-1]
    if tiddlers_json.strip():  # Only add comma if we have content
        tiddlers_json = tiddlers_json + ','

    # Inject the tiddlers
    html_before = html[:insert_pos]
    html_after = html[insert_pos:]
    new_html = html_before + '\n' + tiddlers_json + html_after

    # Update HTML head title for SEO
    new_html = re.sub(
        r'<title>.*?</title>',
        '<title>M.I.N.N.E.S.O.T.A. - Minnesota Institute for Not Necessarily Evidence-Supported Observations, Theories, and Anecdotes</title>',
        new_html,
        count=1
    )

    # Write the result
    print(f"Writing {output_path}...")
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(new_html)

    total_count = len(tiddlers) + (1 if plugin_data else 0)
    print(f"Successfully created TiddlyWiki with {total_count} items ({len(tiddlers)} content tiddlers + plugin)")
    return True

if __name__ == '__main__':
    script_dir = Path(__file__).parent
    empty_wiki = script_dir / 'empty.html'
    output_wiki = script_dir / 'index.html'
    plugin_file = script_dir / 'collaborative-blog-plugin.tid'

    if not empty_wiki.exists():
        print(f"ERROR: {empty_wiki} not found")
        sys.exit(1)

    # Load TiddlySite plugin
    plugin_data = None
    if plugin_file.exists():
        plugin_data = load_plugin(plugin_file)
        if not plugin_data:
            print("ERROR: Failed to load plugin")
            sys.exit(1)
    else:
        print(f"Warning: Plugin file not found at {plugin_file}")

    success = inject_tiddlers(empty_wiki, output_wiki, MINNESOTA_TIDDLERS, plugin_data)
    sys.exit(0 if success else 1)
