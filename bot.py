import telebot
import random
from telebot import types
from app import Recipes

bot = telebot.TeleBot('5597091100:AAEMDOfQgjTna9l6sXSVOTNTk_xfVBXAmdo')


@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("🍳 Завтраки")
    btn2 = types.KeyboardButton("🍝 Вторые блюда")
    btn3 = types.KeyboardButton("🍰 Десерты")
    btn4 = types.KeyboardButton("🥩 Мангал")
    btn5 = types.KeyboardButton("🥦 У меня есть!")

    markup.add(btn1, btn2, btn3, btn4, btn5)
    bot.send_message(message.chat.id,
                     text="Поздравляю, {0.first_name}!\n\n"
                          "Теперь тебе доступна самая вкусная подборка завтраков, обедов и ужинов, а также десертов и блюд на мангале.  \n\n"
                          "Все просто: ты нажимаешь нужную кнопку, я рандомно выдаю прекрасный рецепт с полным описанием. \n\n"
                          "Будет вкусненько. Приятного аппетита ☺️".format(
                         message.from_user), reply_markup=markup)


@bot.message_handler(content_types=['text', 'video'])
def func(message):
    if (message.text == "🍳 Завтраки"):
        random_recipes_b = Recipes.query.filter_by(type='breakfast').all()
        recipe_count_b = len(random_recipes_b)
        random_b_id = int(random.uniform(0, recipe_count_b))
        mess = f'{random_recipes_b[random_b_id].name}\n\n{random_recipes_b[random_b_id].description}'
        bot.send_video(message.chat.id, video=open('/app/static/files/' + random_recipes_b[random_b_id].image_name, 'rb'), width=720, height=1280)
        bot.send_message(message.chat.id, mess, parse_mode='html')

    elif (message.text == "🍝 Вторые блюда"):
        random_recipes_l = Recipes.query.filter_by(type='lunch').all()
        recipe_count_l = len(random_recipes_l)
        random_l_id = int(random.uniform(0, recipe_count_l))
        mess = f'{random_recipes_l[random_l_id].name}\n\n{random_recipes_l[random_l_id].description}'
        bot.send_video(message.chat.id, video=open('/app/static/files/' + random_recipes_l[random_l_id].image_name, 'rb'), width=720, height=1280)
        bot.send_message(message.chat.id, mess, parse_mode='html')

    elif (message.text == "🍰 Десерты"):
        random_recipes_d = Recipes.query.filter_by(type='dessert').all()
        recipe_count_d = len(random_recipes_d)
        random_d_id = int(random.uniform(0, recipe_count_d))
        mess = f'{random_recipes_d[random_d_id].name}\n\n{random_recipes_d[random_d_id].description}'
        bot.send_video(message.chat.id, video=open('/app/static/files/' + random_recipes_d[random_d_id].image_name, 'rb'), width=720, height=1280)
        bot.send_message(message.chat.id, mess, parse_mode='html')

    elif (message.text == "🥩 Мангал"):
        random_recipes_g = Recipes.query.filter_by(type='grill').all()
        recipe_count_g = len(random_recipes_g)
        random_g_id = int(random.uniform(0, recipe_count_g))
        mess = f'{random_recipes_g[random_g_id].name}\n\n{random_recipes_g[random_g_id].description}'
        bot.send_video(message.chat.id, video=open('/app/static/files/' + random_recipes_g[random_g_id].image_name, 'rb'), width=720, height=1280)
        bot.send_message(message.chat.id, mess, parse_mode='html')

    elif (message.text == "🥦 У меня есть!"):
        mess = bot.send_message(message.chat.id, 'Введите название продукта')
        bot.register_next_step_handler(mess, ihave)
    else:
        bot.send_message(message.chat.id, text="Выберите тип рецепта")


def ihave(message):
    f_ingredient = message.text.lower()
    random_recipes_i = Recipes.query.filter_by(ingredient=f_ingredient).all()
    recipe_count_i = len(random_recipes_i)
    random_i_id = int(random.uniform(0, recipe_count_i))

    if recipe_count_i != 0:
        mess = f'{random_recipes_i[random_i_id].name}\n\n{random_recipes_i[random_i_id].description}'
        bot.send_video(message.chat.id,
                       video=open('/app/static/files/' + random_recipes_i[random_i_id].image_name, 'rb'), width=720, height=1280)
        bot.send_message(message.chat.id, mess, parse_mode='html')
    else:
        bot.send_message(message.chat.id, text="Нет рецепта с такими продуктами")


bot.polling(none_stop=True)
