# CS 513 Group Project

## Part 1

    Team ID: 37
    Team Name: ______
    Aaron Schlesinger and David Pankros 
    {aschle2, pankros2}@illinois.edu

> The title / header of your Phase-I report should list (i) the Team-ID of your group1 and (ii) for each group member
> the name and Illinois email address
>
> In addition you can give yourself a (cute) team name for ease of identification

### Description of Dataset (25 points)

> a. Here you will provide an ER diagram, an ontology, or a detailed database schema (10 points), and
> b. a narrative description of the dataset covering structure and content (15 points)

Dish contains information about food dishes, the number of menus where they appeared, a high and low price, and a first
and last appearance year.

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

The `physical_description` column is really a separate collection of "tags" that describe the menu, and these data would
thus be better stored as a separate table. The `occasion` column is also potentially representative of some kind of tag,
but the format varies. Some are delimited by semi-colon, some are not delimited, and some are encapsulated in
hard-brackets (and seemingly limited to 8 characters).

`MenuPage` is a collection of information about individual physical pages for a menu. It contains a reference to
a `menu_id` and a page number. (1202 have no page number, however). An `image_id` field presumably references an image
in another table, but there is no provided table that it references.  (23 rows in `image_id` include non-numeric
values). There are also `full_height` and `full_width` fields that seem to indicate an image size in pixels, though some
appear incorrect or are altogether missing (such as id 329). There is a `uuid` field that stores many distinct values
but lacks a consistent format (some are upper case, while most are lower) and there is no indication what it references.
Finally, 5789 MenuPage rows are missing their referenced Menus.

`MenuItem` is a collection of individual dishes that appear on a menu page, along with the following fields:

- Price of the dish (445,916 rows of which are blank),
- A `high_price` column (91,905 rows of which are populated),
- A reference to the dish in the `Dish` table (241 rows of which are blank),
- When it was created and update (or more accurately, when the database entry was created and updated),
- `xpos` and `ypos` fields, in the domain `[0,1)` (using SQL
  query `select min(xpos), max(xpos), min(ypos), max(ypos) from MenuItem;`), which presumably represent the location
  relative to the overall width and height of the dish on the menu.

A few additional notes about thee fields:

- The `xpos` and `ypos` fields do not indicate the location of the origin (i.e. is `(0,0)` the top-left or bottom left
  of the page?), nor do they indicate whether the position is the center of the block or whether it is a corner of a
  block.
- Price does not indicate units. You could presumably join `MenuItem` to `MenuPage` and then to `Menu` to (sometimes)
  discern the price _and_ the currency of the price.
- 35 `MenuItem`s are missing their referenced `MenuPage`
- 244 `MenuItem`s are missing their referenced `Dish`.

### Use Cases (30 points)

#### Use case U1

> a. Target (Main) use case U1: data cleaning is necessary and sufficient (20 points)

You'd likely be able to use standard data cleaning techniques to produce a dataset suitable for at least the following
applications:

- Non-production-critical online applications like reference systems
- Data mining applications like analytics systems concerning the New York City restaurant industry
- Unsupervised machine learning applications, which would likely be most valuable for pattern recognition and possible
  generative AI use cases

> b. “Zero data cleaning” use case U0: data cleaning is not necessary (5 points)

Since these raw data contain at least several inconsistencies we consider to be severe, we believe that they are
unsuitable for use in user-facing applications. Further, we don't believe that data mining applications over the raw
data would produce reliable results. Thus, we believe that only unsupervised learning applications would be suitable for
the raw data. The accuracy of results generated from these applications should not be directly relied upon for critical
applications.

> c. “Never enough” use case U2 : data cleaning is not sufficient (5 points)

We believe there are many applications for which even data cleaning would not be sufficient, including the following:

- Any application involving knowing true prices because the currency is very sparse. We can guess, but never know, that
  the prices are in comparable units.
- Any application for which data accuracy and consistency is critical. We anticipate these applications will primarily
  be user-facing
- Automated systems in which the results of the automation are used to ensure safety, drive revenue, or other critical
  purposes.

### Data Quality Problems (30 points)

> a. List obvious data quality problems with evidence (examples and/or screenshots) (20 points)

Generally speaking, the schema for these data is largely denormalized, which reduces or eliminates the opportunity to
establish referential integrity in many cases. These reductions in turn can reduce the overall quality of the data. We
believe it's important to note, however, that many front-end applications -- particularly their performance -- can
benefit from this denormalized arrangement.

1. Dish
2. Menu
3. MenuItem
4. MenuPage

Several data inconsistencies exist in this collection. 5 menu records indicate a different number of pages than are
actually stored in the `MenuPage` table, and 217 Menus also differ in the number of Dishes stored versus the number of
dishes referenced in the 'dish_count' column. In each instance, only the first page number is stored. Additionally,
some "pages" seemingly contain hundreds of dishes, which calls into question whether the `page_number` column is
actually used in a semantically consistent way.

#### Dish

