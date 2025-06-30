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
            {"role": "system", "content": "You're a financial data formatter."},
            {"role": "user", "content": f"Extract a clean table from this text:\n{text}"}
        ]
    )
    return response.choices[0].message.content

def save_to_csv(data, filename="cleaned_statement.csv"):
    rows = [line.split(" | ")[1:-1] for line in data.strip().split("\n")[2:]]
    with open(filename, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Date", "Description", "Amount", "Type", "Category"])
        writer.writerows(rows)

if __name__ == "__main__":
    with open("raw_text.txt", "r") as f:
        raw_text = f.read()
    cleaned_table = clean_bank_text_with_gpt(raw_text)
    save_to_csv(cleaned_table)
    print("✅ Saved to cleaned_statement.csv")
