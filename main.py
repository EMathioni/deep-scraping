import csv

from bs4 import BeautifulSoup as bsp
import requests

from constants import contants as cts

### DISCLAIMER: ###
### Script developed for study, help and knowledge purposes. ###
### Any use that violates these purposes will be entirely YOUR responsibility. ###
### Use it wisely. ###

print("Welcome to Deep Web Scraping (DWS) v1")
print("Developed by: https://github.com/EMathioni\n")


def start_scraping():
    try:
        query = str(input("Type your search: ")).replace(" ", "+")
        date = str(input("Type amount days to filter: ")).strip()
        url_search = scraping_opt(query, date)
        print(url_search)
        print('Searching results...')
        request_url = requests.get(url_search)
        soup = bsp(request_url.text, 'html.parser')
        no_result = soup.find('p', id='noResults')
        if no_result:
            print("\nNothing found to '{}'".format(query))
            retry()
        else:
            all_results = soup.find('ol', class_='searchResults').find_all('li', class_='result')
            all_results_list = []
            for result in all_results:
                names = result.contents[1]
                description = result.contents[3]
                links = result.contents[5]
                date_stamp = result.contents[7]
                if names.text.strip() == "" and description.text.strip() == 'No description provided':
                    continue
                elif names.text.strip() == "":
                    names = "No title"
                    data = {
                        'Title': names,
                        'Description': description.text.strip(),
                        'Link': 'http://' + links.text.strip(),
                        'Since': date_stamp.text.strip()
                    }
                    all_results_list.append(data)
                elif description.text.strip() == 'No description provided':
                    description = "No description found"
                    data = {
                        'Title': names.text.strip(),
                        'Description': description,
                        'Link': 'http://' + links.text.strip(),
                        'Since': date_stamp.text.strip()
                    }
                    all_results_list.append(data)
                else:
                    data = {
                        'Title': names.text.strip(),
                        'Description': description.text.strip(),
                        'Link': 'http://' + links.text.strip(),
                        'Since': date_stamp.text.strip()
                    }
                    all_results_list.append(data)
            return save_to_csv(all_results_list, query)
    except Exception as e:
        print(e)
        retry()


def retry():
    print("\nDo you want to search again?\nY - Yes\nN - No")
    user_input = choice_option()
    if user_input is True:
        start_scraping()
    elif user_input is False:
        print("\nThank you so much for using our service!")
        print("Developed by: https://github.com/EMathioni\n")
        exit()
    else:
        print("Invalid option.")
        retry()


def choice_option():
    option = str(input('#> ')).lower().strip()
    if option == 'y':
        return True
    if option == 'n':
        return False
    return None


def save_to_csv(results, query):
    print("Saving results...")
    file = open(f'Deep Web Results to [{query.title().replace("+", " ")}].csv', 'w', encoding="utf-8")
    writer = csv.writer(file)
    writer.writerow(['Title', 'Description', 'Link', 'Since'])

    for result in results:
        writer.writerow(list(result.values()))
    file.close()
    print(f"File saved! ({file.name})")
    retry()


def scraping_opt(query, date):
    if date is None:
        print('If you leave it blank, the result will be all the time. '
              'Do you sure wanna proceed? y/n')
        option = choice_option()
        if option is True:
            date = 'all'
        elif option is False:
            date = str(input("Type amount days to filter: ")).strip()
            if date.isdigit():
                return f"{cts.c['uri']}?q={query}&d={date}"
            else:
                print("Invalid option, no time filter added...")
                return f"{cts.c['uri']}?q={query}"
    return f"{cts.c['uri']}?q={query}&d={date} "


start_scraping()
