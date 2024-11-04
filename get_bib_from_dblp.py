import urllib.request
import urllib.parse
import json
from datetime import datetime
import re
import time
import csv

def sort_bibtex_entries_by_timestamp(bibtex_entries: list) -> list:
    """Sorts BibTeX entries based on the timestamp field in descending order."""

    def extract_timestamp(entry: str) -> datetime:
        match = re.search(r'timestamp\s*=\s*\{([^}]+)\}', entry)
        if match:
            try:
                return datetime.strptime(match.group(1), '%a, %d %b %Y %H:%M:%S %z')
            except ValueError:
                pass
        return datetime.min

    sorted_entries = sorted(bibtex_entries, key=extract_timestamp, reverse=True)
    
    return sorted_entries

def search(query: str) -> None:
    """Searches for a publication and retrieves the top 3 matches."""
    options = {"q": query, "format": "json", "h": 3} # 3 hits
    output = ""
    url = f"https://dblp.org/search/publ/api?{urllib.parse.urlencode(options)}"
    with urllib.request.urlopen(url) as response:
        data = json.loads(response.read().decode())
        hit = data.get("result", {}).get("hits", {}).get("hit", [])

        if hit:
            for item in hit:
                info = item.get("info", {})
                title = info.get("title", "No title found")
                output += f"{title} ({info.get('url').replace('https://dblp.org/rec/', '')})\n"
        else:
            print("No results found in DBLP")
    print(output.strip())

    return output.strip().split("\n")

def get_bib_info(bib: str) -> tuple[str, str, str]:
    """Extracts author, title, and year from a given bib entry."""
    author = re.search(r"author\s*=\s*{(.*?)}", bib, re.DOTALL)
    if author is None:
        author = re.search(r"editor\s*=\s*{(.*?)}", bib, re.DOTALL)
    author = author.group(1) if author is not None else "Unknown"
    title = re.search(r"title\s*=\s*{(.*?)}", bib, re.DOTALL).group(1)
    year = re.search(r"year\s*=\s*{(.*?)}", bib).group(1)
    return author, title, year


def format_bib_key(author: str, title: str, year: str) -> str:
    """Formats the bib key using author's last name, first three words of the title, and the year."""
    author_lastname = author.split(" and")[0].split()[-1].lower()
    first_three_words = "".join(
        re.sub(r"[^a-zA-Z]", "", word) for word in title.split()[:3]
    )
    key = f"{author_lastname}{first_three_words}{year}"
    return key


def extract_url(selected_entry: str):
    """Extracts the URL part from the selected entry in the espanso form"""
    pattern = r"\(([^()]*\/.*\/[^()]*)\)$"
    match = re.search(pattern, selected_entry)
    if match:
        return match.group(1)
    else:
        return None


def get_bib(selected_entry: str) -> None:
    """Gets the bib from the selected entry in the espanso form"""
    full_url = f"https://dblp.org/rec/{extract_url(selected_entry)}.bib"
    with urllib.request.urlopen(full_url) as bib_response:
        bib = bib_response.read().decode()
        if "not found" not in bib:
            author, title, year = get_bib_info(bib)
            key = format_bib_key(author, title, year)
            output = re.sub(r"\{DBLP:.*?\,", "{" + key + ",", bib)
        else:
            output = "Not found in DBLP"
    
    return output.strip()

# arxiv_links = [
#     "https://arxiv.org/pdf/1603.00788",
#     "https://arxiv.org/abs/1704.03976",
#     "https://arxiv.org/pdf/1905.02249",
#     "https://arxiv.org/pdf/1807.03748"
# ]

# def extract_arxiv_id(url):
#     match = re.search(r'arxiv\.org/(?:pdf|abs)/(\d+\.\d+)', url)
#     if match:
#         return match.group(1)
#     return None

# arxiv_ids = [extract_arxiv_id(link) for link in arxiv_links if extract_arxiv_id(link)]

# base_url = "http://export.arxiv.org/api/query?id_list="

# titles = []

# for arxiv_id in arxiv_ids:
#     if arxiv_id:
#         url = f"{base_url}{arxiv_id}"
#         with urllib.request.urlopen(url) as arxiv_response:
#             arxiv_response = arxiv_response.read().decode()
#             title_match = re.search(r"<title>(.*?)</title>", arxiv_response)
#             if title_match:
#                 title = title_match.group(1).strip()
#                 titles.append(title)
#             else:
#                 print(f"Failed to fetch metadata for {arxiv_id}")

titles = ['Participation Is not a Design Fix for Machine Learning.', 'Algorithmic Rural Road Planning in India: Constrained Capacities and Choices in Public Sector.', 'The perils of embedded experiments.', 'The Silence of the Subaltern Student.']

# Initialize the CSV file with headers if it doesn't exist
with open("bibtex_entries.csv", "a", newline='') as csvfile:
    writer = csv.writer(csvfile)
    if csvfile.tell() == 0:  # Only write the header if the file is new
        writer.writerow(["Title", "Entry"])

for title in titles:
    print("----------------------------")
    print(title)
    entries = search(title)
    time.sleep(5)
    
    if not entries or entries[0] == "": 
        print("nothing found for ", title)
        entry = None
    else:
        bibtex_entries = [get_bib(entries[0])]  # Assuming the first entry is the latest
        entry = bibtex_entries[0] if bibtex_entries else None
        time.sleep(5)

    with open("bibtex_entries.csv", "a", newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([title, entry])