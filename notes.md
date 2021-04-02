Questions for Renee:
- who collects this data? how often updated? who updates it?
    - every year, new inspections are appended to this spreadsheet
- do we want visualization tools for the stored database only, or any other data that people want to upload (this is harder)?
    - we want for this data, but also new data uploaded every year
    - ideally we want to automate the process (collect data in an ipad and uploaded to the cloud)

# Meeting with Renee (9/22)
- seed certification: check growers to certify their seed
- check for viruses and also that they are the right variety

- they want two main things:
    - better database
    - models for trends

- there will be info on yield later (we want to predict it)

- data: each row is a sample of potato (seed potato lot)
    - there is a difference between grower (where the potato is grown) and source (where the tubers came from). they are certifying the grower

- what do we want to see in this data?
    - trends: in inspection, they check if plants have virus and if they are the right variety
    - NO_MOS: number of mosaic virus plants; our viruses start ub column Z NO_LR
    - NO_MIX: not correct variety

Questions: at some point it would be good to know what type of plots are good to do.

# Data
Emailed by Renee: `2003-2016 Seed Potato Cert data v20191204_NO FL lines_Rioux 5AUG2020.xlsx`

See `2021-WPVGS-potato` for a cleaned dataset and short description.


Meeting minutes 10/14:
- Haoming continued to check the data discrepancies between summer and winter:
    - SNAME (most discrepancies related to State Farm). It seems that S_GRW was used instead of SNAME
    - He is fixing some of the easy discrepancies (making sure that the chosen spelling does not disagree with other columns)
    - STATE has 8 errors still
    - S_YR has still 60 errors that we can not solve
- On the visualization, Haoming created a Dash board with bar plots that nicely illustrate viruses per state for different years. It was unclear what the data meant (which year)
- Haoming identified that winter_MOS had an inconsistent scale compared to other virus columns (that are mostly between 0,1)

Next steps:
- Do a report of the data inconsistencies for our meeting with Renee
- Continue working with visualizations: maybe do scatterplots with different point shapes per year; investigate what is being plotted (in terms of year) in the bar plots
- Continue planning next steps of analysis: tests of significant factors associated with presence of virus (environment, season, ...)