| Table    | Column               | Type     | Null Count | Domain                |
|----------|----------------------|----------|------------|-----------------------|
| Dish     | id                   | int      | 0          |                       |
| Dish     | name                 | text     | 0          |                       |
| Dish     | description          | text     | 423397     |                       |
| Dish     | menus_appeared       | int      | 0          | [0,7800]              |
| Dish     | times_appeared       | int      | 0          | [-100,8500]           |
| Dish     | first_appeared       | int      | 0          | [0,3000]              |
| Dish     | last_appeared        | int      | 0          | [0,3000]              |
| Dish     | lowest_price         | float    | 29100      | [0,1100]              |
| Dish     | highest_price        | float    | 29100      | [0,3100]              |
| Menu     | id                   | int      | 0          |                       |

Problems:
`description` is wholly unused.
`menus_appeared` contains values from 0 to 7800.  That rows in this collection indicate there are dishes that don't 
appear in any menu strongly suggests that those rows are incorrect.  This calls into question the accuracy of all the 
data stored in `menus_appeared`.
`times_appeared` similarly contains errors that call into question the accuracy of the data stored therein.  Obviously, 
negative numbers have no value and are erroneous.  
`first_appeared` and `last_appeared` contain years and unless the dataset is documenting menus from the time Christ's 
birth, not to mention almost one-thousand years into the future, there are obvious quality problems present.
`lowest_price` and `highest_price` presumably contain currency values, but no units are referenced by the table, 
calling into question the usability of the column and whether it is consistent with the currency in Menu and how this 
column would resolve values expressed in different currencies.


#### Menu

| Table    | Column               | Type     | Null Count | Domain                |
|----------|----------------------|----------|------------|-----------------------|
| Menu     | id                   | int      | 0          |                       |
| Menu     | name                 | text     | 14348      |                       |
| Menu     | sponsor              | text     | 1561       |                       |
| Menu     | event                | text     | 9391       |                       |
| Menu     | venue                | text     | 9414       |                       |
| Menu     | place                | text     | 9422       |                       |
| Menu     | physical_description | text     | 2777       |                       |
| Menu     | occasion             | text     | 13742      |                       |
| Menu     | notes                | text     | 6932       |                       |
| Menu     | call_number          | text     | 1562       |                       |
| Menu     | keywords             | text     | 17545      |                       |
| Menu     | language             | text     | 17545      |                       |
| Menu     | date                 | date     | 586        |                       |
| Menu     | location             | text     | 0          |                       |
| Menu     | location_type        | text     | 17545      |                       |
| Menu     | currency             | text     | 11089      |                       |
| Menu     | currency_symbol      | text     | 11089      |                       |
| Menu     | status               | text     | 0          | complete,under review |
| Menu     | page_count           | int      | 0          | [1,75]                |
| Menu     | dish_count           | int      | 0          | [0,4100]              |

In the Menu collection the `name`, `occasion` and `location_type` columns are frequently blank or null. Some menus are in fact
aggregates of multiple menus, such as ids `31054` and `31230`, that include descriptions such as "62 menus bound into 1
volume". Such semantic inconsistencies will be difficult to remove from the data by automated methods.

As mentioned previously, The `physical_description` and `occasion` columns are really separate collections of "tags"
that describe the menu. Formats of these columns vary: some are not delimited, some are delimited, and some are
encapsulated in hard-brackets (and seemingly limited to 8 characters).

#### MenuPage

| Table    | Column               | Type     | Null Count | Domain                |
|----------|----------------------|----------|------------|-----------------------|
| MenuPage | id                   | int      | 0          |                       |
| MenuPage | menu_id              | int      | 0          |                       |
| MenuPage | page_number          | int      | 1202       | [1,75]                |
| MenuPage | image_id             | int      | 0          |                       |
| MenuPage | full_height          | int      | 329        | [0,13000]             |
| MenuPage | full_width           | int      | 329        | [500,9200]            |
| MenuPage | uuid                 | text     | 0          |                       |

`page_number` contains blank values.  It is unknown if a blank should be considered the first page, such as in a one-page 
menu or if it is simply erroneous.

