import base64
from io import BytesIO
from PIL import Image
import telebot
from config import API_TOKEN
from logic import Text2ImageAPI
import time
import os


bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=['start', 'help'])
def start_message(message):
    bot.send_message(message.chat.id, "Привет! Отправьте мне описание изображения, и я сгенерирую его.")

@bot.message_handler(content_types=['text'])
def handle_text(message):
    api = Text2ImageAPI('https://api-key.fusionbrain.ai/', 'YOUR_API_KEY', 'YOUR_SECRET_KEY')
    
    
    gen_msg = bot.send_message(message.chat.id, "Генерирую картинку...")
    bot.send_chat_action(message.chat.id, 'typing')  
    time.sleep(2)  
    
    decoded_data = api.get_image(message.text)
    image = Image.open(BytesIO(decoded_data))
    image_path = "generated_image.jpg"
    image.save(image_path)
    
 
    bot.delete_message(message.chat.id, gen_msg.message_id)
    
    with open(image_path, "rb") as img_file:
        bot.send_photo(message.chat.id, img_file)
    
    
    os.remove(image_path)

if __name__ == '__main__':
    bot.polling(none_stop=True)
