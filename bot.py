import asyncio
import sqlite3

from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, Command
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import (
    Message,
    CallbackQuery,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    FSInputFile
)

from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from config import BOT_TOKEN, ADMIN_ID, CHANNEL_USERNAME


bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


# =========================
# STATES
# =========================

class OrderState(StatesGroup):
    service = State()
    phone = State()
    description = State()


class SpecialistState(StatesGroup):
    phone = State()
    specialty = State()
    experience = State()

class BroadcastState(StatesGroup):
    message = State()

class ChannelPostState(StatesGroup):
    text = State()
    button_text = State()
    button_url = State()
# =========================
# MENUS
# =========================

def main_menu():

    return InlineKeyboardMarkup(
        inline_keyboard=[

            [
                InlineKeyboardButton(
                    text="🚀 Buyurtma berish",
                    callback_data="order"
                )
            ],

            [
                InlineKeyboardButton(
                    text="👨‍💻 Mutaxassis bo'lish",
                    callback_data="specialist"
                )
            ],

            [
                InlineKeyboardButton(
                    text="📂 Loyihalarimiz",
                    callback_data="portfolio"
                )
            ],

            [
                InlineKeyboardButton(
                    text="💬 Admin bilan bog'lanish",
                    callback_data="admin"
                )
            ],

            [
                InlineKeyboardButton(
                    text="🌟 Biz haqimizda",
                    callback_data="about"
                )
            ]
        ]
    )


def back_menu():

    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🔙 Asosiy menyu",
                    callback_data="home"
                )
            ]
        ]
    )


# =========================
# START
# =========================

