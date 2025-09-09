
# Reviewer

## Requirements

- Python 3.11
- SQLite3 (included in Python)

## Features

- Create vocabulary sets and add terms interactively
- Review sets and track your score
- Leaderboard for top scores per set
- Missed terms review mode
- All data stored in a local SQLite database

## Usage

1. **Run the program**:

    ```bash
    python reviewer.py
    ```

1. **Menu options**:
    - `1. Create New/Add to Set`: Create a new set or add terms to an existing set.
    - `2. Open Set`: Review a set, answer questions, and see your score.
    - `3. Exit`: Quit the program.

1. **Creating a set**:
    - Enter a name and subpath for the set.
    - Add terms and answers (comma-separated for multiple answers).

1. **Reviewing a set**:
    - Select a set from the menu.
    - Answer questions; missed terms can be reviewed again.
    - Optionally log your score and view the leaderboard.

## Troubleshooting

- Make sure you have write permissions in the folder for the database file.
- If you encounter errors, check that your table names use only letters, numbers, and underscores.
- The database file is located at `vocaber.db` in the reviewer folder.

## Example

```terminal
Menu
1. Create New/Add to Set
2. Open Set
3. Exit
Choice: 1
What would you like to name this set? SpanishVocab
What is the sub path for this set? Languages/Spanish
Would you like to add terms to this set? yes
What's the term? hola
What's the answer? hello
...etc...
```

## Sub Path

Basically this is path that you add just like a regular path, it navigatable and etc. The correct way is `Languages/Spanish/Quiz 1` or `Science/Vocab 1`

## Notes

A database comes with this program with a few language sets in it. There is a couple of general languages sets and some Latin sets.

## Updates

### In the future

- A additional tool that comes with this program for configuring the database and editing the program
- **GUI**

### Past

#### v3.0

- Table for each set
- Table for the scores
- Table storing all tables
- Leaderboard implemented
- Navigation system added
- README.md added
- Cleaned all code up
- Converted all files over to SQL format

#### v2.1

- Basic functionality for choosing stuff and new format

#### v2.0

- Instead of using text files for storing vocab sets, changed this to SQL database, reprogrammed the whole thing

#### v1.2

- Reorganized code

#### v1.0

- Sets are randomized
- All basic functionality
- Leaderboard implemented

#### v0.5

- Basic program, you add sets and run through them

#### v0.1

- Basic functionality of going through Vocab, you have to manually add it
