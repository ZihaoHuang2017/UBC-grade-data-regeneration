# UBC-grade-data-regeneration
In the year of 2023, UBC PAIR stopped giving out the entirety of score distribution nor the standard deviation (The letter grades with fewer than 6 entries are removed). This has made the analysis on prior results much harder. Fortunately the score of the lower and higher quantile are given, so assuming a mostly normal distribution one could figure out the relative proportions of each letter grade and allocate a number of students to the proportions. 

This tool will work the best if there's only 1 or 2 fields missing or if the lowest/highest score are somewhat close. I do not guarantee that the generated result will be accurate at all.

## LIMITS
This tool doesn't consider the possiblities of:
- Bimodal Distribution (Common in courses like CPSC 110, where you fail the entire course if you fail the combined average of exams)
- Skewed results (Happens when the presumed mean is quite different from the actual average)
- Pure chaos (MATH 320)
- Too many dropped students/grade entry error (2022W MATH 100 1A1 - either 154 students dropped out or the grades are incorrectly inputed)

## How to use it
You will need to have Python configured.
1. Fill INITIAL_ARR with the existing score distribution, put 0s if data is not found.
2. Fill QUANTILE_25, QUANTILE_75, HI, LO, TOTAL_POP according to the stats provided.
3. Run the file. The newly generated list represents the most possible scenario according to D'Hondt method of allocation.

## Examples
Fields that are *italicized* are generated; Fields that are **bolded** are generated results that contain error and should be adjusted.

2022W CPSC 110 101:

[39, *0*, *1*, *3*, **6**, 6, 15, 25, 39, 59, 70]

2022W WRDS 150B 510:

[*1*, *0*, *0*, *1*, *2*, *3*, 10, 6, *5*, *0*, *0*]

2022W SCIE 113 108:

[*1*, *0*, *0*, *0*, *0*, *0*, *0*, *2*, *4*, 7, 11]

2022W JAPN 320 003 (No information given):

[*0*, *0*, *0*, *1*, *1*, *1*, *2*, *2*, *2*, *2*, *2*]

2022W JAPN 320 003 (Provided that there's only 1 A+ student):

[*0*, *0*, *0*, *1*, *1*, *1*, *2*, *2*, *3*, *2*, 1]
## Future potential expansions
- Use .csv data directly