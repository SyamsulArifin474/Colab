# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
import telebot
import time
import re
import os
from config import text_messages, conf, tokenBot
from datetime import datetime
import flask
from werkzeug.serving import run_simple
from app import logger, views
from app.rules import *
from app.common import _insertAbsen, _insertVA, _updateVa

bot = telebot.TeleBot(tokenBot, threaded=False)

# set WebHook
WEBHOOK_HOST = '206.189.153.85' # IP VPS
WEBHOOK_PORT = 443  # 443, 80, 88 or 8443 (port need to be 'open')
WEBHOOK_LISTEN = '0.0.0.0'  # In some VPS you may need to put here the IP addr
WEBHOOK_SSL_CERT = './webhook_cert.pem'  # Path to the ssl certificate
WEBHOOK_SSL_PRIV = './webhook_pkey.pem'  # Path to the ssl private key
WEBHOOK_URL_BASE = "https://%s:%s" % (WEBHOOK_HOST, WEBHOOK_PORT)
WEBHOOK_URL_PATH = "/%s/" % (API_TOKEN)

app = flask.Flask(__name__)

@app.route('/', methods=['GET', 'HEAD'])
def index():
    return ''

@app.route(WEBHOOK_URL_PATH, methods=['POST'])
def webhook():
    if flask.request.headers.get('content-type') == 'application/json':
        json_string = flask.request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return ''
    else:
        flask.abort(403)


user = ['Faizulamaly', 'alhasyimy'] # set username telegram admin
url = 'https://api.pedatren.nuruljadid.app/' # set url api pedatren
anak = {}
admin = [329627396, 567400538] # set id admin telegram

handler = {}
tes = {
    'uuid': ''
}
temp = []
knownUsers = []
userStep = {}

# set untuk simpan log
def simpanLog(data):
    for cid in admin:
        bot.send_message(cid, data, parse_mode="HTML")

# tangkap semua yang diketikan dalam bot telegram
def listener(messages):
    for m in messages:
        if m.content_type == "text" and m.chat.id not in admin:
            a = datetime.now().strftime("%d-%m-%Y %H:%M")
            tangkap = text_messages["log"].format(
                a, m.from_user.username or "",
                m.from_user.first_name, m.from_user.last_name or "",
                m.chat.id, m.text,
            )
            simpanLog(tangkap)


bot.set_update_listener(listener)


def get_user_step(uid):
    if uid in userStep:
        return userStep[uid]
    else:
        knownUsers.append(uid)
        userStep[uid] = 0
        return 0


def tulis(cek):
    return bot.send_chat_action(cek, 'typing')


def cek_pilihan(cid, nama):
    if nama.lower() == 'lanjut':
        return 1
    else:
        bot.send_message(cid, "Sudah Kami CANCEL",
                         reply_markup=markup_remove())
        del anak[cid]
        return 0


def cek_file(m):
    tipe = m.content_type
    if tipe == 'document':
        doc = bot.get_file(m.document.file_id)
        file = bot.download_file(doc.file_path)
        nama = m.document.file_name
        with open('{}'.format(nama), 'wb') as f:
            f.write(file)
        return nama


@bot.message_handler(commands=['start', 'help'])
def send_welcome(m):
    name = m.from_user.first_name
    if hasattr(m.from_user, 'last_name') and m.from_user.last_name is not None:
        name += u" {}".format(m.from_user.last_name)

    if m.text == "/start":
        bot.send_message(m.chat.id, text_messages['welcome'].format(
            name=name), reply_markup=inlineWali())
    elif m.text == "/help":
        bot.send_message(m.chat.id, text_messages['help'].format(
            name), reply_markup=inlineWali(), parse_mode="MarkDown")


@bot.message_handler(commands=['absen', 'va'])
def prosesRequests(m):
    cid = m.chat.id
    nama = m.text
    admin = views.isAdmin(cid)
    hasil = views.isOrtu(cid)
    try:
        temps = []
        if admin:
            msg = bot.send_message(
                cid, "Masukkan Nama Santriwati", reply_markup=markup_force())
            tes[cid] = nama
            bot.register_next_step_handler(msg, forAdmin)
        elif len(hasil) > 0:
            for i in hasil:  # ikeh
                temps.append(i[0])
            anak[cid] = temps
            tes.__setitem__(cid, nama)
            if nama == '/absen' or handler.get(cid) == "/absen":
                pilih_bulan(m)
                handler[cid] = None
                return
            elif nama == '/va' or handler.get(cid) == "/va":
                cari_va(m)
                handler[cid] = None
                return
        else:
            bot.send_message(cid, text_messages['cari_chatid'])
    except Exception as e:
        bot.send_message(cid, "Mohon maaf ada kesalahan sistem")
        logger.exception(e)


