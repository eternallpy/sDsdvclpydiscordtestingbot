import discord
import os
from discord.ext import tasks, commands
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from itertools import cycle
from stayin_alive import keep_alive

intent = discord.Intents.default()
intent.members = True
intent.message_content = True

client = discord.Client(intents=intent)


@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))
  print("hello white")
  if not autoUpdateRate.is_running():
    autoUpdateRate.start()
 


@client.event
async def on_message(message):
  if message.author == client.user:
    return
  if message.content == 'hello':
    await message.channel.send('Hello!')

  if message.content == 'uprate':
    updateRate()
    # Because discord itself does not support tab or set width, so spaces were used in this case.
    await message.channel.send("JPY:            " + yen +
                               "\n---------------------\n" +
                               "USD:           " + usd +
                               "\n---------------------\n" + "RMB:          " +
                               rmb + "\n---------------------\n" +
                               "GBP:           " + gbp +
                               "\n---------------------\n" + "EURO:        " +
                               euro + "\n---------------------\n\n" +
                               updatetime)

  if message.content == 'rate':
    await message.channel.send("JPY:            " + yen +
                               "\n---------------------\n" +
                               "USD:           " + usd +
                               "\n---------------------\n" + "RMB:          " +
                               rmb + "\n---------------------\n" +
                               "GBP:           " + gbp +
                               "\n---------------------\n" + "EURO:        " +
                               euro + "\n---------------------\n\n" +
                               updatetime)

  if message.content == 'yen':
    await message.channel.send(yen + '\n\n' + updatetime)
  if message.content == 'rmb':
    await message.channel.send(rmb + '\n\n' + updatetime)
  if message.content == 'usd':
    await message.channel.send(usd + '\n\n' + updatetime)
  if message.content == 'euro':
    await message.channel.send(euro + '\n\n' + updatetime)
  if message.content == 'gbp':
    await message.channel.send(gbp + '\n\n' + updatetime)

  if message.content == 'help':
    await message.channel.send(
      "uprate: Manually update all exchange rate and send out the rate list.\n-\nrate: Send out the exchange rate list\n-\nyen/usd/rmb/gbp/euro: Send out corresponding currency exchange rate"
    )


@tasks.loop(minutes=20)
async def autoUpdateRate():
  updateRate()
  global status
  status = cycle(["JPY: " + yen, "USD: " + usd, "RMB: " + rmb])
  if not changeStatus.is_running():
    changeStatus.start()


@tasks.loop(seconds=5.0)
async def changeStatus():
  await client.change_presence(activity=discord.Activity(
    type=discord.ActivityType.watching, name=next(status)))


def updateRate():
  print("Updating")
  global yen, rmb, usd, euro, gbp
  global updatetime
  chrome_options = Options()
  chrome_options.add_argument('--headless')
  chrome_options.add_argument('--disable-setuid-sandbox')
  chrome_options.add_argument('--disable-extensions')
  chrome_options.add_argument('--disable-gpu')
  chrome_options.add_argument('--no-sandbox')
  chrome_options.add_argument('--disable-dev-shm-usage')

  driver = webdriver.Chrome(options=chrome_options)
  driver.get(
    "https://www.hsbc.com.hk/investments/products/foreign-exchange/currency-rate/"
  )
  yen = driver.find_element(
    By.XPATH,
    "/html/body/div[3]/div[2]/div[2]/div[3]/form/div[1]/div/table[2]/tbody/tr[31]/td"
  ).get_attribute("innerHTML")
  rmb = driver.find_element(
    By.XPATH,
    "/html/body/div[3]/div[2]/div[2]/div[3]/form/div[1]/div/table[2]/tbody/tr[52]/td"
  ).get_attribute("innerHTML")
  usd = driver.find_element(
    By.XPATH,
    "/html/body/div[3]/div[2]/div[2]/div[3]/form/div[1]/div/table[2]/tbody/tr[3]/td"
  ).get_attribute("innerHTML")
  gbp = driver.find_element(
    By.XPATH,
    "/html/body/div[3]/div[2]/div[2]/div[3]/form/div[1]/div/table[2]/tbody/tr[45]/td"
  ).get_attribute("innerHTML")
  euro = driver.find_element(
    By.XPATH,
    "/html/body/div[3]/div[2]/div[2]/div[3]/form/div[1]/div/table[2]/tbody/tr[24]/td"
  ).get_attribute("innerHTML")
  updatetime = driver.find_element(
    By.XPATH,
    "/html/body/div[3]/div[2]/div[2]/div[3]/form/div[1]/div/table[2]/tbody/tr[6]/td"
  ).get_attribute("innerHTML")
  updatetime = "Last Update: " + updatetime[5:-53]
  print("Update - Finished")


keep_alive()
client.run(os.getenv('TOKEN'))
