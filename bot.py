import os
import random
import asyncio
from dotenv import load_dotenv

from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup
)

from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ContextTypes,
    filters,
    PollAnswerHandler
)

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")


# =========================
# کلمات بازی
# =========================

WORDS = ['سیب', 'پرتقال', 'موز', 'هندوانه', 'انار', 'انگور', 'هلو', 'گیلاس', 'توت\u200cفرنگی', 'لیمو', 'خیار', 'گوجه', 'هویج', 'سیب\u200cزمینی', 'پیاز', 'سیر', 'ذرت', 'بادمجان', 'کدو', 'کاهو', 'نان', 'پنیر', 'برنج', 'ماکارونی', 'پیتزا', 'همبرگر', 'ساندویچ', 'سوپ', 'سالاد', 'کیک', 'بستنی', 'شکلات', 'عسل', 'مربا', 'چای', 'قهوه', 'آبمیوه', 'نوشابه', 'شیر', 'ماست', 'کتاب', 'دفتر', 'مداد', 'خودکار', 'پاک\u200cکن', 'تراش', 'خط\u200cکش', 'کیف', 'کوله\u200cپشتی', 'میز', 'صندلی', 'تخت', 'کمد', 'آینه', 'چراغ', 'ساعت', 'تلویزیون', 'رادیو', 'تلفن', 'دوربین', 'رایانه', 'لپ\u200cتاپ', 'تبلت', 'صفحه\u200cکلید', 'ماوس', 'هدفون', 'بلندگو', 'پرینتر', 'کنسول', 'دسته\u200cبازی', 'بازی', 'ربات', 'هواپیما', 'قطار', 'اتوبوس', 'دوچرخه', 'موتورسیکلت', 'کشتی', 'زیردریایی', 'خودرو', 'تاکسی', 'آمبولانس', 'آتش\u200cنشانی', 'پلیس', 'چراغ\u200cقرمز', 'جاده', 'پل', 'تونل', 'فرودگاه', 'ایستگاه', 'فروشگاه', 'مدرسه', 'دانشگاه', 'بیمارستان', 'پارک', 'سینما', 'رستوران', 'کتابخانه', 'موزه', 'خانه', 'آپارتمان', 'آشپزخانه', 'حمام', 'اتاق', 'بالکن', 'باغ', 'حیاط', 'درخت', 'گل', 'رز', 'لاله', 'آفتابگردان', 'کاکتوس', 'جنگل', 'کوه', 'رودخانه', 'دریا', 'ساحل', 'جزیره', 'بیابان', 'غار', 'آبشار', 'ابر', 'باران', 'برف', 'رعدوبرق', 'رنگین\u200cکمان', 'خورشید', 'ماه', 'ستاره', 'سیاره', 'فضا', 'موشک', 'فضانورد', 'زمین', 'آتش', 'باد', 'یخ', 'شن', 'سگ', 'گربه', 'ببر', 'فیل', 'زرافه', 'میمون', 'خرس', 'گرگ', 'روباه', 'خرگوش', 'اسب', 'گاو', 'گوسفند', 'بز', 'مرغ', 'خروس', 'اردک', 'ماهی', 'دلفین', 'نهنگ', 'کوسه', 'لاک\u200cپشت', 'مار', 'تمساح', 'قورباغه', 'پروانه', 'زنبور', 'مورچه', 'عنکبوت', 'عینک', 'کلاه', 'کفش', 'جوراب', 'پیراهن', 'شلوار', 'کت', 'کاپشن', 'بارانی', 'چتر', 'کیف\u200cدستی', 'گردنبند', 'دستبند', 'انگشتر', 'چمدان', 'دستکش', 'شال', 'روسری', 'کمربند', 'توپ', 'فوتبال', 'بسکتبال', 'والیبال', 'تنیس', 'شطرنج', 'دویدن', 'شنا', 'دوچرخه\u200cسواری', 'کوهنوردی', 'مسابقه', 'مدال', 'جام', 'استادیوم', 'زمین\u200cبازی', 'دروازه', 'راکت', 'طناب', 'بادبادک', 'پازل', 'قلم\u200cمو', 'نقاشی', 'عکس', 'موسیقی', 'گیتار', 'پیانو', 'ویولن', 'دف', 'فلوت', 'میکروفون', 'فیلم', 'بازیگر', 'کارگردان', 'صحنه', 'ماسک', 'عروسک', 'شمع', 'بادکنک', 'کادو', 'جشن', 'تولد', 'عروسی', 'تعطیلات', 'سفر', 'نقشه', 'قطب\u200cنما', 'هتل', 'چادر', 'کمپ', 'کلید', 'قفل', 'در', 'پنجره', 'پله', 'آسانسور', 'نردبان', 'چکش', 'پیچ\u200cگوشتی', 'میخ', 'چراغ\u200cقوه', 'باتری', 'شارژر', 'کابل', 'پریز', 'ساعت\u200cمچی', 'زنگ', 'سوت', 'سنجاق', 'پول', 'سکه', 'اسکناس', 'کیف\u200cپول', 'بانک', 'فروشنده', 'مشتری', 'بازار', 'مغازه', 'صندوق', 'دکتر', 'پرستار', 'معلم', 'دانشجو', 'مهندس', 'آشپز', 'راننده', 'خلبان', 'ملوان', 'کشاورز', 'نجار', 'نقاش', 'عکاس', 'نویسنده', 'خواننده', 'ورزشکار', 'دانشمند', 'برنامه\u200cنویس', 'طراح', 'کاغذ', 'پاکت', 'نامه', 'تمبر', 'تقویم', 'چراغ\u200cمطالعه', 'تخته', 'گچ', 'زنگوله', 'پرچم', 'تاج', 'شمشیر', 'سپر', 'قلعه', 'پادشاه', 'ملکه', 'شوالیه', 'گنج', 'نقشه\u200cگنج', 'دزد', 'کارآگاه', 'جاسوس', 'راز', 'سرنخ', 'معما', 'رمز', 'کد', 'اثر\u200cانگشت', 'ذره\u200cبین', 'دوربین\u200cمداربسته', 'مغز', 'قلب', 'چشم', 'گوش', 'بینی', 'دست', 'پا', 'دندان', 'مو', 'لب', 'عینک\u200cآفتابی', 'کرم', 'صابون', 'حوله', 'مسواک', 'خمیردندان']


