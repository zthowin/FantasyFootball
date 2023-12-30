# FantasyFootball
This repository contains the data, code used for analysis, and report template(s) for a rudimentary statistical analysis of a season's worth of Fantasy Football data for the 'COC Squad' and 'ThisLeague' Fantasy Football leagues.

## Requirements
- Python 3.x
- Numpy
- Matplotlib
- statsmodels
- pdflatex, with the following non-standard packages:
	- bookcaptions
	- subfigure
	- titling
- Working knowledge of bash shell
	
## How to use
Begin by initializing an environment variable that corresponds to the directory of the league of interest, e.g.,

	`export LEAGUE=/home/user/Documents/FantasyFootball/COC_Squad`

Once set, make `ffAnalysis` an executable.

Run options can be invoked with the `--help` flag.

Note: `report.tex` must be placed inside the `LEAGUE/year/` directory to be compiled correctly.
