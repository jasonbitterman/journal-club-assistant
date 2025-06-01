
# Journal Club Assistant 
Your AI-powered companion for efficient medical research paper analysis

## Examples

| Original Article | AI Generated Summary & Analysis |
| ------ | ----- |
| [DASH Diet NEJM Article](https://www.nejm.org/doi/full/10.1056/NEJM199704173361601) | [Check it out here](examples/NEJM%20DASH_summary.md) |
| [MRCLEAN RCT NEJM Article](https://www.nejm.org/doi/full/10.1056/NEJMoa1411587) | [Check it out here](examples/NEJM%20MRCLEAN%20RCT_summary.md) |


## Overview

Journal Club Assistant streamlines the process of analyzing medical research papers by automatically extracting and organizing key information. 

This assistant processes any research paper PDF and structures the information into an easy-to-digest format. It extracts essential data that's often scattered throughout lengthy academic papers, saving you valuable time and ensuring no critical details are missed.

## Features

### Summary
The assistant generates clear and concise markdown summaries of research papers from PDFs, focusing in on the following key elements of the submitted paper: 

- Study aim and design
- Intervention details
- Subject demographics and grouping
- Inclusion/exclusion criteria
- Primary and secondary outcome measures
- Statistical methodology
- Baseline characteristics
- Detailed results analysis

### AI-Generated Analysis
Users can also choose to have the assistant generate a focused analysis of the submitted research paper. This analysis includes assessment of:

- Potential validity of the reported findings
- Study design limitations
- Clinical significance of reported results
- Commentary on whether the authors' conclusions correlate with the methodology and results

This analysis is not meant to replace your own critical assessment of the research paper, it should only be used as a potential starting point for analyzing papers. Users should also recognize the limitations of large lanugage models in generating analyses like this.

## How to Use Journal Club Assistant

Prior to running the program, you will need to:
1. Install the dependencies: `pip install -r requirements.txt`
2. Create a .env file, and add your openai key: `OPENAI_API_KEY= <your OpenAI key>`

In the command line, run: 

`python journal_club_assistant.py '<file_name>'`

<file_name> refers to the path to the PDF file on your computer or can refer to the URL of a freely available PDF you want to summarize.

### Options

If you want to exclude the program from creating the Analysis section, enter the following instead:

`python journal_club_assistant.py --hide-analysis '<file_name>'`

In this situation, the program will only generate the Summary information from the paper (e.g. study aim, intervention details, subjects, results, etc.).


