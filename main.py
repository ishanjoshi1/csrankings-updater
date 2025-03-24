import bs4
import requests
import re
from Levenshtein import ratio


def main():
    url = "https://www.cs.wisc.edu/people/faculty-2/"
    res = requests.get(url)
    soup = bs4.BeautifulSoup(res.text, "html.parser")

    faculty_on_website = {}
    faculty_members = soup.find_all("div", class_="faculty-member-content")

    for member in faculty_members:
        name = re.sub(" +", " ", member.find("h3", class_="faculty-name").text.strip())
        website_links = [
            inner.find("a", href=True)["href"]
            for inner in member.find_all("h3", class_="faculty-name")
            if inner is not None
        ]
        emails = [
            link["href"].removeprefix("mailto:")
            for link in member.find_all("a", href=True)
            if link["href"].startswith("mailto:")
        ]
        faculty_on_website[name] = {
            "email": emails[0] if emails else None,
            "website": website_links[0] if website_links else None,
        }

    # with open('sam_output.txt', 'r') as f:
    #     from ast import literal_eval
    #     ls = literal_eval(f.read())

    # for faculty in ls:
    #     if re.sub(' +', ' ', faculty['name']) not in faculty_on_website:
    #         print(f"Missing {re.sub(' +', ' ', faculty['name'])} on the website.")

    # for faculty in faculty_on_website:
    #     if not any(faculty_ls['name'] == faculty for faculty_ls in ls):
    #         print(f"Extra {faculty} on the website.")

    res = requests.get(
        "https://raw.githubusercontent.com/emeryberger/CSrankings/gh-pages/csrankings.csv"
    )

    if res.status_code != 200:
        print("Error fetching the CSV file.")
        return

    # read the CSV file from the GitHub URL
    csv_data = res.text.splitlines()
    csv_lines = [line.split(",") for line in csv_data]
    csv_header = csv_lines[0]
    csv_rows = csv_lines[1:]

    faculty_on_csrankings = {}

    for line in csv_rows:
        if len(line) != len(csv_header):
            print("Mismatch in number of columns.")
            continue

        if "University of Wisconsin - Madison" not in line[1]:
            continue

        name = ''.join([i for i in line[0] if not i.isdigit()]).strip()
        website_link = line[2]
        scholar_id = line[3]

        if scholar_id not in faculty_on_csrankings:
            faculty_on_csrankings[scholar_id] = {
                "name": [name],
                "website": website_link,
            }
        else:
            faculty_on_csrankings[scholar_id]['name'].append(name)

    print(len(faculty_on_website))
    print(len(faculty_on_csrankings))

    for faculty in faculty_on_website:
        if not any(ratio(faculty, faculty_name) > 0.7 for scholar_id in faculty_on_csrankings for faculty_name in faculty_on_csrankings[scholar_id]['name']):
            print(f"Missing {faculty} on CSrankings.")
    
    print()
    
    for faculty in faculty_on_csrankings:
        if not any(ratio(faculty_name, website_faculty) > 0.7 for faculty_name in faculty_on_csrankings[faculty]['name'] for website_faculty in faculty_on_website):
            print(f"Extra {faculty_on_csrankings[faculty]['name']} on CSRankings.")

if __name__ == "__main__":
    main()
