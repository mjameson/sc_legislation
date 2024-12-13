import requests
from bs4 import BeautifulSoup
import csv
import re
import sys
import argparse

def scrape_bill_summary(bill_number, session_number, chamber):
    base_url = "https://www.scstatehouse.gov/billsearch.php"
    bill_url = f"{base_url}?billnumbers={bill_number.zfill(4)}&session={session_number}&summary=B"

    print(f"Fetching Summary from: {bill_url}")

    response = requests.get(bill_url)
    if response.status_code != 200:
        print(f"Failed to fetch summary for Bill {bill_number}. HTTP Status: {response.status_code}")
        return ''

    soup = BeautifulSoup(response.text, 'html.parser')
    summary_label = soup.find('b', string='Summary:')
    if summary_label and summary_label.next_sibling:
        summary_text = summary_label.next_sibling.strip()
        return summary_text
    else:
        print(f"Summary not found for Bill {bill_number}.")
        return ''

def process_prefile(prefile_url, limit=None):
    # Extract metadata from the URL
    match = re.search(r'sess(\d{3})_(\d{4})-\d{4}/(hpref|spref)(\d{2})/pref\d{2}(h|s)(\d+)\.htm', prefile_url)
    if not match:
        print(f"Invalid URL format: {prefile_url}")
        sys.exit(1)

    session_number = match.group(1)
    year = match.group(2)
    chamber_prefix = match.group(3)
    chamber = "House" if chamber_prefix == "hpref" else "Senate"
    prefile_number = match.group(6)

    print(f"Processing: Session {session_number}, Year {year}, Chamber {chamber}, Prefile {prefile_number}")

    # Fetch prefile data
    response = requests.get(prefile_url)
    if response.status_code != 200:
        print(f"Failed to access {prefile_url}. HTTP Status: {response.status_code}")
        return

    soup = BeautifulSoup(response.text, 'html.parser')
    bill_links = soup.find_all('a', href=lambda href: href and 'billnumbers' in href)
    print(f"Found {len(bill_links)} potential bill entries.")

    if limit:
        bill_links = bill_links[:limit]

    data = []

    for link in bill_links:
        # Extract bill number and remove prefix (H. or S.)
        raw_bill_number = link.text.strip()
        bill_number = re.sub(r'^[HhSs]\.\s*', '', raw_bill_number)

        # Fetch summary dynamically
        summary = scrape_bill_summary(bill_number, session_number, chamber)

        # Extract Word document link
        word_link_tag = link.find_next('a', href=lambda href: href and href.endswith('.docx'))
        word_link = f"https://www.scstatehouse.gov{word_link_tag['href']}" if word_link_tag else ''

        # Extract representative/sponsor
        description = link.find_next('a', href=lambda href: href and href.endswith('.docx')).find_next_sibling(
            text=True)
        representative = ''
        if chamber == 'House':
            rep_match = re.search(r'Reps?\.\s+(.+?):', description)  # Match "Rep." or "Reps."
            if rep_match:
                representative = rep_match.group(1).strip()  # Capture everything after "Reps."
        elif chamber == 'Senate':
            senator_match = re.search(r'Senators?\s+(.+?):', description)  # Match "Senator" or "Senators"
            if senator_match:
                representative = senator_match.group(1).strip()  # Capture everything after "Senators"

        # Clean up representative list (handle "and", commas, etc.)
        representative = re.sub(r'\s+and\s+', ', ', representative)  # Replace "and" with commas
        representative = representative.strip()

        # Extract committee information
        committee_tag = word_link_tag.find_next('center') if word_link_tag else None
        committee = committee_tag.get_text(strip=True) if committee_tag else 'Unknown Committee'

        # Clean the Committee column
        committee = re.sub(r'^Prefiled and referred to the Committee on ', '', committee)
        committee = re.sub(r'^Referred to Committee on ', '', committee)

        # Ensure Preamble starts with "A "
        preamble_start = description.find("A ") if description else -1
        preamble = description[preamble_start:].strip() if preamble_start != -1 else ''

        print(f"Processed Bill: {bill_number}, Summary: {summary}, Rep: {representative}, Committee: {committee}, Preamble: {preamble}")

        data.append([bill_number, summary, chamber, representative, committee, preamble, word_link])

    # Save data to CSV
    output_filename = f"{year}_{session_number}_{chamber}_Prefile_{prefile_number}.csv"
    with open(output_filename, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Bill Number', 'Short title/summary', 'Chamber', 'Sponsors (Representatives)', 'Committee', 'Preamble', 'Word Link'])
        writer.writerows(data)

    print(f"Data extraction and CSV creation done. Check {output_filename} file.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process South Carolina legislative prefile data.")
    parser.add_argument("prefile_url", help="URL of the prefile HTML file")
    parser.add_argument("--limit", type=int, default=None, help="Limit the number of entries to process (default: no limit)")

    args = parser.parse_args()
    process_prefile(args.prefile_url, args.limit)