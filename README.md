# trello-convert

## Usage

Requires Python 3.7 or higher. Download the JSON data for your Trello board by accessing `Show Menu/More/Settings/Print
and Export/Export as JSON`. 

```bash
> git clone https://github.com/LiamGraham/trello-convert
> cd trello-convert
> pip install -r requirements.txt
> python convert.py path/to/trello-json
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
- <criterion-1> 
- <criterion-2>
- <criterion-3>

# Notes
- <note-1> 
- <note-2>
- <note-3>
```

e.g.

```
# Acceptance Criteria
- User input field for energy usage in kWh, including options for usage distribution 
(i.e. predominant usage is night time or day time)
- Alternative input method for typical usage based on family size & number of appliances

# Notes
- The electricity usage is used to calculate the amount of energy usage which will ultimately 
be replaced by the solar system. This is required for financial calculations.
```

Story cards should be placed in lists corresponding to their priority ("Must Have", "Should
Have", "Could Have", and "Won't Have"). "Must Have" stories will be place in the list
named "Must Have", and so on.

The story ID is based on the position of the story card on the board. Cards are numbered
from top to bottom and left to right - i.e. The first card in the "Must Have" list is
#1, the second card is #2, and the bottom card in the "Won't Have" list is #n for n
story cards. 

Refer to the [example Trello board](https://trello.com/b/VhYYh3YQ/csse3002-example-trello-board) to see what a correctly formatted and organised board
looks like.
