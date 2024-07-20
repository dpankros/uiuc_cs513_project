# Intengrity Constraints

## Dish

- id must be populated and unique
- name must be populated
- menus_appeared should be greater than 0
- times_appeared should be greater than 0
- first appeared should be between (?? and NOW)
- last appeared should be between (?? and NOW)
- lowest_price should be > 0
- highest_price should not be null and should be > lowest_price


## Menu

- id must be populated and unique
- name must be populated
- sponsor
- event
- venue
- place
- physical_description must be a list of string demlimited by semicolons
- occasion
- notes
- call_number
- keywords
- language
- date must be in iso8601 format
- location
- location_type
- currency
- currency_symbol
- status must be one of the two values
- page_count > 0
- dish_count > 0

## Menu Page
- id must be populated and unique
- menu_id must be defined and menu.id must exist
- page_number
- image_id
- full_height Must be > 0
- full_width Must be > 0
- uuid

## Menu Item
- id must be populated and unique
- menu_page_id must be defined and menu_page.id must exist
- price > 0 or null
- high_price
- dish_id must exist
- created_at should be in iso8601 format.  Must be defined.  Must be <= NOW
- updated_at should be in iso8601 format Must be <= NOW
- xpos
- ypos