def forAdmin(m):
    cid = m.chat.id
    content = views.getPerson(m.text)
    if len(content) > 0:
        msg = bot.send_message(cid, "Silahkan dipilih",
                               reply_markup=markup([i["nama"] for i in content]))
        bot.register_next_step_handler(msg, prosesAdmin)
    else:
        bot.send_message(
            cid, text_messages['wrong_name'], parse_mode="MarkDown")


def prosesAdmin(m):
    cid = m.chat.id
    nama = m.text
    anak[cid] = [nama]
    try:
        if tes[cid] == '/absen' or handler.get(cid) == '/absen':
            pilih_bulan(m)
            return
        elif tes[cid] == '/va' or handler.get(cid) == '/va':
            cari_va(m)
            return
    except Exception as e:
        logger.exception(e)
    finally:
        handler[cid] = None


def sendStatusRegister(cid, pesan):
    for id_admin in admin:
        bot.send_message(
            id_admin, "Status Register Dari <code>{}</code>\n{}".format(cid, pesan), parse_mode="HTML")


@bot.message_handler(commands=['register'])
def register(m):
    msg = bot.send_message(
        m.chat.id, "Masukkan NIK / No Passport anak anda", reply_markup=markup_force())
    bot.register_next_step_handler(msg, register_santri)


def register_santri(m):
    nik = m.text
    cek = re.compile(r'^\d{16}$|^[a-zA-Z]{2}\d{7}$')
    if cek.search(str(nik)):
        prosesRegister(m.chat.id, nik)
    else:
        bot.send_message(m.chat.id, "Masukkan NIK atau Passport dengan benar")


def prosesRegister(cid, nik):
    pesan = views.register(cid, nik)
    if pesan:
        for i in pesan:
            bot.send_message(cid, i)
            sendStatusRegister(cid, i)
    else:
        bot.send_message(cid, "Mohon maaf, data tidak ditemukan")


@bot.message_handler(regexp="^[a-zA-Z]{2}[0-9]{7}$|^[0-9]{16}$")
def handleRegex(m):
    bot.send_message(
        m.chat.id, "Anda telah menginputkan NIK/PASSPORT : {}\nMohon ditunggu akan kami cek".format(m.text))
    pesans = views.register(m.chat.id, m.text)
    if pesans:
        for i in pesans:
            bot.send_message(m.chat.id, i)
            sendStatusRegister(m.chat.id, i)
    else:
        bot.send_message(m.chat.id, "Mohon maaf, data tidak ditemukan")


def pilih_bulan(m):
    hasil = views.pilih_bulan()
    msg = bot.send_message(m.chat.id, "Silahkan Pilih Bulan",
                           reply_markup=markup([i for i in hasil]))
    bot.register_next_step_handler(msg, absen)


def absen(m):
    cid = m.chat.id
    bulan = m.text
    pesan = views.absen(data=anak[cid], bulan=bulan)
    for i in pesan:
        tulis(cid)
        bot.send_message(cid, i, parse_mode="MarkDown",
                         reply_markup=markup_remove())
    del anak[cid]


def cari_va(m):
    cid = m.chat.id
    pesan = views.virtual(data=anak[cid])
    for i in pesan:
        tulis(cid)
        bot.send_message(cid, i, parse_mode="HTML",
                         reply_markup=markup_remove())
    del anak[cid]

# Kirim Bukti Transfer


@bot.message_handler(commands=['bukti'])
def uploadBukti(m):
    tes[m.chat.id] = m.text
    bot.send_message(m.chat.id, text_messages['bukti'], parse_mode="MarkDown")
    msg = bot.send_message(
        m.chat.id, "Silahkan Kirim Bukti Transfer Berupa Photo", reply_markup=markup_force())
    bot.register_next_step_handler(msg, forwardBukti)