# =========================
# اطلاعات بازی
# =========================

games = {}


async def delete_stage_messages(chat_id, context):
    game = games.get(chat_id)
    if not game:
        return
    ids = game.get("stage_message_ids", [])
    for message_id in ids:
        try:
            await context.bot.delete_message(chat_id=chat_id, message_id=message_id)
        except Exception:
            pass
    game["stage_message_ids"] = []


async def send_stage_message(chat_id, context, text, reply_markup=None):
    await delete_stage_messages(chat_id, context)
    message = await context.bot.send_message(
        chat_id=chat_id,
        text=text,
        reply_markup=reply_markup
    )
    games[chat_id]["stage_message_ids"] = [message.message_id]
    return message


# =========================
# شروع ربات
# =========================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    keyboard = [
        [
            InlineKeyboardButton(
                "🎮 شروع بازی",
                callback_data="start_game"
            )
        ]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "🎮 سلام!\n"
        "به بازی جاسوس خوش اومدی!\n\n"
        "برای شروع روی دکمه زیر بزن:",
        reply_markup=reply_markup
    )


# =========================
# انتخاب تعداد بازیکنان
# =========================

async def start_game(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query
    await query.answer()

    keyboard = [
        [
            InlineKeyboardButton("3 نفر", callback_data="players_3"),
            InlineKeyboardButton("4 نفر", callback_data="players_4")
        ],
        [
            InlineKeyboardButton("5 نفر", callback_data="players_5"),
            InlineKeyboardButton("6 نفر", callback_data="players_6")
        ],
        [
            InlineKeyboardButton("7 نفر", callback_data="players_7"),
            InlineKeyboardButton("8 نفر", callback_data="players_8")
        ],
        [
            InlineKeyboardButton("9 نفر", callback_data="players_9"),
            InlineKeyboardButton("10 نفر", callback_data="players_10")
        ]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await query.message.reply_text(
        "🎮 بازی شروع شد!\n\n"
        "👥 چند نفر قراره بازی کنن؟",
        reply_markup=reply_markup
    )
    # =========================
# ساخت بازی
# =========================

async def select_players(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query
    await query.answer()

    players = int(
        query.data.replace("players_", "")
    )

    chat_id = query.message.chat_id

    games[chat_id] = {
        "max_players": players,
        "players": [],
        "status": "waiting",
        "stage_message_ids": [],
        "role_message_id": None,
        "roles_viewed": set()
    }

    keyboard = [
        [
            InlineKeyboardButton(
                "👤 پیوستن به بازی",
                callback_data="join_game"
            )
        ],
        [
            InlineKeyboardButton(
                "🚀 شروع بازی",
                callback_data="launch_game"
            )
        ]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await send_stage_message(
        chat_id, context,
        f"🎮 بازی {players} نفره ساخته شد!\n\n"
        "هر بازیکن روی «👤 پیوستن به بازی» بزنه.\n"
        "بعد از زدن دکمه، اسمش رو همین‌جا داخل گروه بفرسته.\n\n"
        "وقتی همه پیوستن، روی «🚀 شروع بازی» بزن.",
        reply_markup=reply_markup
    )


# =========================
# پیوستن بازیکن
# =========================

async def join_game(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query
    await query.answer()

    chat_id = query.message.chat_id
    user = query.from_user

    game = games.get(chat_id)

    if not game:
        await query.message.reply_text(
            "❌ بازی‌ای وجود نداره."
        )
        return

    for player in game["players"]:

        if player["user_id"] == user.id:

            await query.answer(
                "تو قبلاً به بازی پیوستی!",
                show_alert=True
            )
            return

    if len(game["players"]) >= game["max_players"]:

        await query.answer(
            "❌ ظرفیت بازی پر شده!",
            show_alert=True
        )
        return

    context.user_data["waiting_for_name"] = chat_id

    await query.message.reply_text(
        f"👤 {user.first_name}، حالا اسمت رو همین‌جا داخل گروه بفرست تا وارد بازی بشی."
    )
        # =========================
        # =========================
# ثبت اسم بازیکن
# =========================

async def get_player_name(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    if "waiting_for_name" not in context.user_data:
        return

    chat_id = context.user_data["waiting_for_name"]

    game = games.get(chat_id)

    if not game:
        return

    name = update.message.text.strip()
    user = update.effective_user

    if not name:
        return

    for player in game["players"]:

        if player["user_id"] == user.id:
            return

    if len(game["players"]) >= game["max_players"]:
        return

    game["players"].append({
        "user_id": user.id,
        "name": name
    })

    del context.user_data["waiting_for_name"]

    current = len(game["players"])
    maximum = game["max_players"]

    await update.message.reply_text(
        f"✅ {name} وارد بازی شد!\n\n"
        f"👥 بازیکنان: {current}/{maximum}\n\n"
        "اگر بازیکن دیگری هست، دکمه «پیوستن به بازی» "
        "رو بزنه."
    )

    await context.bot.send_message(
        chat_id=chat_id,
        text=(
            f"👤 {name} به بازی پیوست.\n"
            f"👥 تعداد بازیکنان: {current}/{maximum}"
        )
    )
    # =========================
# شروع واقعی بازی
# =========================

async def launch_game(update, context):
    query = update.callback_query
    chat_id = query.message.chat_id
    game = games.get(chat_id)

    if not game:
        await query.answer(
            "❌ بازی‌ای پیدا نشد.",
            show_alert=True
        )
        return

    players = game["players"]
    maximum = game["max_players"]

    if len(players) < maximum:
        await query.answer(
            f"هنوز {maximum - len(players)} نفر کم هستند!",
            show_alert=True
        )
        return

    # انتخاب تصادفی جاسوس
    spy = random.choice(players)

    # انتخاب تصادفی کلمه
    secret_word = random.choice(WORDS)

    game["spy_id"] = spy["user_id"]
    game["secret_word"] = secret_word
    game["status"] = "playing"

    await query.answer()

    keyboard = [
        [
            InlineKeyboardButton(
                "🔐 نمایش نقش من",
                callback_data="show_role"
            )
        ]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    role_message = await send_stage_message(
        chat_id, context,
        "🎉 بازی شروع شد!\n\n"
        "🔐 نقش‌ها آماده هستند.\n"
        "هر بازیکن فقط روی دکمه زیر بزند تا نقش خودش را به‌صورت خصوصی ببیند.\n\n"
        "⚠️ نقش خودت را به بقیه نشان نده!",
        reply_markup=reply_markup
    )

    # پیام نقش تا وقتی همه بازیکنان نقش خود را نبینند باقی می‌ماند
    game["role_message_id"] = role_message.message_id
    game["stage_message_ids"] = []
    game["roles_viewed"] = set()

    # شروع مرحله صحبت
    await start_discussion(chat_id, context)
async def show_role(update, context):
    query = update.callback_query
    chat_id = query.message.chat_id
    user_id = query.from_user.id

    game = games.get(chat_id)

    if not game:
        await query.answer("❌ بازی‌ای پیدا نشد.", show_alert=True)
        return

    player = next(
        (player for player in game["players"]
         if player["user_id"] == user_id),
        None
    )

    if not player:
        await query.answer(
            "❌ تو جزو بازیکنان این بازی نیستی!",
            show_alert=True
        )
        return

    if game.get("status") not in ["playing", "discussion"]:
        await query.answer(
            "⏳ هنوز نقش‌ها آماده نیستند یا بازی تمام شده.",
            show_alert=True
        )
        return

    if user_id == game["spy_id"]:
        role_text = (
            "🕵️‍♂️ نقش تو: جاسوس\n\n"
            "🤫 کلمه مخفی رو نمی‌دونی!"
        )
    else:
        role_text = (
            "👤 نقش تو: شهروند\n\n"
            f"🔑 کلمه مخفی:\n{game['secret_word']}"
        )

    # نمایش مطمئن نقش به خود بازیکن در PV ربات
    try:
        await context.bot.send_message(
            chat_id=user_id,
            text=role_text
        )
    except Exception:
        pass

    # نمایش فوری به صورت پنجره روی همان دکمه؛ اگر PV قبلاً باز نشده باشد
    await query.answer(
        role_text,
        show_alert=True
    )

    game.setdefault("roles_viewed", set()).add(user_id)

    # وقتی همه بازیکنان نقش خود را دیدند، پیام نقش از گروه حذف می‌شود
    if len(game["roles_viewed"]) >= len(game["players"]):
        role_message_id = game.get("role_message_id")
        if role_message_id:
            try:
                await context.bot.delete_message(
                    chat_id=chat_id,
                    message_id=role_message_id
                )
            except Exception:
                pass
            game["role_message_id"] = None

    # =========================
# شروع مرحله صحبت
# =========================

async def start_discussion(
    chat_id,
    context: ContextTypes.DEFAULT_TYPE
):

    game = games.get(chat_id)

    if not game:
        return

    players = game["players"]

    # ساخت ترتیب تصادفی صحبت
    order = players.copy()
    random.shuffle(order)

    game["speaking_order"] = order
    game["status"] = "discussion"

    text = "🎲 ترتیب تصادفی صحبت:\n\n"

    for i, player in enumerate(order, start=1):
        text += f"{i}️⃣ {player['name']}\n"

    text += (
        "\n🗣️ حالا نوبت صحبت کردن شماست!\n\n"
        "⏱️ ۳ دقیقه فرصت دارید با هم صحبت کنید "
        "و درباره جاسوس حدس بزنید.\n\n"
        "🤫 ربات تا پایان این ۳ دقیقه کاری انجام نمی‌دهد."
    )

    await send_stage_message(chat_id, context, text)

    # صبر کردن دقیقاً ۳ دقیقه
    await asyncio.sleep(180)

    # بعد از ۳ دقیقه، رأی‌گیری
    await start_vote(chat_id, context)
    # =========================
# شروع رأی‌گیری
# =========================

async def start_vote(
    chat_id,
    context: ContextTypes.DEFAULT_TYPE
):

    game = games.get(chat_id)

    if not game:
        return

    players = game["players"]

    game["status"] = "voting"
    game["votes"] = {}

    options = [
        player["name"]
        for player in players
    ]

    await delete_stage_messages(chat_id, context)

    message = await context.bot.send_poll(
        chat_id=chat_id,
        question="🗳️ به چه کسی شک داری؟",
        options=options,
        is_anonymous=False,
        allows_multiple_answers=False
    )
    game["stage_message_ids"] = [message.message_id]

    game["poll_id"] = message.poll.id
    game["poll_message_id"] = message.message_id

    info_message = await context.bot.send_message(
        chat_id=chat_id,
        text=(
            "📩 رأی‌گیری شروع شد!\n\n"
            "هر بازیکن فقط یک رأی می‌تواند بدهد.\n"
            "به کسی که فکر می‌کنید جاسوس است رأی بدهید."
        )
    )
    game["stage_message_ids"].append(info_message.message_id)

    asyncio.create_task(
        finish_vote_after_time(chat_id, context)
    )


async def finish_vote_after_time(chat_id, context):
    await asyncio.sleep(60)

    game = games.get(chat_id)

    if not game:
        return

    if game.get("status") != "voting":
        return

    try:
        await context.bot.stop_poll(
            chat_id=chat_id,
            message_id=game["poll_message_id"]
        )
    except Exception:
        pass

    await calculate_result(chat_id, context)


# =========================
# دریافت رأی بازیکنان
# =========================

async def receive_vote(update, context):
    poll_answer = update.poll_answer

    user_id = poll_answer.user.id

    # اگر کاربر رأی خودش را پاک کرده باشد
    if not poll_answer.option_ids:
        for chat_id, game in games.items():
            if game.get("poll_id") == poll_answer.poll_id:
                game["votes"].pop(user_id, None)
                return

    option_id = poll_answer.option_ids[0]

    for chat_id, game in games.items():

        if game.get("poll_id") != poll_answer.poll_id:
            continue

        players = game["players"]

        # فقط بازیکنان بازی اجازه رأی دارند
        if not any(player["user_id"] == user_id for player in players):
            return

        game["votes"][user_id] = option_id

        # اگر همه رأی داده باشند، رأی‌گیری زودتر تمام شود
        if len(game["votes"]) == len(players):

            try:
                await context.bot.stop_poll(
                    chat_id=chat_id,
                    message_id=game["poll_message_id"]
                )
            except Exception:
                pass

            await calculate_result(chat_id, context)

        return
    # =========================
# محاسبه نتیجه رأی‌گیری
# =========================

async def calculate_result(chat_id, context):
    game = games.get(chat_id)

    if not game:
        return

    players = game["players"]
    votes = game.get("votes", {})

    # اگر هیچ‌کس رأی نداده باشد
    if not votes:
        game["status"] = "finished"

        await context.bot.send_message(
            chat_id=chat_id,
            text="🗳️ هیچ‌کس رأی نداد!\n\n"
                 "🕵️ جاسوس برنده شد!"
        )
        return

    # شمارش رأی‌ها
    vote_count = {}

    for option_id in votes.values():
        vote_count[option_id] = vote_count.get(option_id, 0) + 1

    max_votes = max(vote_count.values())

    winners = [
        option_id
        for option_id, count in vote_count.items()
        if count == max_votes
    ]

    # اگر رأی‌ها مساوی نباشند
    if len(winners) == 1:
        selected_index = winners[0]
        selected_player = players[selected_index]

        await finish_game( # type: ignore
            chat_id,
            selected_player,
            context
        )
        return

    # اگر چند نفر بیشترین رأی مساوی داشته باشند
    tied_players = [
        players[option_id]
        for option_id in winners
        if option_id < len(players)
    ]

    game["tied_players"] = tied_players
    game["status"] = "defense"

    names = "\n".join(
        f"👤 {player['name']}"
        for player in tied_players
    )

    await context.bot.send_message(
        chat_id=chat_id,
        text="⚖️ رأی‌ها مساوی شد!\n\n"
             f"{names}\n\n"
             "🗣️ بازیکنان مساوی باید از خودشان دفاع کنند.\n"
             "⏱️ ۱ دقیقه فرصت دفاع دارید."
    )

    await asyncio.sleep(60)

    await start_final_vote(chat_id, context)
    return


# =========================
# رأی‌گیری نهایی
# =========================

async def start_final_vote(
    chat_id,
    context: ContextTypes.DEFAULT_TYPE
):

    game = games.get(chat_id)

    if not game:
        return

    tied_players = game.get("tied_players", [])

    if len(tied_players) < 2:
        return

    game["status"] = "final_voting"
    game["final_votes"] = {}

    options = [
        player["name"]
        for player in tied_players
    ]

    await delete_stage_messages(chat_id, context)

    message = await context.bot.send_poll(
        chat_id=chat_id,
        question="🗳️ رأی نهایی",
        options=options,
        is_anonymous=False,
        allows_multiple_answers=False
    )
    game["stage_message_ids"] = [message.message_id]

    game["final_poll_id"] = message.poll.id
    game["final_poll_message_id"] = message.message_id

    info_message = await context.bot.send_message(
        chat_id=chat_id,
        text=(
            "🗳️ رأی‌گیری نهایی شروع شد!\n\n"
            "فقط بازیکن‌هایی که در رأی قبلی مساوی نبودند "
            "می‌توانند رأی بدهند.\n\n"
            "هر نفر فقط یک رأی دارد."
        )
    )
    game["stage_message_ids"].append(info_message.message_id)


async def finish_final_vote_after_time(chat_id, context):
    await asyncio.sleep(60)

    game = games.get(chat_id)

    if not game:
        return

    if game.get("status") != "final_voting":
        return

    try:
        await context.bot.stop_poll(
            chat_id=chat_id,
            message_id=game["final_poll_message_id"]
        )
    except Exception:
        pass

    await calculate_final_result(chat_id, context)


# =========================
# دریافت رأی نهایی
# =========================

async def receive_final_vote(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    poll_answer = update.poll_answer

    user_id = poll_answer.user.id
    option_id = poll_answer.option_ids[0]

    for chat_id, game in games.items():

        if game.get("final_poll_id") != poll_answer.poll_id:
            continue

        tied_players = game.get("tied_players", [])

        # فقط بازیکن‌های مجاز می‌توانند رأی بدهند
        allowed_voters = [
            player["user_id"]
            for player in game["players"]
            if player not in tied_players
        ]

        if user_id not in allowed_voters:
            return

        game["final_votes"][user_id] = option_id

        # وقتی همه افراد مجاز رأی دادند
        if len(game["final_votes"]) == len(allowed_voters):

            await context.bot.stop_poll(
                chat_id=chat_id,
                message_id=game["final_poll_message_id"]
            )

            await calculate_final_result(
                chat_id,
                context
            )

        return


# =========================
# محاسبه رأی نهایی
# =========================

async def calculate_final_result(
    chat_id,
    context: ContextTypes.DEFAULT_TYPE
):

    game = games.get(chat_id)

    if not game:
        return

    tied_players = game.get("tied_players", [])
    final_votes = game.get("final_votes", {})

    vote_count = {}

    for option_id in final_votes.values():

        vote_count[option_id] = (
            vote_count.get(option_id, 0) + 1
        )

    max_votes = max(vote_count.values())

    winners = [
        option_id
        for option_id, count in vote_count.items()
        if count == max_votes
    ]

    # اگر رأی نهایی هم مساوی شد
    if len(winners) > 1:

        await context.bot.send_message(
            chat_id=chat_id,
            text=(
                "⚖️ رأی نهایی هم مساوی شد!\n\n"
                "🕵️ جاسوس برنده شد!"
            )
        )

        game["status"] = "finished"
        return

    selected_index = winners[0]

    selected_player = tied_players[selected_index]

    await finish_game(
        chat_id,
        selected_player,
        context
    )
    
async def finish_game(chat_id, selected_player, context):
    game = games.get(chat_id)

    if not game:
        return

    await delete_stage_messages(chat_id, context)

    role_message_id = game.get("role_message_id")
    if role_message_id:
        try:
            await context.bot.delete_message(
                chat_id=chat_id,
                message_id=role_message_id
            )
        except Exception:
            pass
        game["role_message_id"] = None

    spy_id = game["spy_id"]
    secret_word = game["secret_word"]

    if selected_player["user_id"] == spy_id:
        result = (
            "🎉 شهروندها برنده شدند!\n\n"
            f"🕵️ جاسوس: {selected_player['name']}\n"
            f"🔑 کلمه مخفی: {secret_word}"
        )
    else:
        spy_player = next(
            player for player in game["players"]
            if player["user_id"] == spy_id
        )

        result = (
            "🕵️ جاسوس برنده شد!\n\n"
            f"👤 بازیکنی که اشتباه انتخاب شد: {selected_player['name']}\n"
            f"🕵️ جاسوس واقعی: {spy_player['name']}\n"
            f"🔑 کلمه مخفی: {secret_word}"
        )

    game["status"] = "finished"

    await context.bot.send_message(
        chat_id=chat_id,
        text=f"🏁 بازی تمام شد!\n\n{result}"
    )
    # =========================
# اتصال دکمه‌ها
# =========================

app = Application.builder().token(BOT_TOKEN).build()

app.add_handler(
    CommandHandler("start", start)
)

app.add_handler(
    CallbackQueryHandler(
        start_game,
        pattern="^start_game$"
    )
)

app.add_handler(
    CallbackQueryHandler(
        select_players,
        pattern="^players_"
    )
)

app.add_handler(
    CallbackQueryHandler(
        join_game,
        pattern="^join_game$"
    )
)

app.add_handler(
    CallbackQueryHandler(
        launch_game,
        pattern="^launch_game$"
    )
)

app.add_handler(
    MessageHandler(
        filters.TEXT & ~filters.COMMAND,
        get_player_name
    )
)
app.add_handler(CallbackQueryHandler(show_role, pattern="^show_role$"))

app.add_handler(PollAnswerHandler(receive_vote))

app.add_handler(PollAnswerHandler(receive_final_vote))

print("Bot is running...")

app.run_polling()

# test githup