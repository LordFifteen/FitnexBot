import telebot
from telebot import types
import sqlite3
import random
from datetime import datetime

BOT_TOKEN = ""
bot = telebot.TeleBot(BOT_TOKEN)

#Мотивационные цитаты
MOTIVATIONAL_QUOTES = [
    "«Я плакал, потому что у меня не было футбольных кед, но однажды я встретил человека, у которого не было ног», — Зинедин Зидан",
    "«Я никогда не понимал значение слова «сдаться», — Жан-Клод Ван Дамм",
    "«Я промахнулся 9000 раз за свою карьеру. Я проиграл почти 300 игр. 26 раз мне был доверен решающий бросок, и я промахивался. Я терпел поражения снова и снова. И именно поэтому я достиг успеха», — Майкл Джордан",
    "«Сильный характер выковывается, только когда преодолеваешь сопротивление — и в спортивном зале, и в жизни», — Арнольд Шварценеггер",
    "«Тренируйся с теми, кто сильнее. Не сдавайся там, где сдаются другие. И победишь там, где победить нельзя», — Брюс Ли",
    "«Научите спортсмена до конца бороться за любое место, и он сумеет сражаться за первое», — Лариса Латынина",
    "«Успех не случайность. Это тяжёлая работа, настойчивость, обучение, изучение, жертвоприношение и, прежде всего, любовь к тому, что вы делаете или учитесь делать», — Пеле",
    "«Тот, кто хочет добиться убедительных побед, обязан пытаться прыгнуть выше головы», — Лев Яшин",
    "«Мы не хотим рассказывать о своих мечтах, мы хотим их показать». – Криштиану Роналду",
    "«Если что-то стоит между тобой и твоим успехом, убери это. Никогда не отказывайся». – Дуэйн «Скала» Джонсон"
]

#Планы тренировок
WORKOUT_PLANS = {
    "beginner": """
🧘‍♂️ НАЧАЛЬНЫЙ УРОВЕНЬ (3 дня/неделю)

День 1: Грудь + Трицепс
• Жим лежа: 3х10
• Отжимания: 3хмакс
• Разведение гантелей: 3х12
• Французский жим: 3х12

День 2: Спина + Бицепс
• Тяга верхнего блока: 3х10
• Тяга штанги в наклоне: 3х10
• Подтягивания: 3хмакс
• Сгибание рук: 3х12

День 3: Ноги
• Приседания: 3х10
• Румынская тяга 3*8-12
• Разгибание ног 3*12-15
• Сгибание ног 3*12-15
""",
    "intermediate": """
🏋️ СРЕДНИЙ УРОВЕНЬ (4 дня/неделю)

День 1: Грудь
• Жим лежа: 4х8
• Жим гантелей на наклонной: 3х10
• Кроссовер: 3х12
• Отжимания на брусьях: 3хмакс

День 2: Спина
• Становая тяга: 4х6
• Подтягивания: 4хмакс
• Тяга Т-грифа: 3х10
• Тяга нижнего блока: 3х12

День 3: Ноги
• Приседания со штангой: 4х8
• Приседания в Гакк-тренажере 3*8-12
• Выпады на месте 3*8-12
• Икры стоя: 4х15

День 4: Плечи + Руки
• Армейский жим: 4х8
• Махи гантелями: 3х12
• Подъем штанги на бицепс: 3х10
• Французский жим: 3х12
""",
    "home": """
🏠 ДОМАШНИЕ ТРЕНИРОВКИ

Ежедневный комплекс:
• Отжимания: 4х15
• Приседания: 4х20
• Планка: 3х60 сек
• Скручивания: 4х20
• Берпи: 3х10
• Выпады: 3х15 на ногу
"""
}