@dp.message(CommandStart())
async def start(message: Message):

    try:
        member = await bot.get_chat_member(
            CHANNEL_USERNAME,
            message.from_user.id
        )

        if member.status in ["left", "kicked"]:

            keyboard = InlineKeyboardMarkup(
                inline_keyboard=[
                    [
                        InlineKeyboardButton(
                            text="📢 Kanalga obuna bo'lish",
                            url="https://t.me/nexoraguild"
                        )
                    ],
                    [
                        InlineKeyboardButton(
                            text="✅ Tekshirish",
                            callback_data="check_sub"
                        )
                    ]
                ]
            )

            await message.answer(
                "❌ Botdan foydalanish uchun avval kanalga obuna bo'ling.",
                reply_markup=keyboard
            )

            return

    except TelegramBadRequest:
        pass

    conn = sqlite3.connect("nexora.db")
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT OR IGNORE INTO users
        (
        tg_id,
        fullname,
        username,
        role
        )
        VALUES (?, ?, ?, ?)
        """,
        (
            message.from_user.id,
            message.from_user.full_name,
            message.from_user.username,
            "user"
        )
    )
    conn.commit()
    conn.close()

    photo = FSInputFile("logo.jpg")

    await message.answer_photo(
        photo=photo,
        caption=
        "🚀 <b>NEXORA GUILD</b>\n\n"

        "Kelajakni kutadiganlar ko'p.\n"
        "Kelajakni yaratadiganlar esa juda kam.\n\n"

        "Nexora Guild — IT, texnologiya va innovatsiya orqali "
        "yoshlarni birlashtiruvchi zamonaviy platforma.\n\n"

        "Bu yerda:\n"
        "✅ Buyurtma berishingiz\n"
        "✅ Mutaxassis bo'lishingiz\n"
        "✅ Jamoaga qo'shilishingiz\n"
        "✅ Loyihalarda ishtirok etishingiz mumkin.\n\n"

        "🔥 Kelajakni birga quramiz!",

        parse_mode="HTML",
        reply_markup=main_menu()
    )
    # =========================
# HOME
# =========================

@dp.callback_query(F.data == "home")
async def home(callback: CallbackQuery):

    await callback.message.delete()

    photo = FSInputFile("logo.jpg")

    await callback.message.answer_photo(
        photo=photo,
        caption=
        "🚀 <b>NEXORA GUILD</b>\n\n"
        "Kelajakni kutmang.\n"
        "Kelajakni yarating.\n\n"
        "Biz bilan IT olamiga qadam qo'ying.",
        parse_mode="HTML",
        reply_markup=main_menu()
    )

    await callback.answer()


# =========================
# ABOUT
# =========================

@dp.callback_query(F.data == "about")
async def about(callback: CallbackQuery):

    await callback.message.delete()

    photo = FSInputFile("about.jpg")

    await callback.message.answer_photo(
        photo=photo,
        caption=
        "🌟 <b>BIZ HAQIMIZDA</b>\n\n"

        "Nexora Guild — bu oddiy loyiha emas.\n"
        "Bu kelajakni qurishga intilayotgan yoshlar jamiyati.\n\n"

        "Bugungi dunyoda IT sohasini bilgan inson "
        "nafaqat yaxshi daromad topadi, balki "
        "butun dunyo bilan ishlash imkoniyatiga ega bo'ladi.\n\n"

        "Bizning maqsadimiz:\n"
        "🚀 Yoshlarni IT ga qiziqtirish\n"
        "🚀 Loyihalar yaratish\n"
        "🚀 Tajriba almashish\n"
        "🚀 Jamoa shakllantirish\n"
        "🚀 Kelajak liderlarini tayyorlash\n\n"

        "Nimalar qilamiz?\n"
        "🤖 Telegram botlar\n"
        "🌐 Web saytlar\n"
        "📱 Mobil ilovalar\n"
        "🎨 Dizayn xizmatlari\n"
        "🧠 Sun'iy intellekt loyihalari\n"
        "📈 Marketing va SMM\n\n"

        "Kelajakdagi rejamiz:\n"
        "🏫 O'quv markaz ochish\n"
        "📚 IT kurslar tashkil qilish\n"
        "💼 Yoshlarni ish bilan ta'minlash\n"
        "🌍 Xalqaro loyihalarda qatnashish\n\n"

        "Biz ishonamizki har bir yoshning "
        "ichida ulkan salohiyat yashiringan.\n\n"

        "🔥 Kelajakni kutmang.\n"
        "🔥 Kelajakni yarating.\n\n"

        "NEXORA GUILD — Kelajakni birga quramiz.",

        parse_mode="HTML",
        reply_markup=back_menu()
    )

    await callback.answer()


# =========================
# PORTFOLIO
# =========================

@dp.callback_query(F.data == "portfolio")
async def portfolio(callback: CallbackQuery):

    await callback.message.delete()

    photo = FSInputFile("portfolio.jpg")

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="📢 Kanalimiz",
                    url=f"https://t.me/{CHANNEL_USERNAME.replace('@','')}"
                )
            ],
            [
                InlineKeyboardButton(
                    text="🔙 Asosiy menyu",
                    callback_data="home"
                )
            ]
        ]
    )

    await callback.message.answer_photo(
        photo=photo,
        caption=
        "📂 <b>NEXORA GUILD LOYIHALARI</b>\n\n"

        "Biz quyidagi yo'nalishlarda ishlaymiz:\n\n"

        "🤖 Telegram Botlar\n"
        "🌐 Web Saytlar\n"
        "📱 Mobil Ilovalar\n"
        "🎨 Dizayn\n"
        "🛒 Online Do'konlar\n"
        "📊 CRM Tizimlar\n"
        "🧠 AI Yechimlar\n"
        "🎬 Video Montaj\n"
        "📈 SMM Xizmatlari\n\n"

        "Har bir loyiha sifat va natijaga "
        "yo'naltirilgan holda ishlab chiqiladi.",

        parse_mode="HTML",
        reply_markup=keyboard
    )

    await callback.answer()


# =========================
# ADMIN CONTACT
# =========================

@dp.callback_query(F.data == "admin")
async def admin_contact(callback: CallbackQuery):

    await callback.message.delete()

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="💬 Adminga yozish",
                    url="https://t.me/afruzelmurodov"
                )
            ],
            [
                InlineKeyboardButton(
                    text="🔙 Asosiy menyu",
                    callback_data="home"
                )
            ]
        ]
    )

    await callback.message.answer(
        "💬 <b>ADMIN BILAN BOG'LANISH</b>\n\n"

        "Savollaringiz bormi?\n"
        "Loyiha buyurtma qilmoqchimisiz?\n"
        "Hamkorlik taklifingiz bormi?\n"
        "Jamoaga qo'shilmoqchimisiz?\n\n"

        "Admin sizga quyidagilar bo'yicha yordam beradi:\n\n"

        "✅ Buyurtmalar\n"
        "✅ Hamkorlik\n"
        "✅ IT maslahatlar\n"
        "✅ Jamoaga qo'shilish\n"
        "✅ Kurslar haqida ma'lumot\n"
        "✅ Texnik yordam\n\n"

        "🕒 Ish vaqti:\n"
        "09:00 — 22:00\n\n"

        "Odatda barcha murojaatlarga imkon qadar tez javob beriladi.",

        parse_mode="HTML",
        reply_markup=keyboard
    )

    await callback.answer()
    # =========================
# ORDER
# =========================

@dp.callback_query(F.data == "order")
async def order_start(callback: CallbackQuery, state: FSMContext):

    await callback.message.delete()

    await state.set_state(OrderState.service)

    await callback.message.answer(
        "🚀 Buyurtma berish\n\n"
        "Kerakli xizmat turini yozing.\n\n"
        "Misol:\n"
        "🤖 Telegram bot\n"
        "🌐 Web sayt\n"
        "📱 Mobil ilova\n"
        "🎨 Dizayn\n"
        "🧠 AI loyiha"
    )

    await callback.answer()


@dp.message(OrderState.service)
async def order_service(message: Message, state: FSMContext):

    await state.update_data(service=message.text)

    await state.set_state(OrderState.phone)

    await message.answer(
        "📞 Telefon raqamingizni yuboring."
    )


@dp.message(OrderState.phone)
async def order_phone(message: Message, state: FSMContext):

    await state.update_data(phone=message.text)

    await state.set_state(OrderState.description)

    await message.answer(
        "📝 Loyihangiz haqida batafsil yozing."
    )


@dp.message(OrderState.description)
async def order_description(message: Message, state: FSMContext):

    data = await state.get_data()

    conn = sqlite3.connect("nexora.db")
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO orders
        (
        client_id,
        service,
        phone,
        description
        )
        VALUES (?, ?, ?, ?)
        """,
        (
            message.from_user.id,
            data["service"],
            data["phone"],
            message.text
        )
    )

    order_id = cursor.lastrowid

    conn.commit()
    conn.close()

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="✅ Qabul qilish",
                    callback_data=f"accept_{order_id}"
                ),
                InlineKeyboardButton(
                    text="❌ Bekor qilish",
                    callback_data=f"reject_{order_id}"
                )
            ]
        ]
    )

    await bot.send_message(
        ADMIN_ID,
        f"📦 YANGI BUYURTMA\n\n"
        f"🆔 Buyurtma ID: {order_id}\n\n"
        f"👤 {message.from_user.full_name}\n"
        f"🆔 Telegram ID: {message.from_user.id}\n\n"
        f"🛠 Xizmat: {data['service']}\n"
        f"📞 Telefon: {data['phone']}\n"
        f"📝 Tavsif:\n{message.text}",
        reply_markup=keyboard
    )

    await message.answer(
        "✅ Buyurtmangiz yuborildi.\n\n"
        "Admin ko'rib chiqmoqda.",
        reply_markup=main_menu()
    )

    await state.clear()


