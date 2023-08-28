# Data from FreedomHouse.org

Publications are listed here: <https://freedomhouse.org/reports/publication-archives>

"Country and Territory Ratings and Statuses, 1973-2023 (Excel
Download)" is the second download link, and is saved in this directory
as "Country_and_Territory_Ratings_and_Statuses_FIW_1973-2023 .xlsx"

It has several tabs, including detailed prose documentation on the
first tab.  The second tab is "Country Ratings, Statuses" and its
right-most column is "EU" and shows the 2022 "Status" value published
in 2023.  The values in the status column are "NF" for "not free" "PF"
for "partially free" and "F" for "free" ... however, this file is not
as useful, because it focuses on summarizing data all the way back to
1973 and there were significant changes to the scoring process along
the way.

the more useful file is
"Aggregate_Category_and_Subcategory_Scores_FIW_2003-2023.xlsx" which
is simpler and has the modern score structure.  Its "INDEX" tab says:

'''
This workbook lists all publicly available data by survey year
(e.g. survey FIW2003 analyzes calendar year 2002).  The same
indicators were present from FIW2003 through FIW2017.  In FIW2018, Add
A (Additional Discretionary Question A) was eliminated, and Add B
(Additional Discretionary Question B) was renamed Add Q.  For
data-analysis purposes, Freedom in the World divides countries and
territories into six world regions: Africa, the Americas,
Asia-Pacific, Eurasia, Europe, and the Middle East. Prior to the 2022
edition, the countries of North Africa were grouped with the Middle
East rather than the rest of Africa.

Key

C/T? indicates whether the entry is a country (c) or territory (t)
F=Free, PF=Partly Free, NF=Not Free
PR Rating=Political Rights Rating
CL Rating=Civil Liberties Rating

A Aggr=aggregate score for the A. Electoral Process subcategory
B Aggr=aggregate score for the B. Political Pluralism and Participation subcategory
C Aggr=aggregate score for the C. Functioning of Government subcategory
Add Q (Add B)=score for Additional Discretionary Question (B)
Add A=score for Additional Discretionary Question A
PR Aggr=aggregate score for the Political Rights category
D Aggr=aggregate score for the D. Freedom of Expression and Belief subcategory
E Aggr=aggregate score for the E. Associational and Organizational Rights subcategory
F Aggr=aggregate score for the F. Rule of Law subcategory
G Aggr=aggregate score for the G. Personal Autonomy and Individual Rights subcategory
CL Aggr=aggregate score for the Civil Liberties category
Total Aggr=aggregate score for all categories
'''

It's second tabs has those fields as columns.  The freedomhouse.csv
file contains the key fields only for the 2023 edition, which means
data from the year 2022.

- "Country/Territory" --> name
- region
- "C/T?" --> country_or_territory
- status
- "Total" --> score

I built this csv manually by copying the block of 2023 out of the
"Aggregate....xlsx" file into a new Google Sheets spreadsheet,
deleting the columns we don't plan to use and renaming the two
headers.  Then download as .csv

The __init__.py in this directory reads the CSV and offers
`typing.NameTuple` objects for each.

freedomhouse.places, which is a dictionary keyed on the name of the
country and the values are the typing.NamedTuple objects created from
the rows of the CSV.

Also, the package offers freedomhouse.FreedomStatus, which is an enum.
