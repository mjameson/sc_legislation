import requests
from bs4 import BeautifulSoup
import csv

def scrape_bill_summary(bill_number):
    bill_url = f"https://www.scstatehouse.gov/billsearch.php?billnumbers={bill_number}&session=126&summary=B"
    response = requests.get(bill_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    summary_div = soup.find('div', class_='bill-list-item')
    if not summary_div:
        print(f"Could not find summary for bill number: {bill_number}")
        return ''
    summary_label = summary_div.find('b', string='Summary:')
    if not summary_label:
        print(f"Could not find 'Summary:' label for bill number: {bill_number}")
        return ''
    summary_text = summary_label.next_sibling
    return ' '.join(summary_text.strip().split()) if summary_text else ''

#main_url = 'https://www.scstatehouse.gov/sess125_2023-2024/hpref24/pref24h1.htm' #2024
#main_url = 'https://www.scstatehouse.gov/sess125_2023-2024/spref24/pref24s0.htm' #2024
#main_url = 'https://www.scstatehouse.gov/sess126_2025-2026/hpref25/pref25h1.htm' #2025
main_url = 'https://www.scstatehouse.gov/sess126_2025-2026/hpref25/pref25s0.htm' #2025

main_response = requests.get(main_url)
main_page_content = main_response.text
main_soup = BeautifulSoup(main_page_content, 'html.parser')

bill_links = main_soup.find_all('a', href=lambda x: x and 'billnumbers' in x)
data = []

for link in bill_links:
    bill_number = link['href'].split('=')[1].split('&')[0]
    bill_name = link.text.strip()
    print(f"Processing Bill: {bill_name}")

    summary = scrape_bill_summary(bill_number)

    # Parsing representative information
    rep_paragraph = link.find_next('p')
    if rep_paragraph and '--' in rep_paragraph.text:
        rep_info = rep_paragraph.text.split('--')[1].split(':')[0].strip()
    else:
        rep_info = ''

    # Parsing committee information
    committee_paragraph = rep_paragraph.find_next('center') if rep_paragraph else None
    committee_info = committee_paragraph.text.strip() if committee_paragraph else ''

    data.append([bill_name, summary, rep_info, committee_info])

csv_filename = 'sc_senate_detailed.csv'
with open(csv_filename, 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Bill Name', 'Summary', 'Representative', 'Committee'])
    writer.writerows(data)

print(f"Data extraction and CSV creation done. Check {csv_filename} file.")

