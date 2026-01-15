# Contributing to M.I.N.N.E.S.O.T.A.

Thank you for your interest in contributing to the Minnesota Institute for Not Necessarily Evidence-Supported Observations, Theories, and Anecdotes.

## Voice and Tone Guidelines

All content should maintain the established voice: a blend of SCP Foundation documentation style with Minnesota understated humor.

### Writing Style

**Do:**
- Use clinical, procedural language for incident descriptions
- Include specific timestamps and measurements
- Write in past tense for historical events
- Use "Object Class:" designations at the start of articles
- Reference official bodies (Tourism Board, Department of Natural Resources, etc.)
- Include witness testimony with interview subject codes (e.g., "Interview Subject 14-A")
- Maintain Minnesota Nice sensibility (polite, understated, passive-aggressive)

**Do Not:**
- Use emojis or excessive exclamation points
- Include em-dashes (use commas or periods instead)
- Write overly enthusiastic prose
- Use phrases like "amazingly" or "incredibly" without irony
- Include obvious jokes or punchlines (let the absurdity speak for itself)

### Minnesota Cultural Elements

Include authentic Minnesota references:
- Hotdish (not casserole, unless specifically discussing the difference)
- Church basement activities
- Ice fishing
- State Fair
- Weather complaints
- Passive-aggressive communication
- The Minnesota Goodbye
- Geographic references (Bemidji, Lake Minnetonka, Twin Cities, etc.)

### SCP-Style Formatting

Each article should include:
- **Object Class:** designation (e.g., "Object Class: Bemidji-Local")
- **Background** section with historical context
- **Incident Description** with specific timeline
- **Witness Testimony** or **Evidence** section
- **Current Status** or **Containment Procedures**
- Optional: **See Also** links to related articles

## Article Structure

### Required Metadata

```python
"Article Title": {
    "title": "Article Title",
    "author": "Dr. First Last",  # Scandinavian names preferred
    "date": "YYYYMMDD",  # 8-digit date format
    "excerpt": "One-sentence summary for homepage display.",
    "text": """Object Class: Classification-Here

    Article content...
    """,
    "tags": "Post Category1 Category2"  # Include "Post" plus 1-3 categories
}
```

### Date Formatting

Use 8-digit YYYYMMDD format:
- June 15, 1923 becomes "19230615"
- December 10, 2003 becomes "20031210"

### Tags

Always include "Post" plus relevant categories:
- **Featured** - for highlighted articles on homepage (use sparingly, max 4-5)
- **Folklore** - legends and cryptids
- **Culture** - social customs and traditions
- **Food** - culinary incidents
- **Tourism** - tourist attractions and controversies
- **Politics** - legislative and governmental matters
- **Geography** - lakes, landmarks, natural features
- **Weather** - meteorological phenomena
- **Events** - festivals, fairs, celebrations
- **Legal** - court cases and laws
- **Mystery** - unsolved incidents
- **Science** - research and studies

## Example Article Template

```python
"The [Incident Name]": {
    "title": "The [Incident Name]",
    "author": "Dr. [Scandinavian Name]",
    "date": "YYYYMMDD",
    "excerpt": "Brief one-sentence description.",
    "text": """Object Class: [Classification]

Brief introductory paragraph establishing the incident.

!! Background

Historical context and normal conditions prior to the incident.

!! The Incident

Detailed description with specific times, dates, and measurements.

Timeline if appropriate:
* HH:MM AM/PM - Event description
* HH:MM AM/PM - Response action

!! Witness Testimony / Evidence

Interview Subject XX-Y: "Direct quote from witness."

Or bullet-pointed evidence list.

!! Investigation / Response

Official response from authorities, investigation findings.

!! Current Status / Containment Procedures

Present-day situation, preventive measures in place.

!! See Also

* [[Related Article 1]]
* [[Related Article 2]]
""",
    "tags": "Post Category1 Category2"
}
```

## Submission Process

1. Fork the repository
2. Add your article to `MINNESOTA_TIDDLERS` dictionary in `build-wiki.py`
3. Follow the formatting guidelines above
4. Test build: `python build-wiki.py`
5. Verify the article appears correctly in `index.html`
6. Submit pull request with description of your addition

## Testing

Before submitting:
1. Run `python build-wiki.py`
2. Open `index.html` in a browser
3. Verify your article displays correctly
4. Check that all internal links work
5. Confirm the tone matches existing articles

## Questions?

For questions about contributing, open an issue on GitHub or submit a pull request with your proposed changes for review.

Remember: We are documenting highly questionable incidents with absolute professionalism. The humor comes from the contrast between the absurd content and the serious presentation.
