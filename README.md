# trello-convert

## Usage

Download the JSON data for your Trello board by accessing `Show Menu/More/Settings/Print
and Export/Export as JSON`. 

```bash
>>> git clone https://github.com/LiamGraham/trello-convert
>>> cd trello-convert
>>> pip install -r requirements.txt
>>> ./convert.py path/to/trello-json
```

## Trello Board Structure

All story cards in the Trello board should have the following format:

```
(<story-points>) <story-title>: <story-body>
```

e.g. 
```
(1) Energy Usage Input: As a potential customer, I want the system to...
```

The acceptance criteria and notes for the story should be placed in the card description
as follows:

```
# Acceptance Criteria
- 
- 
- 

# Notes
- 
- 
-
```

Story cards should be place in lists corresponding to their priority ("Must Have", "Should
Have", "Could Have", and "Won't Have"). "Must Have" stories will be place in the list
named "Must Have", and so on.

The story ID is based on the position of the story card on the board. Cards are numbered
from top to bottom and left to right - i.e. The first card in the "Must Have" list is
#1, the second card is #2, and the bottom card in the "Won't Have" list is #n for n
story cards. 

Refer to the [example Trello board](https://trello.com/b/VhYYh3YQ/csse3002-example-trello-board) to see what a correctly formatted and organised board
looks like.
