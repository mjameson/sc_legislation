# SC Legislation Prefile Scraper

This Python script extracts legislative information from the South Carolina Statehouse website. It processes prefiled bills for a given session and generates a CSV file containing details such as bill numbers, summaries, sponsors, committees, and more.

## Features

- Extracts legislative details from a specified prefile URL.
- Handles both House and Senate chambers dynamically.
- Outputs data in a structured CSV format.
- Supports a limit on the number of entries for testing or smaller datasets.
- Automatically names the output file based on session, year, chamber, and prefile number.

---

## Requirements

### Dependencies

Ensure the following Python libraries are installed:

- `requests`
- `beautifulsoup4`

Install them with pip if needed:

```bash
pip install requests beautifulsoup4
```

Python Version

The script is compatible with Python 3.x.

Usage

Command Syntax

python3 sc_legislation.py <prefile_url> [--limit <number>]

Parameters
    •    <prefile_url>: The URL of the prefile HTML file (e.g., https://www.scstatehouse.gov/sess126_2025-2026/hpref25/pref25h2.htm).
    •    --limit <number> (optional): Limits the number of entries processed. If omitted, the script processes all available entries.

Examples
    1.    Process All Entries:

```python
sc_legislation.py https://www.scstatehouse.gov/sess126_2025-2026/hpref25/pref25h2.htm
```

2. Process the First 3 Entries for Testing:

```python
python3 sc_legislation.py https://www.scstatehouse.gov/sess126_2025-2026/hpref25/pref25h2.htm --limit 3
```

Output

The script generates a CSV file named based on the session, year, chamber, and prefile number. For example:
    •    2025_126_House_Prefile_2.csv
    •    2025_126_Senate_Prefile_1.csv

### CSV Columns

The output CSV includes the following columns:

| Column Name                    | Description                                        |
| ------------------------------ | -------------------------------------------------- |
| **Bill Number**                | The numeric portion of the bill ID (e.g., `3563`). |
| **Short title/summary**        | A brief summary of the bill.                       |
| **Chamber**                    | Either `House` or `Senate`.                        |
| **Sponsors (Representatives)** | Names of the sponsors (e.g., `Davis, B. J. Cox`).  |
| **Committee**                  | The committee assigned to the bill.                |
| **Preamble**                   | The bill’s full description starting with “A”.     |
| **Word Link**                  | Link to the Word document version of the bill.     |

### How It Works

1. The script parses the provided `prefile_url` to extract metadata (e.g., session, year, chamber, prefile number).
2. It fetches the HTML content of the URL and identifies legislative entries.
3. For each bill:
   - Extracts the bill number, summary, sponsors, committee, and preamble.
   - Fetches additional details, such as the Word document link.
4. Outputs the data into a well-structured CSV file.

---

### Troubleshooting

- **HTTP Errors**: Ensure the provided `prefile_url` is valid and accessible.
- **Missing Data**: If certain fields (e.g., sponsors or committees) are empty, check the HTML structure of the source page for inconsistencies.
- **Dependencies**: Verify that `requests` and `beautifulsoup4` are installed.

---

### Contributing

Feel free to fork this project and submit pull requests for enhancements or bug fixes. Feedback and suggestions are always welcome!

---

### License

This project is open-source and available under the [MIT License](LICENSE).
