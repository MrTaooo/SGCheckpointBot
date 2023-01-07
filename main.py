import telebot
import requests
from datetime import datetime

bot = telebot.TeleBot('5895899031:AAGMv_wzv7pKLJqacQYUiS27rSPzO7QumNI')

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Good day! How can I assist you?\n\n/checkpointsCamera for live snapshots of Woodlands/Tuas Checkpoint\n\n/roadworks for live updates on SG road incidents")


@bot.message_handler(commands=['checkpointsCamera'])
def checkpointsCamera(message):
    headers = {"AccountKey": "p34dHcCaTsmmlz4DPlzUGw=="}
    response = requests.get(
        'http://datamall2.mytransport.sg/ltaodataservice/Traffic-Imagesv2', headers=headers)
    data = response.json()['value']
    imageArr = []
    locationArr = ['View from Woodlands Causeway (Towards Johor)', 'View from Woodlands Checkpoint (Towards BKE)', 'View from Second Link at Tuas', 'View from Tuas Checkpoint']
    
    for x in data:
        CID = x["CameraID"]
        IL = x['ImageLink']

        # View from Woodlands Causeway (Towards Johor)
        if CID == "4703":
            image = requests.get(IL).content
            # Send the response back to the user
            # bot.send_message(message.chat.id,"test123")
            imageArr.append(image)

        # View from Woodlands Checkpoint (Towards BKE)
        if CID == "4713":
            image = requests.get(IL).content
            # Send the response back to the user
            # bot.send_message(message.chat.id,"test123")
            imageArr.append(image)

        # View from Second Link at Tuas
        if CID == "2701":
            image = requests.get(IL).content
            # Send the response back to the user
            # bot.send_message(message.chat.id,"test123")
            imageArr.append(image)

        # View from Tuas Checkpoint
        if CID == "2702":
            image = requests.get(IL).content
            # Send the response back to the user
            # bot.send_message(message.chat.id,"test123")
            imageArr.append(image)
    sendImage(imageArr, locationArr, message)
def sendImage(sendingArr, sendingLocation, message):
    # datetime object containing current date and time
    now = datetime.now()

    # dd/mm/YY H:M:S
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")

    for x in range(len(sendingArr)):
        eachImage = sendingArr[x]
        eachCaption = sendingLocation[x]
        bot.send_photo(message.chat.id, photo=eachImage, caption=f"{dt_string}\n\n{eachCaption}")
        

    # for x in data:
    #     CID = x["CameraID"]
    #     IL = x['ImageLink']
    #     if CID == "4703":
    #         image = requests.get(IL).content
    #         # Send the response back to the user
    #         # bot.send_message(message.chat.id,"test123")
    #         bot.send_photo(message.chat.id, photo=image,
    #                        caption="View from Tuas Checkpoint")

@bot.message_handler(commands=['roadworks'])
def roadworks(message):
    headers = {"AccountKey": "p34dHcCaTsmmlz4DPlzUGw=="}
    response = requests.get('http://datamall2.mytransport.sg/ltaodataservice/TrafficIncidents', headers=headers)
    data = response.json()['value']

    dataTypeArr = []
    messageArr = []

    for eachData in data:
        dataType = eachData['Type']
        roadMessage = eachData['Message']
        if("(towards Tuas)" in roadMessage or "(towards Woodlands)" in roadMessage):
            dataTypeArr.append(dataType)
            messageArr.append(roadMessage)

    sendRoadwork(dataTypeArr, messageArr, message)
def sendRoadwork(dataTypeArr, messageArr, message):
    if(len(dataTypeArr)>0):
        for x in range(len(dataTypeArr)):
            dataType = dataTypeArr[x]
            roadMessage = messageArr[x]
            bot.send_message(message.chat.id,f"Type: {dataType}\n{roadMessage}\n\n")
    else:
        bot.send_message(message.chat.id,"It seems like there's no road incident")

bot.polling()