def forwardBukti(m):
    if m.content_type == 'photo':
        # Forward Message To Daltim
        bot.forward_message(372628748, m.chat.id, m.message_id)
        logger.info("Transfer By {} ".format(m.chat.id))
        bot.send_message(
            m.chat.id, "Terimakasih\nBukti Transfer Sudah kami terima")
    else:
        bot.send_message(
            m.chat.id, "Mohon Maaf kami tolak, Silahkan kirim Bukti Berupa Gambar")

# Infor Nomor DLL


def daftarInfo(m):
    bot.send_message(m.chat.id, text_messages['informasi'],
                     parse_mode="MarkDown", reply_markup=markup_remove())


'''
Daftar Fungsi Untuk Admin
'''
# Kirim Laporan Absensi Ke Wali Santri


def kirim_absensi(m):
    num = 0
    jum = 0
    santris = views.kirim_absensi()
    bot.send_message(
        m.chat.id, "Jumlah Seharunya yang terkirim {}\nMohon Tunggu, Kami Akan Kirim Absensi".format(len(santris)))
    for i in santris:
        text = (
            text_messages["send_absen"].format(
                i.get("nis"),
                i.get("nama"),
                i.get("blok"),
                i.get("kamar"),
                i.get("lembaga"),
                i.get("ubudiyah"),
                i.get("alquran"),
                i.get("belajar"),
                i.get("sekolah"),
                i.get("diniyah"),
                i.get("bulan"),
            )
        )
        try:
            bot.send_message(i.get("chat_id"), text, parse_mode="HTML")
        except Exception as e:
            logger.exception(e)
            continue
        jum += 1
        num += 1
        if jum == 29:
            time.sleep(2)
            jum = 0
    bot.send_message(m.chat.id, "Terkirim Sebanyak : {}".format(num))

# Cek Data Pedatren / Singkronisasi


def pilih_cek(m):
    msg = bot.send_message(m.chat.id, "Masukkan Pilihan",
                           reply_markup=markup(["INPUT", "DELETE"]))
    bot.register_next_step_handler(msg, cek_data)


def cek_data(m):
    bot.send_message(m.chat.id, views.pedatren(
        m.text), reply_markup=markup_remove())

# Insert Absen, Insert Virtual, Update Virtual


def sendExcel(m):
    msg = bot.send_message(m.chat.id, "Kirim File Excelnya Mbak :)")
    bot.register_next_step_handler(msg, getExcel)


def getExcel(m):
    tipe = m.content_type
    cid = m.chat.id
    try:
        if tipe == 'document':
            doc = bot.get_file(m.document.file_id)
            file = bot.download_file(doc.file_path)
            nama = m.document.file_name
            with open('{}'.format(nama), 'wb') as f:
                f.write(file)
            if tes[cid] == '/insertabsen':
                logger.info(tes[cid])
                pesan = _insertAbsen(nama)
                bot.send_message(m.chat.id, pesan)
            elif tes[cid] == '/insertva':
                pesan = _insertVA(nama)
                bot.send_message(m.chat.id, pesan)
            elif tes[cid] == '/updateva':
                pesan = _updateVa(nama)
                bot.send_message(m.chat.id, pesan)
    except Exception as e:
        logger.exception(e)

# REKAP VA


def rekapVADaerah(m):
    markup1 = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True)
    markup1.add("ALL")
    wilayah = views.filter()
    for i in wilayah:
        markup1.add(i["blok"])
    msg = bot.send_message(
        m.chat.id, "Silahkan Pilih Daerah", reply_markup=markup1)
    bot.register_next_step_handler(msg, prosesRekapVaDaerah)


def prosesRekapVaDaerah(m):
    cid = m.chat.id
    wilayah = views.filter()
    pilih = None
    for i in wilayah:
        if i["blok"] == m.text:
            pilih = i["id_blok"]
    try:
        bot.send_message(
            cid, "Dimengerti!\n\nSilahkan tunggu sambil lalu ngopi. Akan kami racik Datanya", reply_markup=markup_remove())
        views.rekap_virtual(cid, daerah=pilih)
        with open('{}.xlsx'.format(cid), 'rb') as f:
            bot.send_document(cid, f)
        os.remove("{}.xlsx".format(cid))

    except Exception as e:
        logger.exception(e)
        bot.send_message(cid, "Mohon Maaf Ada Error. Kwkwkw",
                         reply_markup=markup_remove())