# =========================
# SPECIALIST
# =========================

@dp.callback_query(F.data == "specialist")
async def specialist_start(callback: CallbackQuery, state: FSMContext):

    await callback.message.delete()

    await state.set_state(SpecialistState.phone)

    await callback.message.answer(
        "👨‍💻 Mutaxassis bo'lish\n\n"
        "Telefon raqamingizni yuboring."
    )

    await callback.answer()


@dp.message(SpecialistState.phone)
async def specialist_phone(message: Message, state: FSMContext):

    await state.update_data(phone=message.text)

    await state.set_state(SpecialistState.specialty)

    await message.answer(
        "💻 Yo'nalishingizni yozing.\n\n"
        "Misol:\n"
        "Python\n"
        "Frontend\n"
        "Backend\n"
        "UI/UX\n"
        "Graphic Design"
    )


@dp.message(SpecialistState.specialty)
async def specialist_specialty(message: Message, state: FSMContext):

    await state.update_data(specialty=message.text)

    await state.set_state(SpecialistState.experience)

    await message.answer(
        "📚 Tajribangiz haqida yozing."
    )


@dp.message(SpecialistState.experience)
async def specialist_experience(message: Message, state: FSMContext):

    data = await state.get_data()

    conn = sqlite3.connect("nexora.db")
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT OR REPLACE INTO specialists
        (
        tg_id,
        fullname,
        username,
        phone,
        specialty,
        experience
        )
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            message.from_user.id,
            message.from_user.full_name,
            message.from_user.username,
            data["phone"],
            data["specialty"],
            message.text
        )
    )

    specialist_id = message.from_user.id

    conn.commit()
    conn.close()

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="✅ Tasdiqlash",
                    callback_data=f"spec_accept_{specialist_id}"
                ),
                InlineKeyboardButton(
                    text="❌ Rad etish",
                    callback_data=f"spec_reject_{specialist_id}"
                )
            ]
        ]
    )

    await bot.send_message(
        ADMIN_ID,
        f"👨‍💻 YANGI MUTAXASSIS\n\n"
        f"👤 {message.from_user.full_name}\n"
        f"🆔 {message.from_user.id}\n"
        f"📞 {data['phone']}\n"
        f"💻 {data['specialty']}\n\n"
        f"📚 Tajriba:\n{message.text}",
        reply_markup=keyboard
    )

    await message.answer(
        "🎉 Arizangiz yuborildi.\n\n"
        "Admin ko'rib chiqmoqda.",
        reply_markup=main_menu()
    )

    await state.clear()
