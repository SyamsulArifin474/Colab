from telebot import types


def inlineWali():
    markup = types.InlineKeyboardMarkup()
    markup.row(
        types.InlineKeyboardButton("Absensi", callback_data="absensi"),
        types.InlineKeyboardButton("Register", callback_data="register"),
    )
    markup.row(
        types.InlineKeyboardButton("Virtual Account", callback_data="virtual"),
    )
    markup.row(
        types.InlineKeyboardButton(
            "Kirim Bukti Transfer", callback_data="bukti"),
        types.InlineKeyboardButton("Informasi", callback_data="informasi"),
    )
    markup.row(
        types.InlineKeyboardButton("Hubungi Kami", callback_data="hubungi"),
    )
    return markup


def inlineHubungi():
    markup = types.InlineKeyboardMarkup()
    markup.row(
        types.InlineKeyboardButton("Admin Bot", url="https://t.me/alhasyimy"),
        types.InlineKeyboardButton(
            "Kantor Keamanan", url="https://t.me/Kamtib_Daltim"),
    )
    markup.row(
        types.InlineKeyboardButton(
            "Kantor Pesantren", url="https://t.me/alhasyimiyah_DalTim"),
    )
    return markup


def forAdminOnly():
    markup = types.InlineKeyboardMarkup()
    markup.row(
        types.InlineKeyboardButton("Cek Data", callback_data="admin_cek"),
        types.InlineKeyboardButton("Jum. Register", callback_data="admin_jum"),
    )
    markup.row(
        types.InlineKeyboardButton("Balas Pesan", callback_data="admin_balas"),
        types.InlineKeyboardButton("Kirim Absen", callback_data="admin_kirim"),
        types.InlineKeyboardButton(
            "Rekap. Regis", callback_data="admin_rekap_regis"),
    )
    markup.row(
        types.InlineKeyboardButton(
            "Update Virtual", callback_data="admin_update_va"),
        types.InlineKeyboardButton(
            "Insert Absen", callback_data="admin_insert_absen"),
    )
    markup.row(
        types.InlineKeyboardButton(
            "Reset Register", callback_data="admin_reset"),
        types.InlineKeyboardButton(
            "Insert Virtual", callback_data="admin_insert_va"),
    )
    markup.row(
        types.InlineKeyboardButton(
            "Rekap VA Daerah", callback_data="admin_rekap_va_daerah"),
        types.InlineKeyboardButton(
            "Rekap VA Lembaga", callback_data="admin_rekap_va_lembaga"),
    )
    markup.row(
        types.InlineKeyboardButton(
            "Tidak Punya BRIVA", callback_data="admin_cekBRIVA"),
        types.InlineKeyboardButton(
            "Simpan JSON", callback_data="admin_simpanJSON"),
    )
    return markup


def forStaf():
    markup = types.InlineKeyboardMarkup()
    markup.row(
        types.InlineKeyboardButton("Cek Data", callback_data="admin_cek"),
        types.InlineKeyboardButton("Jum. Register", callback_data="admin_jum"),
    )
    markup.row(
        types.InlineKeyboardButton("Balas Pesan", callback_data="admin_balas"),
        types.InlineKeyboardButton(
            "Reset Register", callback_data="admin_reset"),
    )
    return markup


def markup(data):
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    for i in data:
        markup.add(i)
    return markup


def markup_force():
    return types.ForceReply(selective=False)


def markup_remove():
    return types.ReplyKeyboardRemove(selective=False)
