import requests
from bs4 import BeautifulSoup
import inquirer

def fetch_songs():
    poll_url = "https://babelsberg03.de/media/karli-charts/"

    poll_response = requests.get(poll_url)
    poll_response.raise_for_status()
    
    soup = BeautifulSoup(poll_response.text, 'html.parser')
    song_elements = soup.select("ul.poll_ans_ul_cls li.poll_ans_li_cls")
    
    songs = []
    for element in song_elements:
        input_tag = element.find('input')
        if input_tag:
            song_id = input_tag.get('value')
            song_name = input_tag.find_next_sibling(string=True).strip()
            songs.append((song_name, song_id))

    return songs


def validate_no_votes_input(answers, current):
    try:
        int(current)
        return True
    except ValueError:
        return False


def main():
    print("Suche Songs...")
    songs = fetch_songs()

    questions = [
            inquirer.List('song',
                          message="Welchen Song möchtest du in der Halbzeitpause des nächsten Heimspiels hören?",
                          choices=songs,
                          carousel=True),
            inquirer.Text('number_of_votes', 
                          message="Wie viele Stimmen möchtest du abgeben?", 
                          validate=validate_no_votes_input)
            ]

    answers = inquirer.prompt(questions)

    url = "https://babelsberg03.de/?pollone=poll-submitted"
    headers = {
            "Content-Length": "8", 
            "Content-Type": "application/x-www-form-urlencoded",
            "Referer": "https://babelsberg03.de/media/karli-charts/"
            }
    data = {
            "ans": answers['song']
            }
    
    print("Stimmen werden abgegeben...")

    for _ in range(int(answers['number_of_votes'])):
        response = requests.post(url, headers=headers, data=data)

    print(f"{answers['number_of_votes']} Stimmen erfolgreich abgegeben.")


if __name__ == "__main__":
    main()