#База данных
def init_db():
    conn = sqlite3.connect('fitness.db', check_same_thread=False)
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            username TEXT,
            weight REAL,
            height REAL,
            age INTEGER,
            goal TEXT
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS workouts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            type TEXT,
            duration INTEGER,
            date TEXT
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS nutrition (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            calories INTEGER,
            protein REAL,
            fat REAL,
            carbs REAL,
            date TEXT
        )
    ''')

    conn.commit()
    conn.close()

def init_reminders_db():
    conn = sqlite3.connect('fitness.db', check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS reminders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            time TEXT,
            days TEXT
        )
    ''')
    conn.commit()
    conn.close()


#Клавиатуры
def main_keyboard():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row("📈 Мой прогресс", "📝️ Планы тренировок")
    keyboard.row("🥗 Добавить питание", "➕ Добавить тренировку")
    keyboard.row("🗣 Мотивация", "⏰ Напоминания")
    keyboard.row("👤 Профиль")
    return keyboard


def workout_plans_keyboard():
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton("Начальный", callback_data="plan_beginner"))
    keyboard.add(types.InlineKeyboardButton("Средний", callback_data="plan_intermediate"))
    keyboard.add(types.InlineKeyboardButton("Домашний", callback_data="plan_home"))
    return keyboard


def goals_keyboard():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row("🏋️‍♂️ Набор массы", "🚴‍♀️ Похудение")
    keyboard.row("⚖️ Поддержание", "⛹️‍♂️ Выносливость")
    return keyboard


#Команда /start
@bot.message_handler(commands=['start'])
def start_command(message):
    user_id = message.from_user.id
    username = message.from_user.first_name

    conn = sqlite3.connect('fitness.db')
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
    user = cursor.fetchone()

    if not user:
        bot.send_message(
            message.chat.id,
            f"🤗 Привет, {username}!\n"
            f"Я твой фитнес-трекер! Давай настроим профиль.\n"
            f"Введи свой вес в кг:"
        )
        bot.register_next_step_handler(message, get_weight)
    else:
        bot.send_message(
            message.chat.id,
            f"С возвращением, {username}!",
            reply_markup=main_keyboard()
        )

    conn.close()


def get_weight(message):
    try:
        weight = float(message.text)
        bot.send_message(message.chat.id, "📏 Введи свой рост в см:")
        bot.register_next_step_handler(message, get_height, weight)
    except:
        bot.send_message(message.chat.id, "❗️ Введи число (например: 36)")
        bot.register_next_step_handler(message, get_weight)


def get_height(message, weight):
    try:
        height = float(message.text)
        bot.send_message(message.chat.id, "🎂 Введи свой возраст:")
        bot.register_next_step_handler(message, get_age, weight, height)
    except:
        bot.send_message(message.chat.id, "❗️ Введи число (например: 100)")
        bot.register_next_step_handler(message, get_height, weight)


def get_age(message, weight, height):
    try:
        age = int(message.text)
        bot.send_message(
            message.chat.id,
            "🎯 Выбери свою цель:",
            reply_markup=goals_keyboard()
        )
        bot.register_next_step_handler(message, get_goal, weight, height, age)
    except:
        bot.send_message(message.chat.id, "❗️ Введи целое число")
        bot.register_next_step_handler(message, get_age, weight, height)


def get_goal(message, weight, height, age):
    goal = message.text
    user_id = message.from_user.id
    username = message.from_user.first_name

    conn = sqlite3.connect('fitness.db')
    cursor = conn.cursor()

    cursor.execute(
        'INSERT OR REPLACE INTO users VALUES (?, ?, ?, ?, ?, ?)',
        (user_id, username, weight, height, age, goal)
    )
    conn.commit()
    conn.close()

    bot.send_message(
        message.chat.id,
        f"☑️ Профиль создан!\n"
        f"• Вес: {weight} кг\n"
        f"• Рост: {height} см\n"
        f"• Возраст: {age} лет\n"
        f"• Цель: {goal}",
        reply_markup=main_keyboard()
    )


