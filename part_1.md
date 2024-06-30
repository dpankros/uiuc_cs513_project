# CS 513 Group Project
## Part 1
    Team ID: ______
    Team Name: ______
    David Pankros, Aaron Schlesinger {pankros2, __}@illinois.edu

> The title / header of your Phase-I report should list (i) the Team-ID of your group1 and (ii) for each group member the name and Illinois email address
> 
> In addition you can give yourself a (cute) team name for ease of identification
 
### Description of Dataset (25 points)

>a. Here you will provide an ER diagram, an ontology, or a detailed database schema (10 points), and
>b. a narrative description of the dataset covering structure and content (15 points)

Dish contains information about food dishes, the number of menus where they appeared, a high and low price, and a first and last appearance year.

`Menu` contains a collection of the following fields:

- sponsors,
- events,
- venue types,
- venue name and general location,
- a description of the physical menu,
- the occasion for the meal,
- notes about the physical menu,
- a "call number,"
- keywords and language (both blank),
- the date of the menu,
- a location type (unused),
- the currency on the menu (sparely used),
- a currency symbol (used when currency is designated),
- a status field (presumably for an internal workflow),
- a menu page count, and
- the number of dishes on the menu

Several data inconsistencies exist in this collection.  5 menu records indicate a different number of pages than are actually stored in the `MenuPage` table, and 217 Menus also differ in the number of Dishes stored versus the number of dishes referenced in the 'dish_count' column.  In each instance, only the first page number is stored.  Additionally, some "pages" seemingly contain hundreds of dishes, which calls into question whether the `page_number` column is actually used in a semantically consistent way.

The `physical_description` column is really a separate collection of "tags" that describe the menu, and these data would thus be better stored as a separate table. The `occasion` column is also potentially representative of some kind of tag, but the format varies.  Some are delimited by semi-colon, some are not delimited, and some are encapsulated in hard-brackets (and seemingly limited to 8 characters).

Most commonly, the occasion and physical description are blank or null.  Some menus are in fact aggregates of multiple menus, such as ids `31054` and `31230`, that include descriptions such as "62 menus bound into 1 volume".

`MenuPage` is a collection of information about individual physical pages for a menu.  It contains a reference to a `menu_id` and a page number. (1202 have no page number, however).  An `image_id` field presumably references an image in another table, but there is no provided table that it references.  (23 rows in `image_id` include non-numeric values).  There are also `full_height` and `full_width` fields that seem to indicate an image size in pixels, though some appear incorrect or are altogether missing (such as id 329).  There is a `uuid` field that stores many distinct values but lacks a consistent format (some are upper case, while most are lower) and there is no indication what it references.  Finally, 5789 MenuPage rows are missing their referenced Menus.

`MenuItem` is a collection of individual dishes that appear on a menu page, along with the following fields:

- Price of the dish (445,916 rows of which are blank),
- A `high_price` column (91,905 rows of which are populated), 
- A reference to the dish in the `Dish` table (241 rows of which are blank),
- When it was created and update (or more accurately, when the database entry was created and updated),
- `xpos` and `ypos` fields, in the domain `[0,1)` (using SQL query `select min(xpos), max(xpos), min(ypos), max(ypos) from MenuItem;`), which presumably represent the location relative to the overall width and height of the dish on the menu.

A few additional notes about thee fields:

- The `xpos` and `ypos` fields do not indicate the location of the origin (i.e. is `(0,0)` the top-left or bottom left of the page?), nor do they indicate whether the position is the center of the block or whether it is a corner of a block.
- Price does not indicate units. You could presumably join `MenuItem` to `MenuPage` and then to `Menu` to (sometimes) discern the price _and_ the currency of the price.  
- 35 `MenuItem`s are missing their referenced `MenuPage`
- 244 `MenuItem`s are missing their referenced `Dish`.


### Use Cases (30 points)

#### Use case U1

>a. Target (Main) use case U1: data cleaning is necessary and sufficient (20 points)

You'd likely be able to use standard data cleaning techniques to produce a dataset suitable for at least the following applications:

- Non-production-critical online applications like reference systems
- Data mining applications like analytics systems concerning the New York City restaurant industry
- Unsupervised machine learning applications, which would likely be most valuable for pattern recognition and possible generative AI use cases

>b. “Zero data cleaning” use case U0: data cleaning is not necessary (5 points)

Since these raw data contain at least several inconsistencies we consider to be severe, we believe that they are unsuitable for use in user-facing applications.  Further, we don't believe that data mining applications over the raw data would produce reliable results.  Thus, we believe that only unsupervised learning applications would be suitable for the raw data.  The accuracy of results generated from these applications should not be directly relied upon for critical applications.

>c. “Never enough” use case U2 : data cleaning is not sufficient (5 points)

We believe there are many applications for which even data cleaning would not be sufficient, including the following:

- Any application involving knowing true prices because the currency is very sparse. We can guess, but never know, that the prices are in comparable units.
- Any application for which data accuracy and consistency is critical. We anticipate these applications will primarily be user-facing
- Automated systems in which the results of the automation are used to ensure safety, drive revenue, or other critical purposes.

