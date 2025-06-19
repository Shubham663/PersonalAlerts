# PersonalAlerts
Provides alerts on telegram for the cricket updates taking place on a website.

# Instructions for running the application:
1. Check for the dependencies listed in Resources needed and download any if not already there
2. Making a bot.
  2.1. Go to telegram and search for BotFather. Start conversation.
  2.2. Do "/newbot"
  2.3. Provide with name and username(unique) for the bot. Save the username as you will require that for later interacting with bot.
  2.4. Save the access token API that you get on bot creation and save it as API_KEY in an ".env" file in your project's root.
3. run the application using python alerts.py
4. interact with bot using /start, at which it will start getting updates from https://www.espncricinfo.com/ for the first live match that it encounters.
