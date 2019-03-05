import vk_api
import time
import json
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import os

def getUsers():
    fd = open("moscow.json", 'r')
    users = json.load(fd)
    fd.close()
    return(users)
def findLogin(login, users):
    k = 0
    for i in users:
        if login in i.get("users"):
            allGuys = i.get("before") + i.get("after") + len(i.get("users"))
            before = str(round(100 * (i.get("before")) / allGuys , 2))
            after = str(round(100 * i.get("after")/ allGuys, 2))
            howMuchUsers = str(round(100 * len(i.get("users")) / allGuys, 2))
            howMuchUsers =  howMuchUsers + "%"
            answer = "%s: lvl %s\n"%(login, str(round(i.get("level"), 2)))
            place = str(k + 1) + '/' + str(len(users))
            answer +="place: %s with %s (%s/%s) users\n" %(place, howMuchUsers, len(i.get("users")), allGuys)
            answer += "higher than %s (%s/%s) users\nlower than %s (%s/%s) users"%(after + "%",i.get("after"), allGuys, before + "%", i.get("before"), allGuys)
            if k == 0:
                answer = "THE BOSS OF THE GYM!\n" + answer + "\nTHE BOSS OF THE GYM!"
            return(answer)
        k+=1
    return("Проверь правильность написания логина")
def getTop(users):
    users = users[0:15]
    formattedUsers = []
    temp = ""
    for k in range(0, len(users)):
        placeGuys = ""
        for i in users[k].get('users'):
            placeGuys += "https://profile.intra.42.fr/users/" + i + "\n"
        formattedUsers.append("top-%s c lvl - %s:\n%s" %(str(k + 1) , str(round(users[k].get('level'), 2)), placeGuys))
    temp = temp.join(formattedUsers)
    return (temp)
token = os.environ['TOKEN']
vk_session = vk_api.VkApi(token=token)
vk = vk_session.get_api()
longpoll = VkBotLongPoll(vk_session, group_id="179224993")
for event in longpoll.listen():
    if event.type == VkBotEventType.MESSAGE_NEW and event.obj.text and event.obj.text.split()[0].lower() == "!рейтинг":
        print(event.obj.user_id)
        if (len(event.obj.text.split()) >= 2):
            login = event.obj.text.split()[1].lower()
            users = getUsers()
            vk.messages.send(user_id = event.obj.from_id, message=findLogin(login, users), random_id = "0")
        else:
            vk.messages.send(user_id = event.obj.from_id, message=getTop(users), random_id = "0")