# =========================
# ADMIN PANEL
# =========================

@dp.message(Command("admin"))
async def admin_panel(message: Message):

    if message.from_user.id != ADMIN_ID:
        return

    conn = sqlite3.connect("nexora.db")
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM users")
    users = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM specialists")
    specialists = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM orders")
    orders = cursor.fetchone()[0]

    conn.close()

    await message.answer(
        f"👑 NEXORA ADMIN PANEL\n\n"
        f"👥 Foydalanuvchilar: {users}\n"
        f"👨‍💻 Mutaxassislar: {specialists}\n"
        f"📦 Buyurtmalar: {orders}"
    )# =========================
# USERS
# =========================

@dp.message(Command("users"))
async def users_count(message: Message):

    if message.from_user.id != ADMIN_ID:
        return

    conn = sqlite3.connect("nexora.db")
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM users")
    count = cursor.fetchone()[0]

    conn.close()

    await message.answer(
        f"👥 Foydalanuvchilar soni: {count}"
    )


# =========================
# SPECIALISTS
# =========================

@dp.message(Command("specialists"))
async def specialists_count(message: Message):

    if message.from_user.id != ADMIN_ID:
        return

    conn = sqlite3.connect("nexora.db")
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM specialists")
    count = cursor.fetchone()[0]

    conn.close()

    await message.answer(
        f"👨‍💻 Mutaxassislar soni: {count}"
    )


# =========================
# ORDERS
# =========================

