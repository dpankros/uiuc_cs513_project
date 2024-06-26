# CS 513 Group Project
## Part 1
    Team ID: ______
    Team Name: ______
    David Pankros, Aaron Schlesinger {pankros2, __}@illinois.edu

> The title / header of your Phase-I report should list (i) the Team-ID of your group1 and (ii) for each group member the name and Illinois email address
> 
> In addition you can give yourself a (cute) team name for ease of identification
 
### Description of Dataset (25 points)
Dish contains information about food dishes, the number of menus where they appeared, a high and low price, and a first and last appearance year.

Menu contains a collection of sponsors, events, venue types, venue name and general location, a description of the physical menu, the occasion for the meal, notes about the physical menu, a "call number", keywords and language (both blank), the date of the menu, a location type (unused), the currency on the menu (sparely used), a currency symbol (used when currency is designated), a status field (presumably for an internal workflow), a menu page count, and the number of dishes on the menu. 5 menus indicate a different number of pages than are actually stored in the MenuPage table.  217 Menus also differ in the number of Dishes stored versus the number of dishes referenced in the 'dish_count' column.  In each instance, only the first page number is stored.  Additionally, some "pages" seemingly contain hundreds of dishes, which calls into question whether the page_number column is actually used in a semantically consistent way.  Physical description is really a separate collection of "tags" that describe the menu.  It would be better as a separate table. Occasion is also potentially tags, but the format is varied.  Sometimes it is semi-colon delimited, sometimes it is not delimited, sometimes values are in hard-brackets (and limited to 8 characters).  Most commonly, occasion and physical description are blank or null.  Some menus are aggregates of multiple menus, such as ids 31054 and 31230, that include descriptions such as "62 menus bound into 1 volume".

MenuPage is a collection of information about individual physical pages for a menu.  It contains a reference to a menu_id and a page number. (1202 have no page number, however.) A "image_id" that presumably references an image in another table, but there is no provided table that it references.  (23 rows in image_id include non-numeric values.)  There is also a full_height and full width that seems to indicate the image size in pixels, though some appear incorrect or are altogether missing (329).  Finally, there is a uuid field that, while there are many distinct values, lacks a consistent format (some are upper case, while most are lower) and there is no indication what it references. 5789 MenuPage rows are missing their referenced Menus.

MenuItem is a collection of individual dishes that appear on a menu page, along with the price of the dish (445,916 blank) (and a high_price column with only 91,905 populated), a reference to the dish in the Dish table (241 are blank), when it was created and update (or more accurately, when the database entry was created and updated).  It also contains the xpos and ypos which are in the domain [0,1) (using SQL query `select min(xpos), max(xpos), min(ypos), max(ypos) from MenuItem;`).  Presumably this is the location, relative to the overall width and height of the dish on the menu.  It does not, however indicate origin (i.e. is (0,0) the top-left or bottom left of the page?) Nor does it indicate whether the position is the center of the block or whether it is a corner of a block.  Price does not indicate units so, presumably, by joining MenuItem to MenuPage and then to Menu, one could (sometimes) discern the price AND the currency of the price.  
35 MenuItems are missing their referenced MenuPages and 244 MenuItems are missing their referenced Dish.

    a. Here you will provide an ER diagram, an ontology, or a detailed database schema (10 points), and
    b. a narrative description of the dataset covering structure and content (15 points)

### Use Cases (30 points)
    a. Target (Main) use case U1: data cleaning is necessary and sufficient (20 points)
    b. “Zero data cleaning” use case U0: data cleaning is not necessary (5 points)
    c. “Never enough” use case U2 : data cleaning is not sufficient (5 points)
            Anything involving knowing true prices because the currency is very sparse.  We can guess, but never know, that the prices are in comparable units.

### Data Quality Problems (30 points)
    a. List obvious data quality problems with evidence (examples and/or screenshots) (20 points)
        Denormalized schema: not good for data quality.  Likely for a front-end application.
        1. Dish
        1. Menu
        1. MenuItem
        1. MenuPage
            No indication of the use for uuid.  Some rows with identical menu_ids and different page numbers have transposed full_height and full_width values indicating that one page is, possibly, rotated.
            Image_id appears like a foreign key, but see the import errors.
            MenuPage.csv:
                image_id uses mixed types
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

    b. Explain why / how data cleaning is necessary to support the main use case U1 (10 points)

### Initial Plan for Phase-II (15 points)
    Below is a possible plan, listing typical data cleaning workflow steps. In your Plan for Phase-II, fill in additional details for the project steps as needed. In particular, include who of your team members will be responsible for which steps, and list the timeline that you are setting yourselves!
    - S1: Review (and update if necessary) your use case description and dataset description
    - S2: Profile D to identify DQ problems: How do you plan to do it? What tools are you going to use?
    - S3: Perform DC “proper”: How are you going to do it? What tools do you plan to use? Who does what?
    - S4: Data quality checking: is D’ really “cleaner” than D? Develop test examples / demos
    - S5: Document and quantify change (e.g. columns and cells changed, IC violations detected: before vs after, etc.)
