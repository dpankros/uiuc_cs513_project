# quality-checker

This is a data quality checker. It's meant to be used in the context of the CS 513 Group Project, Part 2. It's a simple Python script that reads in a CSV file and checks for data quality issues. It's meant to be used as a starting point for data quality checking, and can be extended to include more checks as needed.

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
rye run quality-checker
```