#Мой прогресс
@bot.message_handler(func=lambda message: message.text == "📈 Мой прогресс")
def show_progress(message):
    user_id = message.from_user.id

    conn = sqlite3.connect('fitness.db')
    cursor = conn.cursor()

    #Данные пользователя
    cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
    user = cursor.fetchone()

    #Последние тренировки
    cursor.execute(
        'SELECT * FROM workouts WHERE user_id = ? ORDER BY date DESC LIMIT 3',
        (user_id,)
    )
    workouts = cursor.fetchall()

    #Последнее питание
    cursor.execute(
        'SELECT * FROM nutrition WHERE user_id = ? ORDER BY date DESC LIMIT 1',
        (user_id,)
    )
    nutrition = cursor.fetchone()

    response = "📈 ТВОЙ ПРОГРЕСС\n\n"

    if user:
        response += f"📏 Профиль:\n• Вес: {user[2]} кг\n• Рост: {user[3]} см\n• Цель: {user[5]}\n\n"

    if workouts:
        response += "🏋️ Последние тренировки:\n"
        for workout in workouts:
            response += f"• {workout[2]} - {workout[3]} мин\n"
    else:
        response += "🏋️ Тренировок пока нет\n"

    if nutrition:
        response += f"\n🥗 Последнее питание:\n• {nutrition[2]} ккал\n• Б: {nutrition[3]}г, Ж: {nutrition[4]}г, У: {nutrition[5]}г"

    bot.send_message(message.chat.id, response)
    conn.close()


#Команда сброса данных
@bot.message_handler(commands=['reset'])
def reset_command(message):
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton("☑️ Да", callback_data="reset_confirm"))
    keyboard.add(types.InlineKeyboardButton("❌ Нет", callback_data="reset_cancel"))

    bot.send_message(
        message.chat.id,
        "⚠️ Сбросить ВСЕ данные? Это необратимо!",
        reply_markup=keyboard
    )


#Обработчик подтверждения
@bot.callback_query_handler(func=lambda call: call.data.startswith('reset_'))
def handle_reset(call):
    if call.data == "reset_confirm":
        conn = sqlite3.connect('fitness.db')
        cursor = conn.cursor()
        cursor.execute('DELETE FROM users WHERE user_id = ?', (call.from_user.id,))
        cursor.execute('DELETE FROM workouts WHERE user_id = ?', (call.from_user.id,))
        cursor.execute('DELETE FROM nutrition WHERE user_id = ?', (call.from_user.id,))
        conn.commit()
        conn.close()

        bot.send_message(call.message.chat.id, "☑️ Данные удалены! Используй /start")
    else:
        bot.send_message(call.message.chat.id, "❌ Отменено")

    bot.delete_message(call.message.chat.id, call.message.message_id)


#Планы тренировок
@bot.message_handler(func=lambda message: message.text == "📝️ Планы тренировок")
def show_workout_plans(message):
    bot.send_message(
        message.chat.id,
        "Выбери уровень тренировок:",
        reply_markup=workout_plans_keyboard()
    )


@bot.callback_query_handler(func=lambda call: call.data.startswith('plan_'))
def send_workout_plan(call):
    plan_type = call.data.split('_')[1]
    plan = WORKOUT_PLANS.get(plan_type, "План не найден")
    bot.send_message(call.message.chat.id, plan)


#Добавить тренировку
@bot.message_handler(func=lambda message: message.text == "➕ Добавить тренировку")
def add_workout(message):
    bot.send_message(message.chat.id, "❔ Какая была тренировка?\n(например: силовая, кардио, йога)")
    bot.register_next_step_handler(message, get_workout_type)


def get_workout_type(message):
    workout_type = message.text
    bot.send_message(message.chat.id, "❔ Сколько минут длилась?")
    bot.register_next_step_handler(message, get_workout_duration, workout_type)


