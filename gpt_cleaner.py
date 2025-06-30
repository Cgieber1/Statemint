from openai import OpenAI
from dotenv import load_dotenv
import os
import csv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def clean_bank_text_with_gpt(text):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant that extracts and cleans bank statement data."
            },
            {
                "role": "user",
                "content": f"""Here is some raw bank statement text:

{text}

Please extract each transaction and format it as a table with the following columns:

- Date (format as 'Apr 24, 2025')
- Description
- Amount (use negative for debits)
- Type ('Credit' or 'Debit')
- Category (guess if not obvious)

Return the result as a markdown table with headers. Do not include anything else but the table itself."""
            }
        ]
    )
    return response.choices[0].message.content

def save_to_csv(data, filename="cleaned_statement.csv"):
    lines = data.strip().split("\n")
    cleaned_rows = []
    seen_header = False

    for line in lines:
        if line.startswith("|") and not line.startswith("|---"):
            cells = [cell.strip() for cell in line.strip().split("|")[1:-1]]
            if cells == ["Date", "Description", "Amount", "Type", "Category"]:
                if seen_header:
                    continue  # skip duplicate header
                seen_header = True
                continue  # don't include header in data rows
            if len(cells) == 5:
                cleaned_rows.append(cells)

    with open(filename, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Date", "Description", "Amount", "Type", "Category"])
        writer.writerows(cleaned_rows)

if __name__ == "__main__":
    with open("raw_text.txt", "r") as f:
        raw_text = f.read()
    cleaned_table = clean_bank_text_with_gpt(raw_text)
    save_to_csv(cleaned_table)
    print("✅ Saved to cleaned_statement.csv")
