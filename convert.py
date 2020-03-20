"""
Script to convert Trello JSON data to user story template format.

Story attributes:
- Story title
- Story ID
- Priority
- Story points
- Story body
- Acceptance criteria
- Notes

Trello card format:
"(<story-points>) <title>: <story body>"
e.g. "(2) Basic Entry Form: As a potential customer, I want to..."

Trello description format:
"
## Acceptance Criteria
- <criterion-1> 
- <criterion-2>
...
- <criterion-n> 

## Notes
- <note-1>
- <note-2>
...
- <note-n> 
"

- Specify priority with lists
- Add role as a tag (not a part of template)

JSON fields:
- desc - Description (acceptance criteria and notes)
- name - Story content (points, title and body)
"""

import slides

from dataclasses import dataclass
import sys
import json
from typing import List, Dict
import re


PRIORITIES = {
    "Must Have": "M",
    "Should Have": "S",
    "Could Have": "C",
    "Won't Have": "W",
}


CARD_PATTERN = r"\(([0-9^\s]+)\) ([\S\s^:]+): ([\S\s]+)"
CRITERIA_PATTERN = r"## Acceptance Criteria\n(- [\S\s^\n]+[\n])+"
NOTES_PATTERN = r"## Notes\n(- [\w\s^\n]+[\n]*)+"

CARD_REGEX = re.compile(CARD_PATTERN)
CRITERIA_REGEX = re.compile(CRITERIA_PATTERN)
NOTES_REGEX = re.compile(NOTES_PATTERN)


@dataclass
class UserStory:
    id_: str
    title: str
    body: str
    priority: str
    points: str
    criteria: str=""
    notes: str=""


def validate_card(card: dict) -> bool:
    """ Returns True if the given Trello card JSON object conforms to the required story format, otherwise returns False.  
    
    Arguments: 
        card {dict} -- Trello card JSON to be validated

    Returns:
        bool - True if given card is valid, otherwise False
    """
    return CARD_REGEX.match(card["name"]) is not None


def parse_card(card: dict, lists: dict) -> UserStory:
    """ Returns a UserStory object parsed from the given Trello card JSON object. 

    Arguments:
        card {dict} -- Trello card JSON object
        lsits {dict} -- Mapping of Trello list ids to list names
    
    Returns:
        UserStory - Parsed UserStory object
    """
    content = card["name"]
    desc = card["desc"]
    id_ = str(card["idShort"])
    priority = PRIORITIES[lists[card["idList"]]]

    match = CARD_REGEX.match(content)
    points, title, body = match.groups()

    return UserStory(id_, title, body, priority, points) 


def collect_lists(data: List[dict]) -> dict:
    """Returns a mapping of Trello list ids to list names. Facilitates list name lookup where only the list id is given.
    
    Arguments:
        data {List[dict]} -- Trello JSON data
    
    Returns:
        dict -- Mapping of Trello list ids to list names
    """
    return {x["id"]:x["name"] for x in data["lists"]}


def collect_stories(data: List[dict]) -> List[UserStory]:
    """Returns a list of UserStory objects extracted from the given Trello JSON data.
    
    Arguments:
        data {List[dict]} -- JSON data from which stories will be extracted
    
    Returns:
        List[UserStory] -- List of parsed UserStory objects
    """
    cards = data["cards"]
    lists = collect_lists(data)
    stories = []
    
    for card in cards:
        if lists[card["idList"]] not in PRIORITIES:
            continue
        if not validate_card(card):
            print(f"Card is not valid. Check that it has the correct format: \"{card['name']}\"")
            continue 
        stories.append(parse_card(card, lists))
    return stories


def main(filename: str):
    """Main process
    
    Arguments:
        filename {str} -- Name of JSON file to be converted
    """
    with open(filename, "r") as f:
        data = json.load(f)
    print("Collecting stories")
    stories = collect_stories(data)
    print(f"Collected {len(stories)} valid stories")
    print("Creating pptx file")
    slides.create_slides(stories, "stories.pptx")
    print("Done")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise ValueError("Usage: trello-convert <json-file>")
    main(sys.argv[1])
