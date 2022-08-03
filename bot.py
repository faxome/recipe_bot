import telebot
import random
from telebot import types
from app import db, Recipes

bot = telebot.TeleBot('5566497434:AAExeWLSda5SL5iFLbOzZTVDKD2sgd2fBRA')


@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("🍳 Завтраки")
    btn2 = types.KeyboardButton("🍝 Обеды")
    btn3 = types.KeyboardButton("🍽 Ужины")
    btn4 = types.KeyboardButton("🥩 У меня есть!")
    markup.add(btn1, btn2, btn3, btn4)
    bot.send_message(message.chat.id,
                     text="Привет, {0.first_name}! Я тестовый бот для поиска рецептов вкуснейших блюд 🍱".format(
                         message.from_user), reply_markup=markup)


@bot.message_handler(content_types=['text'])
def func(message):
    if (message.text == "🍳 Завтраки"):
        random_recipes_b = Recipes.query.filter_by(type='breakfast').all()
        recipe_count_b = len(random_recipes_b)
        random_b_id = int(random.uniform(0, recipe_count_b))
        mess = f'{random_recipes_b[random_b_id].name}\n\n{random_recipes_b[random_b_id].description}'
        bot.send_photo(message.chat.id, photo=open('./static/files/' + random_recipes_b[random_b_id].image_name, 'rb'))
        bot.send_message(message.chat.id, mess, parse_mode='html')

    elif (message.text == "🍝 Обеды"):
        random_recipes_l = Recipes.query.filter_by(type='lunch').all()
        recipe_count_l = len(random_recipes_l)
        random_l_id = int(random.uniform(0, recipe_count_l))
        mess = f'{random_recipes_l[random_l_id].name}\n\n{random_recipes_l[random_l_id].description}'
        bot.send_photo(message.chat.id, photo=open('./static/files/' + random_recipes_l[random_l_id].image_name, 'rb'))
        bot.send_message(message.chat.id, mess, parse_mode='html')

    elif (message.text == "🍽 Ужины"):
        random_recipes_d = Recipes.query.filter_by(type='dinner').all()
        recipe_count_d = len(random_recipes_d)
        random_d_id = int(random.uniform(0, recipe_count_d))
        mess = f'{random_recipes_d[random_d_id].name}\n\n{random_recipes_d[random_d_id].description}'
        bot.send_photo(message.chat.id, photo=open('./static/files/' + random_recipes_d[random_d_id].image_name, 'rb'))
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
            bot.send_photo(message.chat.id, photo=open('./static/files/' + random_recipes_i[random_i_id].image_name, 'rb'))
            bot.send_message(message.chat.id, mess, parse_mode='html')
        else:
            bot.send_message(message.chat.id, text="Нет рецепта с такими продуктами")


bot.polling(none_stop=True)