def rekapVALembaga(m):
    markup1 = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True)
    markup1.add("ALL")
    wilayah = views.filter("lembaga")
    for i in wilayah:
        markup1.add(i["lembaga"])
    msg = bot.send_message(
        m.chat.id, "Silahkan Pilih Lembaga", reply_markup=markup1)
    bot.register_next_step_handler(msg, prosesRekapVALembaga)


def prosesRekapVALembaga(m):
    cid = m.chat.id
    lembaga = views.filter("lembaga")
    pilih = None
    for i in lembaga:
        if i["lembaga"] == m.text:
            pilih = i["alias_lembaga"]
    try:
        bot.send_message(
            cid, "Dimengerti!\n\nSilahkan tunggu sambil lalu ngopi. Akan kami racik Datanya", reply_markup=markup_remove())
        views.rekap_virtual(cid, lembaga=pilih)
        with open('{}.xlsx'.format(cid), 'rb') as f:
            bot.send_document(cid, f)
        os.remove("{}.xlsx".format(cid))

    except Exception as e:
        logger.exception(e)
        bot.send_message(cid, "Mohon Maaf Ada Error. Kwkwkw",
                         reply_markup=markup_remove())

# Cek yang tidak memiliki BRIVA


def gakPunyaBRIVA(m):
    views.gakPunyaVA(m.chat.id)
    try:
        with open("{}.xlsx".format(m.chat.id), "rb") as f:
            bot.send_document(m.chat.id, f)
            os.remove("{}.xlsx".format(m.chat.id))
    except Exception as e:
        logger.exception(e)
        bot.send_message(
            m.chat.id, "Mohon maaf Gesss Error. kwkwkwk", reply_markup=markup_remove())

# Reset Chat ID Register


def resetChat(m):
    msg = bot.send_message(
        m.chat.id, "Masukkan NIK Santriwati yang mau di Reset", reply_markup=markup_force())
    bot.register_next_step_handler(msg, prosesReset)


def prosesReset(m):
    id_reset = m.text
    nik = re.compile(r'^[0-9]{16}$|^[a-zA-Z]{2}[0-9]{7}$')
    if nik.search(id_reset):
        views.resetID(id_reset)
        bot.send_message(m.chat.id, "Sudah di Reset")
        logger.info("Reset By {} at {}".format(m.chat.id, id_reset))
    else:
        bot.send_message(m.chat.id, "Masukkan NIK/PASSPORT Dengan Benar!")

# Jumlah Yang Sudah Register


def jumlahRegister(m):
    bot.send_message(m.chat.id, views.jumlahRegister(),
                     reply_markup=markup_remove())

# Balas Pesan


def inputChatId(m):
    msg = bot.send_message(
        m.chat.id, "Masukkan ID Telegram", reply_markup=markup_force())
    bot.register_next_step_handler(msg, inputPesan)


def inputPesan(m):
    cek = re.compile(r'^[0-9]{9}$')
    if cek.search(str(m.text)):
        tes.__setitem__('id_telegram', m.text)
        msg = bot.send_message(
            m.chat.id, "Masukkan pesan yang akan disampaikan", reply_markup=markup_force())
        bot.register_next_step_handler(msg, balasPesan)
    else:
        bot.send_message(m.chat.id, "ID Telegram tidak Valid !",
                         reply_markup=markup_remove())


def balasPesan(m):
    try:
        pesan = m.text
        bot.send_message(tes['id_telegram'], pesan,
                         reply_markup=markup_remove())
        bot.send_message(m.chat.id, "Pesan :\n{}\n\nSudah berhasil dikirim".format(
            pesan), reply_markup=markup_remove())
    except Exception as e:
        bot.send_message(
            m.chat.id, "Pesan Gagal dikirim, pastikan yang diinput hanya text (Bukan Gambar/Document)", reply_markup=markup_remove())
        logger.exception(e)


