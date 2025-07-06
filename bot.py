import re
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor

API_TOKEN = "7971051467:AAEgFdgmEcmfYmIWfSqQ_sCv0MNNzcrl49Y"  # Replace with your bot token

bot = Bot(token=API_TOKEN, parse_mode="HTML")
dp = Dispatcher(bot)

# Clean URL for /f type links (standard cleaning)
def clean_url(url):
    url = url.strip()
    
    # Ensure the url starts with https://
    if not url.startswith("http"):
        url = "https://" + url
    url = url.replace("http://", "https://")
    
    # Remove query parameters and fragments
    url = re.sub(r"(\?|\&)[^=]+=[^&]*", "", url)  # Remove query parameters
    url = re.sub(r"#.*", "", url)  # Remove fragments
    url = re.sub(r"//+", "/", url)  # Fix redundant slashes

    return url

# Clean text URL for /ftxt type links (keep query params intact but remove unnecessary ones)
def clean_text_url(url):
    url = url.strip()
    
    # Ensure the url starts with https://
    if not url.startswith("http"):
        url = "https://" + url
    url = url.replace("http://", "https://")
    
    # Clean query params but keep the "text" parameter for example
    url = re.sub(r"(\?|\&)(?!text=)[^=]+=[^&]*", "", url)  # Remove all params except "text"
    url = re.sub(r"#.*", "", url)  # Remove fragments
    url = re.sub(r"//+", "/", url)  # Fix redundant slashes
    
    return url

# Command handler for /f (standard URL cleaning)
@dp.message_handler(commands=['f'])
async def handle_clean_url(message: types.Message):
    # Extract URL from the message text
    links = re.findall(r'(https?://[^\s]+)', message.text)
    if links:
        cleaned_links = [clean_url(link) for link in links]
        reply_text = "\n".join(cleaned_links)
        await message.reply(f"Cleaned Links:\n{reply_text}")
    else:
        await message.reply("No valid URLs found!")

# Command handler for /ftxt (clean text URLs but keep some parameters intact)
@dp.message_handler(commands=['ftxt'])
async def handle_clean_text_url(message: types.Message):
    # Extract URL from the message text
    links = re.findall(r'(https?://[^\s]+)', message.text)
    if links:
        cleaned_links = [clean_text_url(link) for link in links]
        reply_text = "\n".join(cleaned_links)
        await message.reply(f"Cleaned Text Links:\n{reply_text}")
    else:
        await message.reply("No valid URLs found!")

if __name__ == "__main__":
    print("Bot started!")
    executor.start_polling(dp, skip_updates=True)
