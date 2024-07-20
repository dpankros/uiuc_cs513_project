# CS 513 Group Project, Part 2

**Team ID**: 37

__Team Name__: PADS

Aaron Schlesinger and David Pankros 

{aschle2, pankros2}@illinois.edu

## 1. Description of Data Cleaning Performed

### Identify and describe all (high-level) data cleaning steps you have performed.

We've used OpenRefine and a SQL database together to achieve data cleaning outcomes that are more complex than OpenRefine would easily allow us to do on its own. We've also managed to build a Python client for OpenRefine's API. Instead of using the OpenRefine dashboard to perform data cleaning steps visually with the point-and-click user interface, we're able to integrate all our data cleaning steps, listed below, into a single Python program that can be run from the command line.

- Raw CSV manipulation
- Loading CSV data into OpenRefine
- Manipulating data in OpenRefine
- Loading partially-cleaned data into the SQL database
- Constructing specific views of data in SQL
- Manipulating data in SQL
- Exporting cleaned data from SQL to final, cleaned data in CSV format

The result of the single, unified Python program is that we have the ability to run our entire workflow, including all outer and inner workflow steps, with a single command. This ability to run the entire workflow with a single command is a significant advantage over running the workflow manually, step-by-step, in OpenRefine and SQL and gives us the ability to easily reproduce our results.

### For each high-level data cleaning step you have performed, explain its rationale. Was the step really required to support use case U1? Explain. If not, explain why those steps were still useful.

For context, use case `U1` is summarized as using standard data cleaning techniques to produce data to be used for non-production-critical applications, data mining, unsupervised learning, or possibly further analysis and manipulation to use cleaner subsets of the entire dataset for additional purposes.

We have listed the high-level data cleaning steps in the introduction to this section. We will re-list them below and explain the rationale for each step.

#### Raw CSV manipulation
This step is primarily loading CSV data into memory, for the purpose of subsequently loading it into OpenRefine. We do no data cleaning in this step, but it is necessary to support all the subsequent steps.

#### Loading CSV data into OpenRefine

Similarly to the previous step, we do not perform any data cleaning in this step. Loading data into OpenRefine is necessary to support all OpenRefine-based and subsequent cleaning steps.

#### Manipulating data in OpenRefine

#### Loading partially-cleaned data into the SQL database

#### Constructing specific views of data in SQL

#### Manipulating data in SQL

#### Exporting cleaned data from SQL to final, cleaned data in CSV format


## 2. Document data quality changes

### Quantify the results of your efforts, e.g., by providing a summary table of changes: Which columns changed? How many cells (per column) have changed, etc.?

### Demonstrate that data quality has been improved, e.g., by devising IC-violation reports (answers to denial constraints) and showing the difference between number of IC violations reported before and after cleaning.

## 3. Create a workflow model

### A visual representation of your overall (or “outer”) workflow W1, e.g., using a tool such as YesWorkflow. At a minimum, you should identify key inputs, outputs, and steps of the workflow, along with dependencies between these. Key phases and steps of your data cleaning project may include, e.g., data profiling, data loading, data cleaning, IC violation checks, etc. Explain the design of W1 and why you’ve chosen the tools that you have in your overall workflow.

### A detailed (possibly visual) representation of your “inner” data cleaning workflow W2 (e.g., if you’ve used OpenRefine, you can use the OR2YW tool).

## 4. Conclusions & Summary

### Please provide a concise summary and conclusions of your project, including lessons learned.

### Reflect on how work was completed. You should summarize the contributions of each team member here (for teams with >= 2 members).

## 5. Submission of supplementary materials in a single ZIP file

- Workflow model
- Operation history
  - OpenRefine recipe
  - Other scripts, provenance files
- Queries
- Original ("dirty") and cleaned datasets
  - Please provide an **accessible** Box folder link in a plain text file: `DataLinks.txt`