def rekapRegister(m):
    views.rekapRegister(m.chat.id)
    try:
        with open("{}.xlsx".format(m.chat.id), "rb") as f:
            bot.send_document(m.chat.id, f)
        os.remove("{}.xlsx".format(m.chat.id))
    except Exception as e:
        logger.exception(e)
        bot.send_message(m.chat.id, "Mohon Maaf Ada Error. kwkwkkw")

# fungsi untuk menyimpan semua data santri ke json. kwkwkwk
# bisa digunakan untuk mencari nomor bisa diperlukan
def simpanJSON(m):
    views.simpanJSON(m.chat.id)
    try:
        with open("dataJSON.json", "rb") as f:
            bot.send_document(m.chat.id, f)
    except Exception as e:
        logger.exception(e)

# fungsi untuk admin, jika bukan admin akan ditolak
# admin bisa berupa administrator, pengguna atau lainnya, sesuai kondisi
@bot.message_handler(commands=['admin'])
def forAdministrator(m):
    cek_admin = views.isAdmin(m.chat.id)
    if cek_admin:
        if cek_admin[0].lower() == 'admin':
            bot.send_message(m.chat.id, "Silahkan Dipilih",
                             reply_markup=forAdminOnly())
        else:
            bot.send_message(m.chat.id, "Silahkan Dipilih",
                             reply_markup=forStaf())
    else:
        bot.send_message(m.chat.id, "Mohon Maaf, Hanya untuk Admin :)")

# fungsi untuk menangkap callback_data yang ada di app/rules.py
@bot.callback_query_handler(func=lambda call: True)
def prosesAdminOnly(c):
    cid = c.message.chat.id
    data = c.data
    if data == 'absensi':
        handler[cid] = "/absen"
        prosesRequests(c.message)
    elif data == 'virtual':
        handler[cid] = "/va"
        prosesRequests(c.message)
    elif data == 'register':
        handler[cid] = "/register"
        register(c.message)
    elif data == 'bukti':
        uploadBukti(c.message)
    elif data == 'informasi':
        daftarInfo(c.message)
    elif data == 'hubungi':
        bot.edit_message_text("Silahkan dipilih", cid,
                              c.message.message_id, reply_markup=inlineHubungi())
    elif data == 'admin_kirim':
        kirim_absensi(c.message)
    elif data == 'admin_balas':
        inputChatId(c.message)
    elif data == 'admin_cek':
        pilih_cek(c.message)
    elif data == 'admin_jum':
        jumlahRegister(c.message)
    elif data == 'admin_reset':
        resetChat(c.message)
    elif data == 'admin_rekap_regis':
        rekapRegister(c.message)
    elif data == 'admin_update_va':
        tes.__setitem__(cid, "/updateva")
        sendExcel(c.message)
    elif data == 'admin_insert_absen':
        tes.__setitem__(cid, "/insertabsen")
        sendExcel(c.message)
    elif data == 'admin_inser_va':
        tes.__setitem__(cid, "/insertva")
        sendExcel(c.message)
    elif data == "admin_rekap_va_lembaga":
        rekapVALembaga(c.message)
    elif data == "admin_rekap_va_daerah":
        rekapVADaerah(c.message)
    elif data == "admin_cekBRIVA":
        gakPunyaBRIVA(c.message)
    elif data == "admin_simpanJSON":
        simpanJSON(c.message)
    else:
        bot.send_message(cid, "Pilihan Tidak Dalam Daftar",
                         reply_markup=markup_remove())

# set apa yang diketikkan oleh pengguna bot, dan tampilkan Markup
@bot.message_handler(func=lambda message: True, content_types=["text"])
def handleAllMessage(m):
    nama = m.chat.first_name
    bot.send_message(m.chat.id, text_messages['text'].format(
        name=nama), parse_mode="MarkDown", reply_markup=inlineWali())


bot.remove_webhook()

time.sleep(0.1)

bot.set_webhook(url=WEBHOOK_URL_BASE+WEBHOOK_URL_PATH,
                certificate=open(WEBHOOK_SSL_CERT, 'r'))

if __name__ == '__main__':
    run_simple(WEBHOOK_LISTEN,
               WEBHOOK_PORT,
               app,
               use_reloader=True,
               ssl_context=(WEBHOOK_SSL_CERT, WEBHOOK_SSL_PRIV),
               use_debugger=True,
               use_evalex=True
               )
