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

## Design

