
# Journal Club Assistant 
Your AI-powered companion for efficient medical research paper analysis

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

## How to Use Journal Club Assistant
The tool runs directly off the command line. Enter the following in the command line: 

`python filesearch_test_flags.py '<file_name>'`

<file_name> refers to the path to the PDF file on your computer or can refer to the URL of a freely available PDF you want to summarize.

If you want to exclude the program from performing the AI-Generated Analysis setion, enter the following instead:

`python filesearch_test_flags.py --hide-analysis '<file_name>'`

In this situation, the program will only generate the Summary information from the paper (e.g. study aim, intervention details, subjects, results, etc.).

## Examples
Journal Club Assistant was asked to create a summary of a PDF of this classic New England Journal of Medicine article on the DASH diet: https://www.nejm.org/doi/full/10.1056/NEJM199704173361601. The generated file is available at [examples/NEJM DASH_summary.md](examples/NEJM%20DASH_summary.md)

Another example: Journal Club Assistant was provided a more recent NEJM article regarding intraarterial alteplase for acute ischemic stroke (https://www.nejm.org/doi/full/10.1056/NEJMoa1411587). The generated file is available at [examples/NEJM MRCLEAN RCT_summary.md](examples/NEJM%20MRCLEAN%20RCT_summary.md)

