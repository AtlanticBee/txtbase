# Txtbase

## Overview

This repository represents a database engine using only plaintext files (one per table column) and associated supporting programs.

The project aims to bring together a few solutions and avoid some frustrations:
- The use of text files makes it easy to modify without cumbersome SQL, and copy-paste techniques from existing spreadsheets and CSVs are easy
- The use of text files makes git tracking of the database's history easy
- Without many external dependencies, the databse system works just as well for low-tech setups on a local machine as they do in the cloud
- The columnar storage format is a natural way to look at data and easier to manually modify

There are some trade-offs of course (e.g. speed vs a binary file DB) and I won't be going to great lengths making this fast - the success of this database will be primarily measured in:
- Quality of code
- Ease of installation and  use
- Documentation

## Design (v3)

OK, my first instinct was to maintain a nested object for the DB (DB -> Table -> Column (Data)).
However, I think this emulates the "real world" filesystem / human concept of a database or spreadsheet, rather than making it easiest for the computer to handle.

Instead, I think we should have:
- A database (perhaps an object with a few names and statistics methods), but otherwise not much, maybe nothing!
- A dict of tables (name is key) or set?
- A dict of columns (name is key, )
- Lists of their relationships and rules

Let's work it out a bit more thoroughly...
A column of data is a name and a list of one of our four data types (number, boolean, string, ISO datetime)
- For our first version, do we even want types, or shall we just check types at runtime if an operation is run (i.e. everything sits as text in memory, but then if someone does a SUM and we encountered a non-summable row we'd throw an error?)
- We could also, following on from this idea, throw useful user error messages like where the incorrect data was encoutered or sanitisation methods to check the existing data meets a specific data type
- This would make it easier an we wouldn't have to store any dedicated tracker of what column is which type which either adds user overhead (a JSON schema, specific .col.string nomenclature, or special rows that denote type) or complexity to a system that may not need to worry about it anyway AND... it's stored in textfiles anyway so why not! It's the simplest approach
We do still need to codify any relationships between a column and a foreign key, and if it's used as a foreign key then duplicates cannot be allowed. That would be easier to implement in our new global system since we'd just keep a list (or more likely set) of column names that are being used as a foreign key, or a dictionary with a list of what columns use it for better errors for the user.

There is one issue. I'd like the fast lookups of the columns in dictionaries/sets just like the tables, but we should really allow duplicate column names (e.g. you could have a table of horses and a column called "name", and a separate column of names for sheep). Either we simply use a data structure that allows column name duplicates, or perhaps a combined string that is the table name + column name? The issue there is we start doing string parsing, whereas previously our solution was to nest a data object inside the other. Alternatively we give it a unique ID on load (an integer would suffice) and if a column with the same table and same column name appears, it would be easy to rectify... no. Let's consider the other options:
- tables come with x.col, x.ref where x.col is the column data and x.ref is the reference to a foreign key containing a string like "mytable/mycolumn" which is intelligible in the UNIX community as a path to another file, but not requiring the user to know symbols like ".." or file extensions
- A dedicated (or top-level DB) folder location for reference value .col files where duplicates aren't allowed. This would be neat, but would require people to enforce this themselves. It also means when looking inside a folder the .ref wouldn't need to contain anything except the .col file name (since we know which table to look in).
- a ref filename which is something like x.table.column.ref with nothing inside required. This could cause problems parsing the filenames however and requires the user to type it exactly as stated in a kind of custom filenaming language which is probably overly complex

I'm not happy with any of these completely (although the first option seems to win out in my mind). I could also create a symbolic link to the file using existing UNIX tools. However having looked into this (despite being a feature visible in all three major operating systems), symlinks are treated as physically separate from the "inodes" that govern file system permissions and links, so editing them easily with a text editor would be impossible and this avenue will not work.




One nice thing about this is that as long as (say) our set of tables exists, if we then wanted to add metadata (e.g. table creator, name history...) it's just another list of data, rather than a modification of our entire encapsulated object-world model.

