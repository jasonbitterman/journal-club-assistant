# Importing basics

import os
import requests
import time
from io import BytesIO
from openai import OpenAI
import argparse
from urllib.parse import urlparse
from dotenv import load_dotenv

load_dotenv()

client = OpenAI()

nooptions = 0

customized_instructions_items = {
    "studyaim": {
        "description": "Extract the aim of the study from the paper.",
        "heading": "Aim of Study",
    },
    "studydesign": {
        "description": "Extract the study design from the paper.",
        "heading": "Study Design",
    },
    "intervention": {
        "description": "Extract the intervention or test being assessed by the study from the paper.",
        "heading": "Intervention",
    },
    "subjects": {
        "description": "Extract the number of subjects in each group from the paper.",
        "heading": "Number of Subjects",
    },
    "inclexclcriteria": {
        "description": "Extract the inclusion and exclusion criteria for the subjects from the paper.",
        "heading": "Inclusion and Exclusion Criteria",
    },
    "primaryoutcome": {
        "description": "Extract the primary outcome measure(s) from the paper.",
        "heading": "Primary Outcome",
    },
    "secondaryoutcome": {
        "description": "Extract the secondary outcome measure(s) from the paper.",
        "heading": "Secondary Outcome",
    },
    "statisticalmethods": {
        "description": "Extract the statistical methods used in the paper.",
        "heading": "Statistical Methods",
    },
    "baselinecharacteristics": {
        "description": "Extract the differences between the baseline characteristics for the groups of subjects (if there are differences, be specific in which group had the difference in a certain way. If there is no difference in baseline characteristics, state this as well).",
        "heading": "Baseline Characteristics",
    },
    "resultsprimary": {
        "description": "Extract the results for all of the primary outcome measure(s) from the paper. Be clear the direction of results with regard to the groups.",
        "heading": "Primary Outcome Results",
    },
    "resultssecondary": {
        "description": "Extract the results for all of the secondary outcome measure(s) from the paper.",
        "heading": "Secondary Outcome Results",
    },
    "analysis": {
        "description": "In only 1 or 2 paragraphs (do not exceed 2 paragraphs), give your analysis of the paper on whether their conclusions are valid based on what is presented (think about things like issues in the methods, limitations of the inclusion/exclusion criteria for the patient population studies, loss of patients to followup or crossover of patients between groups, certain results being elided in the discussion or abstract sections, intention to treat vs per protocol results, whether statistically significant findings are truly clinically meaningful, etc). Err on the side of being analytical and harsh, do not simplify or be generous.",
        "heading": "Analysis",
    },
}


def create_file(client, file_path):
    if file_path.startswith("http://") or file_path.startswith("https://"):
        # Download the file content from the URL
        response = requests.get(file_path)
        file_content = BytesIO(response.content)
        file_name = file_path.split("/")[-1]
        file_tuple = (file_name, file_content)
        result = client.files.create(file=file_tuple, purpose="user_data")
    else:
        # Handle local file path
        with open(file_path, "rb") as file_content:
            result = client.files.create(file=file_content, purpose="user_data")
    print(f"File uploaded with ID: {result.id}")
    return result.id


def create_custom_input_prompt(options):
    customized_instructions_text = ""

    if options["summary"] == True:
        for option in [
            k for k in customized_instructions_items.keys() if k != "analysis"
        ]:
            instructions_item = customized_instructions_items[option]
            customized_instructions_text += (
                instructions_item["description"]
                + f" Give this section a heading of ## {instructions_item['heading']}."
                "\n"
            )

    if options["analysis"] == True:
        instructions_item = customized_instructions_items["analysis"]
        customized_instructions_text += (
            instructions_item["description"]
            + f" Give this section a heading of ## {instructions_item['heading']}."
            "\n"
        )

    return (
        "Extract the specific title of the paper, precede the title with ##. Then, extract the following information from this paper (insert a new line between each section):\n"
        + customized_instructions_text
    )


def main():
    parser = argparse.ArgumentParser(
        description="A script that summarizes and analyzes PDFs of medical papers."
    )
    parser.add_argument(
        "file_name",
        type=str,
        help="Path to the PDF file or the URL of the PDF you want to summarize",
    )

    parser.add_argument(
        "--hide-analysis",
        dest="analysis",
        action="store_false",
        help="Exclude analysis",
    )

    parser.add_argument(
        "--hide-summary", dest="summary", action="store_false", help="Exclude summary"
    )
    parser.set_defaults(summary=True)

    args = parser.parse_args()

    file_name = args.file_name

    # Getting the file either from a URL or locally
    file_id = create_file(client, file_name)

    # Create a vector store
    vector_store = client.vector_stores.create(name="knowledge_base")
    print(f"Vector store created with ID: {vector_store.id}")

    # Add the file to the vector store
    file_in_vector_store = client.vector_stores.files.create(
        vector_store_id=vector_store.id, file_id=file_id
    )
    print(f"File added to vector store with ID: {file_in_vector_store.id}")

    time.sleep(20)
    print("Waiting for file to be processed...")

    options = {
        "summary": args.summary,
        "analysis": args.analysis,
    }

    input_prompt = create_custom_input_prompt(options)

    # %
    response = client.responses.create(
        model="gpt-4.1",
        instructions="You are an expert peer reviewer for a medical journal. You analyze papers very carefully and have a keen eye for details and potential issues with methodology, results, and conclusions. You also look for discrepancies between the data and how the authors choose the discuss the results. Return your response in markdown format.",
        input=input_prompt,
        tools=[{"type": "file_search", "vector_store_ids": [vector_store.id]}],
    )

    # Save response to markdown file
    if file_name.startswith("http://") or file_name.startswith("https://"):
        # Extract the filename from the URL
        parsed_url = urlparse(file_name)
        base = os.path.basename(parsed_url.path)
    else:
        base = os.path.basename(file_name)

    if base.lower().endswith(".pdf"):
        filename = base[:-4] + "_summary.md"
    else:
        filename = base + "_summary.md"

    with open(filename, "w") as f:
        f.write(response.output_text)
    print("File summary created.")


if __name__ == "__main__":
    main()
