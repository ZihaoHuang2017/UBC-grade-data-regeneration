# UBC-grade-data-regeneration
In the year of 2023, UBC PAIR stopped giving out the entirety of score distribution nor the standard deviation (The letter grades with fewer than 6 entries are removed). This has made the analysis on prior results much harder. Fortunately the score of the lower and higher quantile are given, so assuming a mostly normal distribution one could figure out the relative proportions of each letter grade, and multiply them to achieve an estimate of the persons that are in that grade bracket. 

This tool will work the best if there's only 1 or 2 fields missing or if the lowest/highest score are somewhat close. I do not guarantee that the generated result will be accurate at all.

## LIMITS
This tool doesn't consider the possiblities of:
- Bimodal Distribution (Common in courses like CPSC 110, where you fail the entire course if you fail the combined average of exams)
- Skewed results (Happens when the presumed mean is quite different from the actual average)
- Pure chaos (MATH 320)

## How to use it
You will need to have Python configured.
1. Fill INITIAL_ARR with the existing score distribution, put 0s if data is not found.
2. Fill LO, HI according to the lowest/highest score.
3. Fill QUANTILE_25, QUANTILE-75 according to the 25th/75th percentile score.
4. Fill TOTAL_POP according to the Reported section.
5. Run the file. The newly generated list represents the most possible scenario.

## Future potential expansions
- Use .csv data directly
- Round the numbers to be integers (D'Hondt or Huntington-Hill?)
- Make some of the logics run slightly faster