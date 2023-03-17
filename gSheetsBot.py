from dotenv import load_dotenv
import hikari
import lightbulb
import os

#google imports
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

load_dotenv()


bot = lightbulb.BotApp(token=f"{os.getenv('bot_key')}")

creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
if os.path.exists('token.json'):
    creds = Credentials.from_authorized_user_file('token.json', SCOPES)
# If there are no (valid) credentials available, let the user log in.
if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file(
            'credentials.json', SCOPES)
        creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open('token.json', 'w') as token:
        token.write(creds.to_json())

service = build('sheets', 'v4', credentials=creds)
sheet = service.spreadsheets()

#initial test command
@bot.command
@lightbulb.option('sheetname', 'Name of the sheet you are accessing.')
@lightbulb.command('sheettest', 'Get stuff from specified sheet')
@lightbulb.implements(lightbulb.SlashCommand)
async def readSheet(ctx):
    result = sheet.values().get(spreadsheetId='1pisIsaFXR4OOYbn5q5yhxeLdqTLPtHou8-jD8M2POmw', range=f'{ctx.options.sheetname}').execute()
    print(result)
    values = result.get('values')
    for value in values:
        if 'london' in value:
            print(value)
    await ctx.respond('Testing')




bot.run()