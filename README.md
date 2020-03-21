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

Refer to the [example Trello board](https://trello.com/b/VhYYh3YQ/csse3002-example-trello-board) to see what a correctly formatted and organised board
looks like.
