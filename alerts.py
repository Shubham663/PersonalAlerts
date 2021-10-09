from decouple import config
from bs4 import BeautifulSoup
import requests
from time import sleep
from telegram import Update
from telegram.ext import Updater,CommandHandler,CallbackContext

# The URL from which the match's information is fetched
URL='https://www.espncricinfo.com/'
API_KEY = config('API_KEY')


def fetchAndSend(chatId,context) -> None:
  context.bot.send_message(chatId,text='Trying to fetch data from the cricket website that you love ' + URL)
  cricInfo=requests.get(URL)
  cricInfoBetter=BeautifulSoup(cricInfo.content,"html.parser")

  # matches: all the matches on home page
  matches=cricInfoBetter.find_all("div",class_="scorecard-container")
  # print(matches)

  # This for loop searches for the first "live" match
  for match in matches:
    flag=0
    match1=match

    # isLive: Fetches the match status 
    isLive = match.find_all("div",class_="status status-hindi red")
    for live in isLive:
      # print(live.span.text)
      if(live.span.text=="live"):
        flag=1
        print('live')
        break
    if flag==1:
      break
    y=1

  #for loop has ended therefor either match1 is live or not match is active  
  # print(match1)

  #going to the webpage for the match which we have ectracted as match1
  nextURL=URL[:-1]+match1.select_one('.match-info-link-HSB')['href']
  cricInfo=requests.get(nextURL)
  cricInfoBetter=BeautifulSoup(cricInfo.content,"html.parser")

  # Fetching the detail which teams are taking part in match
  names=cricInfoBetter.find_all("div",class_="match-header-info match-info-MATCH")
  name=names[0]
  context.bot.send_message(chatId,text='Match Details: '+name.text)
  print(nextURL)

  # Stores the most recent update from previous iteration of the while loop starting 5 lines below 
  prev=''
  count=0

  # This while loop will look for updates on the website for the match
  while True:
    newarray=[]
    newarray2=[]
    newarray3=[]
    count=count+1
    cricInfo=requests.get(nextURL)
    cricInfoBetter=BeautifulSoup(cricInfo.content,"html.parser")
    overs=cricInfoBetter.find_all("span",class_="match-comment-over")
    infos=cricInfoBetter.find_all("div",class_="match-comment-short-text")
    scoreDivs=cricInfoBetter.find_all("div",class_="match-info match-info-MATCH match-info-MATCH-full-width")
    # print(scoreDivs)
    scoreDiv=scoreDivs[0]
    scoreSpans=scoreDiv.find_all("span",class_="score")
    infoSpans =scoreDiv.find_all("span",class_="score-info")
    i=0
    while i<len(infoSpans) and infoSpans[i].text=='':
      i=i+1

    # checks if no match is actice, and exits if so
    if i >= len(scoreSpans):
      break
    scoreSpan=scoreSpans[i]
    score=scoreSpan.text
    # nexprev=infos[0].text
    print(len(infos))

    # Putting latest info available on web in newarray2 
    for info in infos:
      newarray2.append('Summary:' + str(info.text))
    
    #Putting latest overs info available on web in newarray3
    for over in overs:
      newarray3.append(', Overs: '+str(over.text))

    #Getting elementwise addition between summary and overs info
    for m,n in zip(newarray2,newarray3):
      newarray.append(m+n)
    print(len(overs))
    # newarray= np.core.defchararray.add(newarray2, newarray)  
    # above line might have been useful if numpy arrays were there
    if(len(newarray)==0):
      break
    nexprev=newarray[0]
    if(count==1):
      prev=nexprev
      context.bot.send_message(chatId,text=nexprev+',Score: '+str(score))
      continue
    # print(nexprev)

    #getting only the new elements and removing the ones iterated over in previous loops
    val = newarray.index(prev)
    newarray=newarray[0:val]
    newarray.reverse()

    # publishing the latest info to user through telegram bot
    for info in newarray:
      curr=info
      context.bot.send_message(chatId,text=curr+',Score: '+str(score))
      #appending score for better updates to user
    
    prev=nexprev
    sleep(7)
  # context.bot.send_message(chatId,text=str(len(matches)))


# the function that is called when someone starts interacting with bot
def start(update: Update, context: CallbackContext) -> None:
    # """Sends explanation on how to use the bot."""
    update.message.reply_text('Starting scores for the match. Please wait a bit for the updtaes')
    fetchAndSend(update.message.chat_id,context)
    context.bot.send_message(update.message.chat_id,text="No match is currently live, thanks for"+ 
    " making use of the bot. Please use /start again if you want to check for live scores")
    


# The first fucntion that is called, that is effectively from where the execution starts
def main():
  updater = Updater(token=API_KEY)
  # print(API_KEY)
    # Get the dispatcher to register handlers
  dispatcher = updater.dispatcher

    # on start command - answer in Telegram
  dispatcher.add_handler(CommandHandler("start", start))
    # Start the Bot
  updater.start_polling()

# Calling the main function
if __name__=="__main__":
  main()
