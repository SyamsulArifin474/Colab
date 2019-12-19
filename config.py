conf = {
    'token'			 	 : 'TOKEN TELEGRAM BOX', # token telegram bot
	'agent'				 : 'Bot Daltim', # Set User Agent
	'wilayah'			 : 'daltim', # Set Wilayah
	'bri'				 : "01199", # kode BRIVA 
	'user'				 : 'userpedatren', # user pedatren
	'pass'				 : 'password pedatren' # password pedatren
}

text_messages = {
	# set selamat datang
    'welcome':
	    u'Selamat Datang {name}!\n\n'
	    u'Bot ini untuk melayani kebutuhan Wali Santri Wilayah Al-Hasyimiyah PP. Nurul Jadid\n'
		u'Pastikan Anda Telah Register Terlebih Dahulu Dengan Cara Mamasukkan NIK (Nomor Induk Kependudukan) '
        u'Putri Anda Agar Bisa Menggunakan Fasilatas Ini.\n\n'
	    u'Ada kendala atau pertanyaan hubungi @alhasyimy',
	
	'log':
		u"<b>Time : {0}</b>\n"
		u"<b>Username :</b> @{1}\n"
		u"<b>Name :</b> {2} {3}\n"
		u"<b>ID :</b> <code>{4}</code>\n"
		u"<b>Text :</b> {5}",

    'help':
        u'{}\n'
	    u'Silahkan Klik Pilihan Dibawah\n'
	    u'jika Ada kendala atau pertanyaan silahkan menghubungi *Syafiqiyah Adhimiy* @alhasyimy',

	'informasi':
		u'*Jam Buka Tutup Interlokal*\n'
		u'21.00 - 22.00 WIB\n'
		u'Khusus Malam Selasa dan Malam Jum\'at 20.30 - 21.30\n\n'
		u'*DAFTAR NOMOR*\n'
		u'Phone : 085245325425\n'
		u'Phone : 082272739160\n'
		u'Phone : 082231107387\n'
		u'Phone : 082272739168\n\n'
		u'*Jam Pelayanan Perizinan*\n'
		u'Pagi  : 09.00 - 12.00\n'
		u'Siang : 13.00 - 16.00\n'
		u'Malam : 21.00 - 22.00\n',
		
	'absen':
	    u"NIS : {0} \n"
	    u"Nama : {1} \n"
	    u"Daerah : {2} \n"
	    u"Kamar : {3} \n"
	    u"Pendidikan : {4} \n\n"
	    u"*Absensi* \n"
	    u"Ubudiyah : {5} \n"
	    u"Pembinaan Al-Quran : {6} \n"
	    u"Kegiatan belajar : {7} \n"
	    u"Sekolah : {8} \n"
	    u"Diniyah : {9} \n"
		u"*Bulan* : {10}\n\n" 
	    u"*Catatan*\n",
	    # u"{10} \n",

	'va':
	    u"NIS : {0} \n"
	    u"Nama : {1} \n"
	    u"Daerah : {2} \n"
	    u"Kamar : {3} \n"
	    u"pendidikan : {4} \n\n"
	    u"<b>No Virtual Account</b>\n"
	    u"BRI : <code>01199{5}</code> \n\n"
		u"<b>Detail Tagihan</> \n\n",
	    # u"Jika Ada Kesalahan silahkan menghubungi Bagian Bendahara Al-Hasyimiyah <b>El-Wardha Safitri</b> 082236721652 @alhasyimiyah_DalTim",

	'send_absen':
		u"*Assalamu'alaikum*\n"
	    u"Semoga Selalu Dalam Lindungan *Allah SWT*\n"
	    u"Berikut Kami Laporkan Rekap Absensi Nanda *{1}*\n\n"
	    u"NIS : {0} \n"
	    u"Nama : {1} \n"
	    u"Daerah : {2} \n"
	    u"Kamar : {3}\n"
	    u"Pendidikan : {4}\n\n"
	    u"*Absensi*\n"
	    u"Ubudiyah : {5} \n"
	    u"Pembinaan Al-Quran : {6} \n"
	    u"Kegiatan belajar : {7} \n"
	    u"Sekolah : {8} \n"
	    u"Diniyah : {9} \n"
	    u"*Bulan* : {10} \n\n"
	    u"Jika merasa ada kesalahan, Hubungi Bagian Tahkim (Nashihatul Khoiroh) atau BK (Istianatul Hasanah) 0822234234908",

	'chat_id':
		u'NIS : {0}\n'
		u'Nama : {1}\n'
		u'Daerah : {2}\n'
		u'Kamar : {3}\n'
		u'Pendidikan : {4}\n\n'
		u'Register Berhasil',

	'cari_chatid':
		u'Akun Telegram anda belum terkait dengan sistem kami. '
		u'Silahkan klik /register agar Bot ini mengenali anda '
		u'sebagai Wali dari Peserta Didik',

	'terdaftar':
		u'Selamat\n'
		u'Anda telah terdaftar wali dari nanda {name}',

	'terisi':
		u'Mohon Maaf\n'
		u'{name} Sudah mempunya wali yang terdaftar\n'
		u'Jika ada perubahan hubungi @alhasyimiyah_DalTim',
	
	'bukti':
		u'*PENTING*\n'
		u'Harap Beri Keterangan (Caption)\n\n'
		u'Nama Lengkap\n'
		u'Daerah\n'
		u'Tagihan Untuk Bulan\n',
	
	'text':
		u"*{name}*\n"
		u"Mohon maaf kami tidak mengerti apa yang anda inginkan\n"
		u"Barangkali daftar dibawah ini bisa membantu",

	'wrong_name':
		u"Data Tidak Ditemukan, Silahkan Coba Dengan Nama Yang Lain.\n\n"
		u"Contoh Mau Mencari Nama *Faizul Amaly*.\n\n"
		u"Coba Input Nama *Zul Am / Amal / Izul / Amaly*",
}