def get_workout_duration(message, workout_type):
    try:
        duration = int(message.text)
        user_id = message.from_user.id
        date = datetime.now().strftime("%Y-%m-%d %H:%M")

        conn = sqlite3.connect('fitness.db')
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO workouts (user_id, type, duration, date) VALUES (?, ?, ?, ?)',
            (user_id, workout_type, duration, date)
        )
        conn.commit()
        conn.close()

        bot.send_message(
            message.chat.id,
            f"☑️ Тренировка сохранена!\n• {workout_type} - {duration} мин"
        )
    except:
        bot.send_message(message.chat.id, "❗️ Введи число минут")


#Добавить питание
@bot.message_handler(func=lambda message: message.text == "🥗 Добавить питание")
def add_nutrition(message):
    bot.send_message(message.chat.id, "🥗 Введи количество калорий:")
    bot.register_next_step_handler(message, get_calories)


def get_calories(message):
    try:
        calories = int(message.text)
        bot.send_message(message.chat.id, "🍗 Введи белки (г):")
        bot.register_next_step_handler(message, get_protein, calories)
    except:
        bot.send_message(message.chat.id, "❗️ Введи число")


def get_protein(message, calories):
    try:
        protein = float(message.text)
        bot.send_message(message.chat.id, "🥑 Введи жиры (г):")
        bot.register_next_step_handler(message, get_fat, calories, protein)
    except:
        bot.send_message(message.chat.id, "❗️ Введи число")
        bot.register_next_step_handler(message, get_protein, calories)


def get_fat(message, calories, protein):
    try:
        fat = float(message.text)
        bot.send_message(message.chat.id, "🍛 Введи углеводы (г):")
        bot.register_next_step_handler(message, get_carbs, calories, protein, fat)
    except:
        bot.send_message(message.chat.id, "❗️ Введи число")
        bot.register_next_step_handler(message, get_fat, calories, protein)


def get_carbs(message, calories, protein, fat):
    try:
        carbs = float(message.text)
        user_id = message.from_user.id
        date = datetime.now().strftime("%Y-%m-%d %H:%M")

        conn = sqlite3.connect('fitness.db')
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO nutrition (user_id, calories, protein, fat, carbs, date) VALUES (?, ?, ?, ?, ?, ?)',
            (user_id, calories, protein, fat, carbs, date)
        )
        conn.commit()
        conn.close()

        bot.send_message(
            message.chat.id,
            f"☑️ Питание сохранено!\n"
            f"• Калории: {calories}\n"
            f"• Б: {protein}г, Ж: {fat}г, У: {carbs}г"
        )
    except:
        bot.send_message(message.chat.id, "❗️ Введи число")


#Мотивация
@bot.message_handler(func=lambda message: message.text == "🗣 Мотивация")
def send_motivation(message):
    quote = random.choice(MOTIVATIONAL_QUOTES)
    bot.send_message(message.chat.id, f"💭 {quote}")