The `image_id` column appears to be a foreign key to an unprovided collection of images, but many errors occur when 
treating it as such because while predominantly integers are present, values such as 'psnypl_rbk_936' are also contained 
in that column. 
`full_height` and `full_width` likely are the width in pixels of the referenced image.  One would expect the pages of a 
menu to have the same proportions, but Some rows with identical `menu_id`s and different page numbers have transposed 
full_height` and `full_width` values indicating that one (or more) page(s) is/are, possibly, rotated.

Finally, there is no indication of the use for the `uuid` column and the column name provides no clues.  They appear to 
be valid UUIDS, though admittedly we didn't try to parse them properly, but the format looks generally correct. 

#### MenuItem
| Table    | Column               | Type     | Null Count | Domain                |
|----------|----------------------|----------|------------|-----------------------|
| MenuItem | id                   | int      |            |                       |
| MenuItem | menu_page_id         | int      | 0          |                       |
| MenuItem | price                | float    | 445916     | [0,190000]            |
| MenuItem | high_price           | float    | 1240821    | [0,7900]              |
| MenuItem | dish_id              | int      | 241        |                       |
| MenuItem | created_at           | datetime | 0          |                       |
| MenuItem | updated_at           | datetime | 0          |                       |
| MenuItem | xpos                 | float    |            | [0,1)                 |
| MenuItem | ypos                 | float    |            | [0,1]                 |

`price` similar to other collections, price does not indicate a currency and it's values vary wildly from 0 to 190,000.

`high_price`  WHY??  Is it used multiple times in a menu?  At different prices?

`dish_id` contains 241 nulls or blank values.  What is their significance?

`created_at` and `updated_at` seem like fairly-standard database creation/update timestamps and have no observable issues. 

`xpos` and `ypos` have semantic issues in that it is impossible to understand their use without more information, 
particularly the location indicated by xpos and xpos.  Is it a center point, a corner?  Why is there no width and height
to define a bounding box? etc.

> b. Explain why / how data cleaning is necessary to support the main use case U1 (10 points)

We assume the "main use case" from U1 is non-production-critical online systems (rather than data mining/analytics or
unsupervised learning applications), such as reference systems.

If we were to build a reference system over the raw data, the many inconsistencies and other issues with the data would
produce results upon which we could not rely for any reasonable application, even if a single result in question were
accurate. This is particularly true for semantic issues where no straight-forward data manipulation will provide
reliable data, other than manual human review.  We must clean the data to reduce the number and severity of these 
inconsistencies enough to be able to rely upon at least the majority of the results fetched from the reference system.

### Initial Plan for Phase-II (15 points)

> Below is a possible plan, listing typical data cleaning workflow steps. In your Plan for Phase-II, fill in additional
> details for the project steps as needed. In particular, include who of your team members will be responsible for which
> steps, and list the timeline that you are setting yourselves!

As we document our steps for Phase II, we will include responsibilities for each part, but please understand that this
is not the first project that the team members have completed.  They have a history of dividing up tasks in a fair and 
amicable fashion, without an extensive project plan.  Both team members are comfortable and adept at working with 
agile methodologies and these have worked well in the past for us.  All task assignments will be subject to change 
based on our own personal and professional workloads.

> S1: Review (and update if necessary) your use case description and dataset description

We expect to discover more features of (and issues with) this dataset, and thus additional use cases, as we proceed with
data cleaning (DC). Thus, we'll review and update our use cases and dataset descriptions iteratively and as necessary.
This work will initially be done by Aaron.

> S2: Profile D to identify DQ problems: How do you plan to do it? What tools are you going to use?

We have already identified several large DQ problems. We plan to use a combination of SQL (primarily with SQLite), Pandas and
OpenRefine to identify further DQ problems in more detail and, likely, to provide more nuance to the known problems. We 
believe we currently know enough about the DQ problems in this dataset to proceed with DC, but we will iteratively refer 
back to our DQ research process as we proceed.  This will likely be a combined effort between Aaron and Dave.

One internal suggestion was to script all the data cleaning using python and refine-client.  This idea was discounted
when it was observed that the last update to that library was over 10 years ago, and it barely supports python 3. In 
fact, trying to run it using python 3 results in syntax errors from the library.  Thus, any further attempts to script
data cleaning with python have been abandoned.

> S3: Perform DC “proper”: How are you going to do it? What tools do you plan to use? Who does what?

We expect to primarily use OpenRefine to do DC.

> S4: Data quality checking: is `D’` really “cleaner” than D? Develop test examples / demos

We actually want to determine two things about a new dataset `D'`:

1. Is it a dataset that still represents `D` accurately?
2. Is it really cleaner than `D`?

While we plan to use OpenRefine to clean the data, we plan to use the features of a SQL database (primarily SQLite) to
test for these two features.

To determine (1), we plan to attempt to normalize the data and enforce a SQL schema.  We can use views to represent a 
version of the data matching the original dataset. If we can do so with minimal or no errors in the import process, we 
expect features of the database like referential integrity and strict data typing will ensure the dataset still 
represents `D` accurately.

We expect these features to also contribute to ensuring (2), but we also aim to develop a suite of database queries --
primarily those that join across more than 2 tables -- and acceptance criteria for the various results of each query.

Example test cases:

- For tables from the original dataset that purport to include the number of pages, dishes, etc (the "Original Number"),
  is the Original Number accurate?  If so, can a query be constructed for the cleaned dataset that returns the same value as the Original Number.
- Are all foreign key violations resolved? (i.e. For all cases, are there primary keys in the foreign table
  corresponding to the foreign key?)
- 

> S5: Document and quantify change (e.g. columns and cells changed, IC violations detected: before vs after, etc.)

OpenRefine will give detailed provenance for all the cleaning operations we perform, and both the SQL import process and
our acceptance-test suite of queries will give us a detailed, standard outline of IC violations etc...
