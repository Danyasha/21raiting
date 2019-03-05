import requests
import json
from time import sleep
import Intra42
import os

SECRET = os.environ['SECRET']
UID = os.environ['not_UID']

def main():
    IntraPy = Intra42.Intra42(UID, SECRET)
    raiting = []
    LastPage = IntraPy.cursus_users(getPage='last',filterBy = "campus_id", filterVal = "17")
    for i in range(0, LastPage + 1):
        users = IntraPy.cursus_users(page=str(i), filterBy = "campus_id", filterVal = "17")
        print(i)
        for user in users:
            if user.get("end_at"):
                raiting.append({'login':user.get('user').get('login'), 'level':round(user.get('level'), 2)})
    fd = open("moscow.json", "w")
    raiting = IntraPy.sortUsersByRaiting(raiting, addBeforeAfter = True)
    json.dump(raiting, fd, ensure_ascii=False, sort_keys=True, indent=4)
    fd.close()
    print("updating done")
if __name__ == "__main__":
    while(1):
        time = 25
        print("Wait for ", time)
        sleep(time)
        main()