#Профиль
@bot.message_handler(func=lambda message: message.text == "👤 Профиль")
def show_profile(message):
    user_id = message.from_user.id

    conn = sqlite3.connect('fitness.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
    user = cursor.fetchone()
    conn.close()

    if user:
        response = (
            f"👤 ТВОЙ ПРОФИЛЬ\n\n"
            f"• Имя: {user[1]}\n"
            f"• Вес: {user[2]} кг\n"
            f"• Рост: {user[3]} см\n"
            f"• Возраст: {user[4]} лет\n"
            f"• Цель: {user[5]}\n\n"
            f"Используй /start для изменения данных"
        )
    else:
        response = "Профиль не найден. Используй /start"

    bot.send_message(message.chat.id, response)


@bot.message_handler(func=lambda message: message.text == "⏰ Напоминания")
def reminders_menu(message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row("⏰ Установить", "❌ Удалить")
    keyboard.row("📃 Список", "◀️ Назад")
    bot.send_message(message.chat.id, "⏰ Управление напоминаниями:", reply_markup=keyboard)


@bot.message_handler(func=lambda message: message.text == "⏰ Установить")
def set_reminder(message):
    bot.send_message(message.chat.id, "🕐 Введи время:")
    bot.register_next_step_handler(message, get_reminder_time)


def get_reminder_time(message):
    try:
        time_str = message.text
        datetime.strptime(time_str, "%H:%M")
        bot.send_message(
            message.chat.id,
            "📅 В какие дни недели напоминать?\n"
            "Напиши через запятую номера дней:\n"
            "1-ПН, 2-ВТ, 3-СР, 4-ЧТ, 5-ПТ, 6-СБ, 7-ВС\n"
            "Например: 1,3,5 или 2,4,6,7"
        )
        bot.register_next_step_handler(message, get_reminder_days, time_str)
    except ValueError:
        bot.send_message(
            message.chat.id,
            "❗️Неверный формат времени. Используй часы и минуты (например, 09:00)"
        )
        bot.register_next_step_handler(message, get_reminder_time)


def get_reminder_days(message, time_str):
    try:
        user_id = message.from_user.id
        days_input = message.text
        days_list = [day.strip() for day in days_input.split(',')]

        # Проверяем, что все дни от 1 до 7
        valid_days = True
        for day in days_list:
            if not day.isdigit() or int(day) < 1 or int(day) > 7:
                valid_days = False
                break

        if not valid_days:
            bot.send_message(
                message.chat.id,
                "❗️Неверный формат дней. Используй номера от 1 до 7 через запятую (например: 1,3,5)\n"
                "1-ПН, 2-ВТ, 3-СР, 4-ЧТ, 5-ПТ, 6-СБ, 7-ВС"
            )
            return

        days_str = ','.join(days_list)

        conn = sqlite3.connect('fitness.db')
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO reminders (user_id, time, days) VALUES (?, ?, ?)',
            (user_id, time_str, days_str)
        )
        conn.commit()
        conn.close()

        # Показываем пользователю в понятном формате
        day_names = {'1': 'ПН', '2': 'ВТ', '3': 'СР', '4': 'ЧТ', '5': 'ПТ', '6': 'СБ', '7': 'ВС'}
        days_display = ', '.join([day_names[day] for day in days_list])

        bot.send_message(
            message.chat.id,
            f"☑️ Напоминание установлено!\n"
            f"⏰ Время: {time_str}\n"
            f"📅 Дни: {days_display}"
        )

    except Exception as e:
        bot.send_message(
            message.chat.id,
            f"❗️ Ошибка: {e}\nПопробуй еще раз с начала"
        )


@bot.message_handler(func=lambda message: message.text == "📃 Список")
def show_reminders(message):
    user_id = message.from_user.id
    conn = sqlite3.connect('fitness.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM reminders WHERE user_id = ?', (user_id,))
    reminders = cursor.fetchall()
    conn.close()

    if not reminders:
        bot.send_message(message.chat.id, "📭 Нет напоминаний")
        return

    response = "📋 Твои напоминания:\n"
    for reminder in reminders:
        response += f"⏰ {reminder[2]} - {reminder[3]}\n"
    bot.send_message(message.chat.id, response)


@bot.message_handler(func=lambda message: message.text == "❌ Удалить")
def delete_reminder(message):
    user_id = message.from_user.id
    conn = sqlite3.connect('fitness.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM reminders WHERE user_id = ?', (user_id,))
    conn.commit()
    conn.close()
    bot.send_message(message.chat.id, "☑️ Все напоминания удалены!")


@bot.message_handler(func=lambda message: message.text == "◀️ Назад")
def back_to_main(message):
    bot.send_message(message.chat.id, "Главное меню:", reply_markup=main_keyboard())


#Запуск бота
if __name__ == "__main__":
    print("Фитнес-бот запускается...")
    init_db()
    init_reminders_db()
    print("Прочитана база данных")
    print("Бот запущен!")
    bot.infinity_polling()

