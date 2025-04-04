import re
from tkinter import *

import bs4
import requests
from Levenshtein import ratio
from functools import partial
import pandas as pd


def main() -> None:
    url = "https://www.cs.wisc.edu/people/faculty-2/"
    res = requests.get(url, timeout=5)
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
        "https://raw.githubusercontent.com/emeryberger/CSrankings/gh-pages/csrankings.csv",
        timeout=5,
    )

    res.raise_for_status()

    # read the CSV file from the GitHub URL
    csv_data = res.text.splitlines()
    csv_lines = [line.split(",") for line in csv_data]
    csv_header = csv_lines[0]
    csv_rows = csv_lines[1:]

    faculty_on_csrankings = {}

    for line in csv_rows:
        if len(line) != len(csv_header):
            # print("Mismatch in number of columns.")
            continue

        if "University of Wisconsin - Madison" not in line[1]:
            continue

        name = "".join([i for i in line[0] if not i.isdigit()]).strip()
        website_link = line[2]
        scholar_id = line[3]

        if scholar_id not in faculty_on_csrankings:
            faculty_on_csrankings[scholar_id] = {
                "name": [name],
                "website": website_link,
            }
        else:
            faculty_on_csrankings[scholar_id]["name"].append(name)

    # print(len(faculty_on_website))
    # print(len(faculty_on_csrankings))

    # for faculty in faculty_on_website:
    #     if not any(
    #         ratio(faculty, faculty_name) > 0.7
    #         for scholar_id in faculty_on_csrankings
    #         for faculty_name in faculty_on_csrankings[scholar_id]["name"]
    #     ):
    # print(f"Missing {faculty} on CSrankings.")

    # print()

    # for faculty in faculty_on_csrankings:
    #     if not any(
    #         ratio(faculty_name, website_faculty) > 0.7
    #         for faculty_name in faculty_on_csrankings[faculty]["name"]
    #         for website_faculty in faculty_on_website
    #     ):
    # print(f"Extra {faculty_on_csrankings[faculty]['name']} on CSRankings.")

    ####################

    def on_frame_configure(canvas: Canvas) -> None:
        """Reset the scroll region to encompass the inner frame."""
        canvas.configure(scrollregion=canvas.bbox("all"))

    window = Tk()
    canvas = Canvas(window)
    main_frame = Frame(window)
    scrollbar = Scrollbar(window, orient="vertical", command=canvas.yview)
    canvas.configure(yscrollcommand=scrollbar.set)

    scrollbar.pack(side=RIGHT, fill="y")
    canvas.pack(side=LEFT, fill=BOTH, expand=True)
    canvas.create_window((0, 0), window=main_frame, anchor="nw")

    main_frame.bind(
        "<Configure>",
        lambda _, canvas=canvas: on_frame_configure(canvas),
    )

    missing_names = [""] * len(faculty_on_website)
    missing_websites = [""] * len(faculty_on_website)
    missing_scholar_ids = [""] * len(faculty_on_website)
    add_checkbuttons = [BooleanVar() for _ in range(len(faculty_on_website))]

    def on_checkbutton_click(idx) -> None:
        website = missing_websites[idx].get()
        scholar_id = missing_scholar_ids[idx].get()

        if not (add_checkbuttons[idx].get() and website and scholar_id):
            add_checkbuttons[idx].set(False)

    window.title("CSRankings Faculty Checker")
    window.geometry("1130x600")

    missing_label = Label(
        main_frame,
        text="Missing Faculty on CSRankings",
        width=120,
        font=("Arial", 12),
        borderwidth=1,
        relief="solid",
        pady=20,
    )
    missing_label = Label(
        main_frame,
        text="Missing Faculty on CSRankings",
        width=123,
        font=("Arial", 12),
        borderwidth=1,
        relief="solid",
        pady=20,
    )
    missing_label.grid(row=0, column=0, columnspan=4)

    name_header = Label(
        main_frame,
        text="Name",
        width=30,
        borderwidth=1,
        relief="solid",
        font=("Arial, 10"),
        pady=5,
    )
    website_header = Label(
        main_frame,
        text="Website",
        width=50,
        borderwidth=1,
        relief="solid",
        font=("Arial, 10"),
        pady=5,
    )
    scholar_id_header = Label(
        main_frame,
        text="Google Scholar ID",
        width=20,
        borderwidth=1,
        relief="solid",
        font=("Arial, 10"),
        pady=5,
    )
    add_header = Label(
        main_frame,
        text="Add to CSRankings",
        width=20,
        borderwidth=1,
        relief="solid",
        font=("Arial, 10"),
        pady=5,
    )

    name_header.grid(row=1, column=0)
    website_header.grid(row=1, column=1)
    scholar_id_header.grid(row=1, column=2)
    add_header.grid(row=1, column=3)

    for i, faculty in enumerate(faculty_on_website, start=2):
        if not any(
            ratio(faculty, faculty_name) > 0.7
            for scholar_id in faculty_on_csrankings
            for faculty_name in faculty_on_csrankings[scholar_id]["name"]
        ):
            missing_names[i - 2] = Label(
                main_frame,
                text=faculty,
                width=30,
                borderwidth=1,
                relief="solid",
                font=("Arial, 10"),
                pady=5,
            )
            missing_websites[i - 2] = Entry(
                main_frame,
                width=50,
                font=("Arial, 10"),
                borderwidth=1,
                relief="solid",
                justify="center",
            )
            missing_scholar_ids[i - 2] = Entry(
                main_frame,
                width=20,
                font=("Arial, 10"),
                borderwidth=1,
                relief="solid",
                justify="center",
            )
            checkbutton_label = Label(
                main_frame,
                width=20,
                borderwidth=1,
                relief="solid",
                font=("Arial, 10"),
                pady=5,
            )
            checkbutton_label.pack_propagate(flag=False)
            add_checkbutton = Checkbutton(checkbutton_label, text="", variable=add_checkbuttons[i - 2], command=partial(on_checkbutton_click, i - 2))
            add_checkbutton.pack()

            missing_names[i - 2].grid(row=i, column=0)
            missing_websites[i - 2].grid(row=i, column=1)
            missing_scholar_ids[i - 2].grid(row=i, column=2)
            checkbutton_label.grid(row=i, column=3)

    # extra_label = Label(
    #     main_frame,
    #     text="Extra Faculty on CSRankings",
    #     width=123,
    #     font=("Arial", 12),
    #     borderwidth=1,
    #     relief="solid",
    #     pady=20,
    # )
    # extra_label.grid(row=i + 1, column=0, columnspan=4)

    # extra_name_header = Label(
    #     main_frame,
    #     text="Name",
    #     width=30,
    #     borderwidth=1,
    #     relief="solid",
    #     font=("Arial, 10"),
    #     pady=5,
    # )
    # # extra_website_header = Label(
    # #     main_frame,
    # #     text="Website",
    # #     width=50,
    # #     borderwidth=1,
    # #     relief="solid",
    # #     font=("Arial, 10"),
    # #     pady=5,
    # # )
    # extra_add_header = Label(
    #     main_frame,
    #     text="Remove from CSRankings",
    #     width=20,
    #     borderwidth=1,
    #     relief="solid",
    #     font=("Arial, 10"),
    #     pady=5,
    # )

    # extra_name_header.grid(row=i + 2, column=0)
    # # extra_website_header.grid(row=i+2, column=1)
    # # extra_add_header.grid(row=i+2, column=2)
    # extra_add_header.grid(row=i + 2, column=1, sticky="w")

    # for j, faculty in enumerate(faculty_on_csrankings, start=i + 3):
    #     if not any(
    #         ratio(faculty_name, website_faculty) > 0.7
    #         for faculty_name in faculty_on_csrankings[faculty]["name"]
    #         for website_faculty in faculty_on_website
    #     ):
    #         extra_name = Label(
    #             main_frame,
    #             text=faculty_on_csrankings[faculty]["name"],
    #             width=30,
    #             borderwidth=1,
    #             relief="solid",
    #             font=("Arial, 10"),
    #             pady=5,
    #         )
    #         # extra_website = Label(
    #         #     main_frame,
    #         #     text=faculty_on_csrankings[faculty]["website"],
    #         #     width=50,
    #         #     font=("Arial, 10"),
    #         #     borderwidth=1,
    #         #     relief="solid",
    #         #     pady=5,
    #         # )
    #         extra_checkbutton_label = Label(
    #             main_frame,
    #             width=20,
    #             borderwidth=1,
    #             relief="solid",
    #             font=("Arial, 10"),
    #             pady=5,
    #         )
    #         extra_checkbutton_label.pack_propagate(flag=False)
    #         extra_add_checkbutton = Checkbutton(extra_checkbutton_label, text="")
    #         extra_add_checkbutton.pack()

    #         extra_name.grid(row=j, column=0)
    #         # extra_website.grid(row=j, column=1)
    #         # extra_checkbutton_label.grid(row=j, column=2)
    #         extra_checkbutton_label.grid(row=j, column=1, sticky="w")

    def on_done() -> None:
        for i in "abcdefghijklmnopqrstuvwxyz":
            file_name = f"CSrankings/csrankings-{i}.csv"
            df = pd.read_csv(file_name, encoding="utf-8")

            for idx, var in enumerate(add_checkbuttons):
                if not var.get():
                    continue

                name = missing_names[idx].cget("text")
                website = missing_websites[idx].get()
                scholar_id = missing_scholar_ids[idx].get()

                if name[0].lower() != i:
                    continue

                df.loc[len(df)] = {
                            "name": name,
                            "affiliation": "University of Wisconsin - Madison",
                            "homepage": website,
                            "scholarid": scholar_id
                        }

            df = df.sort_values(by=["name", "affiliation", "homepage", "scholarid"])
            df.to_csv(file_name, index=False, lineterminator='\r\n')

        window.destroy()

    submit_button_label = Label(
        main_frame,
        width=123,
        font=("Arial", 12),
        borderwidth=1,
        relief="solid",
        pady=20,
    )
    submit_button = Button(
        submit_button_label,
        text="Done",
        command=on_done,
        width=20,
        font=("Arial", 12),
        borderwidth=1,
        relief="solid",
        pady=5,
    )
    submit_button_label.pack_propagate(flag=False)
    submit_button.pack(anchor="center", expand=True)
    submit_button_label.grid(row=i + 1, column=0, columnspan=4)

    window.mainloop()


if __name__ == "__main__":
    main()

# CSrankings GitHub needs name similar to dblp, name is derived from cs faculty website here