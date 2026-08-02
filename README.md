# README for txtbase

## Background and principles

The idea of txtbase stemmed from some frustrations I encoutered on SQLite with SQL, but which apply more generally to any digital database:
- It takes AGES to do things manually
- Without custom UIs that can interact with the DB, simple Unix processes like copying and pasting or searching require substantial knowledge and effort. and are not directly compatible
- Moving data to/from other file types (e.g. importing data from text files, spreadsheets, notes...) all require extra steps or user interfaces to bridge the gap
- Changes cannot be tracked and data cannot be directly visualised with Git/Github or another version control program (data being stored in high performance binaries)
- Things I don't understand from start to finish annoy me, and databases are one of the many things I don't understand fully

The philosphy of txtbase is therefore as follows:
- Data is stored in columns - one ".col" text file per column
- Columns are saved within directories (folders) that represent the names of tables
- Column files are NOT allowed to be "denormalised" i.e. no CSVs with annoying delimeters. This makes the format as basic and easy to read and edit as possible
- The index of a column is implicit as the line number
- Columns within a table MUST share the same number of lines to maintain integrity. If a mistake is made (e.g. you added a blank row to one column), the fix 
- A database is simply a collection of these table folders along with a few optional settings
- Optional settings are to mark schemas via a JSON that relates a column file to:
    - Its data type (int, float, bool, str) - note if not set, type will be inferred but not guaranteed to be correct
    - If the column uses values from another column (i.e. are foreign keys)
    - I haven't thought this through fully, but I'm considering nullability of a value (and what it means for each data type) - this might affect the idea of hard vs soft deletions
        - A hard deletion would shift everything in a col file up
        - A soft deletion would simply mark the value as no longer valid or null. Again, this will be updated when I've thought about it some more!

Some additional rules to be aware of for ease of use and simplicity:
- Files and folders must only have the following characters: ^[A-Za-z0-9-]+ (i.e. alphanumerical ASCII, and dashes). This is also known as kebab case.
    - This differs from the python scripts that typically use snake case - an accidental but in my opinion useful separation
- Dates are stored as ISO 9601 strings which permit automatic sorting but are more readable than Unix timestamps (which is part of the design philosophy)
- Column files only know if they depend on a foreign key, but they do not know if they themselves are used as a foreign key - this avoids a synchronisation requirement
    - Due to this, there will be an overhead in going from child to parent
- The newline is the only delimeter allowed for data
- Only files with the extension .col are treated as data files
- All folders within the database are considered tables (so if they're empty, they're just empty tables)
- In theory, one-to-many, many-to-one and many-to-many relationships are always just combinations of one-to-many relationships. So that's the only one we will account for here! (With JOIN tables)
- Foreign key tables must be unique

The database engine checks all rules and schemas on startup, during request processing, and during shutdown.
Failed rules will result in an error log and the program will refuse to start.
However, it will not enforce anything when powered off (of course... it can't!). The rest of the time, your database is just files! Do what you want :D

## Basic Architecture

The core logic is in Python.
The database folder is opened and read into memory - which is where all data lives until shutdown.
The python script starts an HTTP server locally (port set in settings.json - where all global program settings live).
Requests to query or update the database are made via the HTTP server.

### Architectural philosophies

- Keep things simple and iterate over multiple versions
- Use data as the primary source of logic wherever possible
- Use rules engines wherever possible
- Forbid messy features like multi-value cells in a row (e.g. none of that JSON rubbish inside columns)

### Features I'd like to implement in this project:

- Simple browser feature for columns and tables that also relies on the HTTP server
- Maybe add summary statistics to the server's capabilities
- Views - custom GET requests (perhaps using joins and conditions) that can be saved and exported
- Exports - to simple formats like CSV, maybe even one of the binary database formats?
- Github Action that checks the integrity of a database after a change or before merging into the main branch for CI/CD compatibility on Github
- Versions produce summary stats on Github too
- A write-ahead log
- Some kind of crash memory safety (maybe frequently saving changes, or dumping files to an on-file buffer that can be recovered on startup)
- Some level of encryption/encoding for sensitive data
- Hashes of files for integrity checks
- Tombstone files and/or soft deletions (should there be a NULL format? What does an empty line represent?)


### Startup
Global settings for the program are saved in settings.json
The program runs in Python using the command "txtbase" with an optional path argument to your database folder.
The entry point is main.py (top level in this repository), but the core of the application runs through core.py.
If the folder is not given, a default folder is used (defined in settings.json) relative to the current working directory.



## Python Setup

The main.py script is the starting point.
The TOML file pyproject.toml allows you to run the program using the alias "txtbase" with this command for adn editable working experience:
```pip install -e .```
Run this from the root directory.

Later, I will try out installing it as an end user direct from Github using:
```pip install git+https://github.com/AtlanticBee/txtbase.git```