import requests
import bs4
import os
import json
import time

if __name__ == "__main__":
    url = "https://mox.polimi.it/people/"
    save_folder = "../public/assets/mox_people"

    os.makedirs(save_folder, exist_ok=True)
    os.makedirs(f"{save_folder}/imgs", exist_ok=True)

    response = requests.get(url)
    soup = bs4.BeautifulSoup(response.content, "html.parser")
    people = soup.find_all("div", class_="column")

    people_json = []
    for person in people:
        img = person.find("img")["src"]
        img_ext = img.split(".")[-1]
        # image is available
        if img.startswith("https://www.mate.polimi.it/servizi/webspace/img/"):
            print("requesting:", img)
            person_name = person.find("h2").text.strip()
            person_position = person.find("h3").text.strip()
            img = requests.get(img)
            # backoff to avoid getting blocked
            time.sleep(1)
            img_path = f"{save_folder}/imgs/{person_name}.{img_ext}"
            with open(img_path, "wb") as f:
                f.write(img.content)

            people_json.append({
                "name": person_name,
                "position": person_position,
                "img": img_path
            })

    with open(f"{save_folder}/people_raw.json", "w") as f:
        json.dump(people_json, f, indent=4)