@dp.message(Command("orders"))
async def orders_list(message: Message):

    if message.from_user.id != ADMIN_ID:
        return

    conn = sqlite3.connect("nexora.db")
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT id, service, description
        FROM orders
        ORDER BY id DESC
        LIMIT 20
        """
    )

    orders = cursor.fetchall()

    conn.close()

    if not orders:
        await message.answer("📦 Buyurtmalar topilmadi.")
        return

    text = "📦 OXIRGI BUYURTMALAR\n\n"

    for order in orders:
        text += (
            f"🆔 #{order[0]}\n"
            f"🛠 Xizmat: {order[1]}\n"
            f"📝 {order[2][:100]}\n\n"
        )

    await message.answer(text)


# =========================
# BROADCAST
# =========================

@dp.message(Command("broadcast"))
async def broadcast_start(message: Message, state: FSMContext):

    if message.from_user.id != ADMIN_ID:
        return

    await state.set_state(BroadcastState.message)

    await message.answer(
        "📢 Hammaga yubormoqchi bo'lgan xabaringizni yozing."
    )


@dp.message(BroadcastState.message)
async def broadcast_send(message: Message, state: FSMContext):

    if message.from_user.id != ADMIN_ID:
        return

    conn = sqlite3.connect("nexora.db")
    cursor = conn.cursor()

    cursor.execute("SELECT tg_id FROM users")
    users = cursor.fetchall()

    conn.close()

    sent = 0
    failed = 0

    for user in users:
        try:
            await bot.send_message(
                user[0],
                message.text
            )
            sent += 1
        except:
            failed += 1

    await message.answer(
        f"✅ Xabar yuborish yakunlandi.\n\n"
        f"📨 Yuborildi: {sent}\n"
        f"❌ Yuborilmadi: {failed}"
    )

    await state.clear()


# =========================
# HELP ADMIN
# =========================

@dp.message(Command("helpadmin"))
async def helpadmin(message: Message):

    if message.from_user.id != ADMIN_ID:
        return

    await message.answer(
    "👑 NEXORA ADMIN BUYRUQLARI\n\n"

    "/admin - Umumiy statistika\n"
    
    "/users - Foydalanuvchilar soni\n"

    "/specialists - Mutaxassislar soni\n"

    "/orders - Oxirgi buyurtmalar\n"

    "/broadcast - Hammaga xabar yuborish\n"

    "/addadmin - Admin qo'shish\n"

    "/removeadmin - Admin o'chirish\n"

    "/admins - Adminlar ro'yxati\n"

    "/helpadmin - Admin yordam menyusi\n"

    "/channelpost - Kanalga post yuborish\n"
)
    
    # =========================
# ACCEPT ORDER
# =========================

@dp.callback_query(F.data.startswith("accept_"))
async def accept_order(callback: CallbackQuery):

    order_id = int(callback.data.split("_")[1])

    conn = sqlite3.connect("nexora.db")
    cursor = conn.cursor()

    cursor.execute(
        "SELECT client_id FROM orders WHERE id=?",
        (order_id,)
    )

    result = cursor.fetchone()

    cursor.execute(
        "UPDATE orders SET status='accepted' WHERE id=?",
        (order_id,)
    )

    conn.commit()
    conn.close()

    if result:
        await bot.send_message(
            result[0],
            "🎉 Buyurtmangiz qabul qilindi!\n\nTez orada siz bilan bog'lanamiz."
        )

    await callback.message.edit_text(
        f"✅ Buyurtma #{order_id} qabul qilindi."
    )

    await callback.answer()


# =========================
# REJECT ORDER
# =========================

@dp.callback_query(F.data.startswith("reject_"))
async def reject_order(callback: CallbackQuery):

    order_id = int(callback.data.split("_")[1])

    conn = sqlite3.connect("nexora.db")
    cursor = conn.cursor()

    cursor.execute(
        "SELECT client_id FROM orders WHERE id=?",
        (order_id,)
    )

    result = cursor.fetchone()

    cursor.execute(
        "UPDATE orders SET status='rejected' WHERE id=?",
        (order_id,)
    )

    conn.commit()
    conn.close()

    if result:
        await bot.send_message(
            result[0],
            "❌ Buyurtmangiz hozircha qabul qilinmadi."
        )

    await callback.message.edit_text(
        f"❌ Buyurtma #{order_id} bekor qilindi."
    )

    await callback.answer()
    # =========================
# ACCEPT SPECIALIST
# =========================

@dp.callback_query(F.data.startswith("spec_accept_"))
async def specialist_accept(callback: CallbackQuery):

    tg_id = int(callback.data.split("_")[2])

    await bot.send_message(
        tg_id,
        "🎉 Tabriklaymiz!\n\n"
        "Siz Nexora Guild mutaxassisi sifatida qabul qilindingiz."
    )

    await callback.message.edit_text(
        "✅ Mutaxassis tasdiqlandi."
    )

    await callback.answer()


# =========================
# REJECT SPECIALIST
# =========================

@dp.callback_query(F.data.startswith("spec_reject_"))
async def specialist_reject(callback: CallbackQuery):

    tg_id = int(callback.data.split("_")[2])

    await bot.send_message(
        tg_id,
        "❌ Afsuski, arizangiz hozircha tasdiqlanmadi."
    )

    await callback.message.edit_text(
        "❌ Mutaxassis rad etildi."
    )

    await callback.answer()
# =========================
# ADD ADMIN
# =========================

@dp.message(Command("addadmin"))
async def add_admin(message: Message):

    if message.from_user.id != ADMIN_ID:
        return

    try:
        new_admin = int(message.text.split()[1])

        conn = sqlite3.connect("nexora.db")
        cursor = conn.cursor()

        cursor.execute(
            "INSERT OR IGNORE INTO admins (tg_id) VALUES (?)",
            (new_admin,)
        )

        conn.commit()
        conn.close()

        await message.answer(
            f"✅ Admin qo'shildi:\n{new_admin}"
        )

    except:
        await message.answer(
            "❌ Format:\n/addadmin USER_ID"
        )


# =========================
# REMOVE ADMIN
# =========================

@dp.message(Command("removeadmin"))
async def remove_admin(message: Message):

    if message.from_user.id != ADMIN_ID:
        return

    try:
        admin_id = int(message.text.split()[1])

        conn = sqlite3.connect("nexora.db")
        cursor = conn.cursor()

        cursor.execute(
            "DELETE FROM admins WHERE tg_id=?",
            (admin_id,)
        )

        conn.commit()
        conn.close()

        await message.answer(
            f"❌ Admin o'chirildi:\n{admin_id}"
        )

    except:
        await message.answer(
            "❌ Format:\n/removeadmin USER_ID"
        )


# =========================
# ADMINS LIST
# =========================

@dp.message(Command("admins"))
async def admins_list(message: Message):

    if message.from_user.id != ADMIN_ID:
        return

    conn = sqlite3.connect("nexora.db")
    cursor = conn.cursor()

    cursor.execute("SELECT tg_id FROM admins")
    admins = cursor.fetchall()

    conn.close()

    text = "👑 NEXORA ADMINLARI\n\n"
    text += f"⭐ Asosiy admin: {ADMIN_ID}\n\n"

    for admin in admins:
        text += f"➕ {admin[0]}\n"

    await message.answer(text)

    # =========================
# CHANNEL POST
# =========================

@dp.message(Command("channelpost"))
async def channel_post_start(message: Message, state: FSMContext):

    if message.from_user.id != ADMIN_ID:
        return

    await state.set_state(ChannelPostState.text)

    await message.answer(
        "📝 Kanal uchun post matnini yuboring."
    )


@dp.message(ChannelPostState.text)
async def channel_post_text(message: Message, state: FSMContext):

    await state.update_data(text=message.text)

    await state.set_state(ChannelPostState.button_text)

    await message.answer(
        "🔘 Tugma nomini yuboring."
    )


@dp.message(ChannelPostState.button_text)
async def channel_post_button(message: Message, state: FSMContext):

    await state.update_data(button_text=message.text)

    await state.set_state(ChannelPostState.button_url)

    await message.answer(
        "🔗 Tugma havolasini yuboring."
    )


@dp.message(ChannelPostState.button_url)
async def channel_post_send(message: Message, state: FSMContext):

    data = await state.get_data()

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=data["button_text"],
                    url=message.text
                )
            ]
        ]
    )

    await bot.send_message(
        chat_id="@nexoraguild",
        text=data["text"],
        reply_markup=keyboard
    )

    await message.answer(
        "✅ Post kanalga yuborildi."
    )

    await state.clear()
    

# =========================
# RUN BOT
# =========================

async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())