# CS 513 Group Project, Data importer and checker

This is a data importer and quality checker. It's meant to be used in the context of the CS 513 Group Project, Part 2. It's a set of Python programs that read in a CSV file to a sqlite database and check for data quality issues. They are meant to compose a suite used for data quality cleaning, checking and validation.

## Usage

I've chosen [rye](https://rye.astral.sh/) to build and run this project, primarily because it's the tool closest to an "all-in-one" experience I'm used to from other languages like Go (the `go` CLI), Rust (the `cargo` tool), Node.JS (the `npm` or `yarn` tools), etc...

To build and run this project, first [install `rye`](https://rye.astral.sh/guide/installation/)

>The easiest way, which requires you to trust the authors, is to run `curl -sSf https://rye.astral.sh/get | bash` on Mac or Linux. If you're on Windows, see that install link for links to installers.

Immediately after installation, run this command (only necessary once):

```shell
rye sync
```

Finally, whenever you want to run your code, run:

```shell
# to import from CSV to sqlite, and do some basic cleaning along the way
#
# NOTE: this takes multiple minutes to run to completion, thanks to Python's
# single-threaded nature.
$ rye run importer 
# to validate the data in the sqlite database
$ rye run checker
```