### Data Quality Problems (30 points)
> a. List obvious data quality problems with evidence (examples and/or screenshots) (20 points)

Generally speaking, the schema for these data is largely denormalized, which reduces or eliminates the opportunity to establish referential integrity in many cases. These reductions in turn can reduce the overall quality of the data. We believe it's important to note, however, that many front-end applications -- particularly their performance -- can benefit from this denormalized arrangement.

1. Dish
2. Menu
3. MenuItem
4. MenuPage

There is no indication of the use for the `uuid` column.  Some rows with identical `menu_id`s and different page numbers have transposed `full_height` and `full_width` values indicating that one page is, possibly, rotated.

The `image_id` column appears like a foreign key, but more than several errors occur when treating it as such.  This column also uses mixed numeric types.  Most of the fields appear to be representable as `double`s, but when attempting to convert the values in this column, the following conversion errors occur:

```text
13944:15: conversion failed: "ps_rbk_637" to double (image_id)
13945:15: conversion failed: "ps_rbk_657" to double (image_id)
13946:15: conversion failed: "ps_rbk_661" to double (image_id)
13947:15: conversion failed: "psnypl_rbk_951" to double (image_id)
13948:15: conversion failed: "psnypl_rbk_952" to double (image_id)
15101:15: conversion failed: "ps_rbk_686" to double (image_id)
15102:15: conversion failed: "ps_rbk_687" to double (image_id)
16876:15: conversion failed: "psnypl_rbk_925" to double (image_id)
16877:15: conversion failed: "psnypl_rbk_926" to double (image_id)
16878:15: conversion failed: "psnypl_rbk_927" to double (image_id)
16879:15: conversion failed: "psnypl_rbk_928" to double (image_id)
27286:15: conversion failed: "psnypl_rbk_988" to double (image_id)
28257:15: conversion failed: "psnypl_rbk_1068" to double (image_id)
34955:14: conversion failed: "psnypl_rbk_935" to double (image_id)
35153:15: conversion failed: "psnypl_rbk_936" to double (image_id)
35908:15: conversion failed: "psnypl_rbk_1077" to double (image_id)
35909:15: conversion failed: "psnypl_rbk_1078" to double (image_id)
35910:15: conversion failed: "psnypl_rbk_1079" to double (image_id)
35911:16: conversion failed: "psnypl_rbk_1080" to double (image_id)
55577:15: conversion failed: "ps_rbk_657" to double (image_id)
57108:15: conversion failed: "ps_rbk_637" to double (image_id)
60216:15: conversion failed: "ps_rbk_643" to double (image_id)
60217:15: conversion failed: "ps_rbk_644" to double (image_id)
```

>b. Explain why / how data cleaning is necessary to support the main use case U1 (10 points)

We assume the "main use case" from U1 is non-production-critical online systems (rather than data mining/analytics or unsupervised learning applications), such as reference systems.

If we were to build a reference system over the raw data, the many inconsistencies and other issues with the data would produce results upon which we could not rely for any reasonable application, even if a single result in question were accurate.  We must clean the data to reduce the number and severity of these inconsistencies enough to be able to rely upon at least the majority of the results fetched from the reference system.

### Initial Plan for Phase-II (15 points)

>Below is a possible plan, listing typical data cleaning workflow steps.  In your Plan for Phase-II, fill in additional details for the project steps as needed.  In particular, include who of your team members will be responsible for which steps, and list the timeline that you are setting yourselves!

> S1: Review (and update if necessary) your use case description and dataset description

We will do this iteratively, but this will initially be led by Aaron.

> S2: Profile D to identify DQ problems: How do you plan to do it? What tools are you going to use?

We have identified several large DQ problems. We plan to use a combination of SQL (primarily with SQLite), Pandas and OpenRefine to identify further DQ problems in more detail. We believe we currently know enough about the DQ problems in this dataset to proceed with DC, but we will iteratively refer back to our DQ research process as we proceed.

> S3: Perform DC “proper”: How are you going to do it? What tools do you plan to use? Who does what?

We expect to primarily use OpenRefine to do DC.

> S4: Data quality checking: is `D’` really “cleaner” than D? Develop test examples / demos

We actually want to determine two things about a new dataset `D'`:

1. Is it a dataset that still represents `D` accurately?
2. Is it really cleaner than `D`?

While we plan to use OpenRefine to clean the data, we plan to use the features of a SQL database (primairly SQLite) to test for these two features.

To determine (1), we plan to attempt to normalize the data and enforce a SQL schema. If we can do so with minimal or no errors in the import process, we expect features of the database like referential integrity and strict data typing will ensure the dataset still represents `D` accurately.

We expect these features to also contribute to ensuring (2), but we also aim to develop a suite of database queries -- primarily those that join across more than 2 tables -- and acceptance criteria for the various results of each query.

> S5: Document and quantify change (e.g. columns and cells changed, IC violations detected: before vs after, etc.)

OpenRefine will give detailed provenance for all the cleaning operations we perform, and both the SQL import process and our acceptance-test suite of queries will give us a detailed, standard outline of IC violations etc...
