import telebot
import random
from telebot import types
from app import Recipes
from lorabot import LoraBot
lora_bot = LoraBot("botstat")

bot = telebot.TeleBot('5597091100:AAEMDOfQgjTna9l6sXSVOTNTk_xfVBXAmdo')


@bot.message_handler(commands=['start'])
def start(message):
    lora_bot.user(USER_ID)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("🍳 Завтраки")
    btn2 = types.KeyboardButton("🍝 Обеды")
    btn3 = types.KeyboardButton("🍽 Ужины")
    btn4 = types.KeyboardButton("🍰 Десерты")
    btn5 = types.KeyboardButton("🥩 Мангал")
    btn6 = types.KeyboardButton("🥦 У меня есть!")

    markup.add(btn1, btn2, btn3, btn4, btn5, btn6)
    bot.send_message(message.chat.id,
                     text="Поздравляю, {0.first_name}!\n\n"
                          "Теперь тебе доступна самая вкусная подборка завтраков, обедов и ужинов, а также десертов и блюд на мангале.  \n\n"
                          "Все просто: ты нажимаешь нужную кнопку, я рандомно выдаю прекрасный рецепт с полным описанием. \n\n"
                          "Будет вкусненько. Приятного аппетита ☺️".format(
                         message.from_user), reply_markup=markup)


@bot.message_handler(content_types=['text', 'video'])
def func(message):
    lora_bot.user(USER_ID)
    if (message.text == "🍳 Завтраки"):
        random_recipes_b = Recipes.query.filter_by(type='breakfast').all()
        recipe_count_b = len(random_recipes_b)
        random_b_id = int(random.uniform(0, recipe_count_b))
        mess = f'{random_recipes_b[random_b_id].name}\n\n{random_recipes_b[random_b_id].description}'
        bot.send_video(message.chat.id,
                       video=open('/app/static/files/' + random_recipes_b[random_b_id].image_name, 'rb'))
        bot.send_message(message.chat.id, mess, parse_mode='html')

    elif (message.text == "🍝 Обеды"):
        random_recipes_l = Recipes.query.filter_by(type='lunch').all()
        recipe_count_l = len(random_recipes_l)
        random_l_id = int(random.uniform(0, recipe_count_l))
        mess = f'{random_recipes_l[random_l_id].name}\n\n{random_recipes_l[random_l_id].description}'
        bot.send_video(message.chat.id,
                       video=open('/app/static/files/' + random_recipes_l[random_l_id].image_name, 'rb'))
        bot.send_message(message.chat.id, mess, parse_mode='html')

    elif (message.text == "🍽 Ужины"):
        random_recipes_d = Recipes.query.filter_by(type='dinner').all()
        recipe_count_d = len(random_recipes_d)
        random_d_id = int(random.uniform(0, recipe_count_d))
        mess = f'{random_recipes_d[random_d_id].name}\n\n{random_recipes_d[random_d_id].description}'
        bot.send_video(message.chat.id,
                       video=open('/app/static/files/' + random_recipes_d[random_d_id].image_name, 'rb'))
        bot.send_message(message.chat.id, mess, parse_mode='html')

    elif (message.text == "🍰 Десерты"):
        random_recipes_d = Recipes.query.filter_by(type='dessert').all()
        recipe_count_d = len(random_recipes_d)
        random_d_id = int(random.uniform(0, recipe_count_d))
        mess = f'{random_recipes_d[random_d_id].name}\n\n{random_recipes_d[random_d_id].description}'
        bot.send_video(message.chat.id,
                       video=open('/app/static/files/' + random_recipes_d[random_d_id].image_name, 'rb'))
        bot.send_message(message.chat.id, mess, parse_mode='html')

    elif (message.text == "🥩 У меня есть!"):
        bot.send_message(message.chat.id, text="Введите название продукта")
    else:
        f_ingredient = message.text.lower()
        random_recipes_i = Recipes.query.filter_by(ingredient=f_ingredient).all()
        recipe_count_i = len(random_recipes_i)
        random_i_id = int(random.uniform(0, recipe_count_i))

        if recipe_count_i != 0:
            mess = f'{random_recipes_i[random_i_id].name}\n\n{random_recipes_i[random_i_id].description}'
            bot.send_video(message.chat.id,
                           video=open('/app/static/files/' + random_recipes_i[random_i_id].image_name, 'rb'))
            bot.send_message(message.chat.id, mess, parse_mode='html')
        else:
            bot.send_message(message.chat.id, text="Нет рецепта с такими продуктами")


bot.polling(none_stop=True)

