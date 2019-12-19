# -*- coding: utf-8 -*-
# database handler (model layer)
import pymysql as MySQLdb
import xlrd, os
from app import logger

HOST 		= 'localhost' # set host mysql
USER 		= 'root' # set user mysql
PASS		= ''# set password mysql
DB			= 'daltim'# set nama database mysql

# list query
def _useMysql(whatToDO, kelas=False, jurusan=False, a=False):
	query = {
	'absen'			: 'SELECT chat_id, ubudiyah, alquran, belajar, sekolah, diniyah,'\
					' bulan from wilayah, absen WHERE wilayah.nik="{}" and wilayah.nik=absen.nik '\
					'and DATE_FORMAT(bulan, "%Y-%m")="{}"'.format(kelas, jurusan),
	'admin'			: 'select level from admin where chat_id="{}"'.format(kelas),
	"kirim"			: 'SELECT wilayah.nik, chat_id, ubudiyah, alquran, belajar, sekolah, diniyah,'\
					  'bulan FROM wilayah, absen WHERE chat_id is not null and wilayah.nik=absen.nik and DATE_FORMAT(bulan, "%Y-%m")="{}"'.format(kelas),
	'cek_chatid'	: 'select chat_id from wilayah where uuid="{}" and chat_id is not null'.format(kelas),
	'cari_chatid'	: 'select chat_id from wilayah where chat_id="{}"'.format(kelas),
	'cek_data'		: 'select uuid from wilayah',
	'cek_va'		: 'select nik, no_va, sisa_tagihan, bulan from va where sisa_tagihan<>0',
	'va' 			: 'select no_va, sisa_tagihan, bulan from va where nik="{}"'.format(str(kelas)),
	'insert_chatid'	: 'update wilayah set chat_id={} where uuid="{}"'.format(kelas,jurusan),
	'kirim_absen'	: 'SELECT nik, chat_id FROM wilayah WHERE chat_id is not null',
	'pilih_bulan'	: 'SELECT DATE_FORMAT(bulan, "%Y-%m") as bulan from absen GROUP BY date_format(bulan, "%Y-%m") DESC LIMIT 7',
	'input'			: 'insert into wilayah (uuid, nik, nis) values ("{}", "{}", "{}")'.format(kelas,jurusan,a),
	'del'			: 'update wilayah set aktif="T" where uuid="{}"'.format(kelas),
	'get_nik'		: 'select nik, chat_id from wilayah where chat_id="{}"'.format(kelas),
	'reset_chatid'	: 'update wilayah set chat_id=Null where nik="{}"'.format(kelas),
    'jum_register'  : 'select count(nik) as jumlah from wilayah where chat_id is not null',
    'id_terakhir'   : 'select count(id) from absen',
	'rekap_reg'     : 'select nik from wilayah where chat_id is not null',
	'gakpunyava'	: 'select nis, no_va from wilayah, va where wilayah.nik=va.nik and wilayah.aktif="Y"',

	}

	conn = MySQLdb.connect(host=HOST, user=USER, passwd=PASS, db=DB)
	try:
		cur = conn.cursor()

		if whatToDO == 'absen':
			cur.execute(query[whatToDO])
			return cur.fetchall()
		elif whatToDO == 'kirim':
			cur.execute(query[whatToDO])
			return cur.fetchall()
		elif whatToDO == 'rekap_reg':
			cur.execute(query[whatToDO])
			return cur.fetchall()
		elif whatToDO == 'admin':
			cur.execute(query[whatToDO])
			return cur.fetchone()
		elif whatToDO == "cek_va":
			cur.execute(query[whatToDO])
			return cur.fetchall()
		elif whatToDO == 'jum_register':
			cur.execute(query[whatToDO])
			return cur.fetchone()
		elif whatToDO == 'reset_chatid':
			cur.execute(query[whatToDO])
			conn.commit()
		elif whatToDO == 'va':
			cur.execute(query[whatToDO])
			return cur.fetchall()
		elif whatToDO == 'cari_chatid':
			cur.execute(query[whatToDO])
			return cur.fetchone()
		elif whatToDO == 'cek_chatid':
			cur.execute(query[whatToDO])
			return cur.fetchone()
		elif whatToDO == 'insert_chatid':
			cur.execute(query[whatToDO])
			conn.commit()
		elif whatToDO == 'kirim_absen':
			cur.execute(query[whatToDO])
			return cur.fetchall()
		elif whatToDO == 'id_terakhir':
			cur.execute(query[whatToDO])
			return cur.fetchone()
		elif whatToDO == 'pilih_bulan':
			cur.execute(query[whatToDO])
			return cur.fetchall()
		elif whatToDO == 'cek_data':
			cur.execute(query[whatToDO])
			return cur.fetchall()
		elif whatToDO == 'input':
			cur.execute(query[whatToDO])
			conn.commit()
		elif whatToDO == 'del':
			cur.execute(query[whatToDO])
			conn.commit()
		elif whatToDO == 'get_nik':
			cur.execute(query[whatToDO])
			return cur.fetchall()
		elif whatToDO == 'gakpunyava':
			cur.execute(query[whatToDO])
			return  cur.fetchall()
	except Exception as e:
		logger.exception(e)
		return e
	finally:
		cur.close()
		conn.close()

def _insertAbsen(data):
	conn = MySQLdb.connect(host=HOST,user=USER, passwd=PASS,db=DB)
	logger.info(data)
	try:
		cur = conn.cursor()
		book = xlrd.open_workbook('{}'.format(data))
		sheet = book.sheet_by_index(0)
		jum = _useMysql("id_terakhir")[0]
		no = jum + 1
		sql = 'insert into absen (id, nik, ubudiyah, alquran, belajar, sekolah, diniyah, bulan) values (%s,%s,%s,%s,%s,%s,%s,%s)'
		for r in range(1,sheet.nrows):
			nik = sheet.cell(r,0).value
			ubudiyah = sheet.cell(r,1).value
			alquran = sheet.cell(r,2).value
			belajar = sheet.cell(r,3).value
			sekolah = sheet.cell(r,4).value
			diniyah = sheet.cell(r,5).value
			bulan = sheet.cell(r,6).value

			text = (no, nik, ubudiyah, alquran, belajar, sekolah, diniyah, bulan)
			cur.execute(sql, text)
			no += 1
		conn.commit()
		cur.close()
		conn.close()
		os.remove('{}'.format(data))
		return "Sudah Di Insert Mbak Absennya, Senyum Dong :p"
	except Exception as e:
		conn.rollback()
		cur.close()
		conn.close()
		logger.exception(e)
		return e

def _insertVA(data):
	conn = MySQLdb.connect(host=HOST,user=USER, passwd=PASS,db=DB)
	try:
		cur = conn.cursor()
		book = xlrd.open_workbook('{}'.format(data))
		sheet = book.sheet_by_index(0)
		sql = 'insert into va (nik, no_va) values (%s,%s)'
		for r in range(1,sheet.nrows):
			nik = sheet.cell(r,0).value
			va = sheet.cell(r,1).value
			text = (nik, va)
			cur.execute(sql, text)
		conn.commit()
		cur.close()
		conn.close()
		os.remove('{}'.format(data))
		return "Sudah Di Insert Mbak Virtualnya, Senyum Dong :p"
	except Exception as e:
		conn.rollback()
		cur.close()
		conn.close()
		logger.exception(e)
		return e[1]

def _updateVa(data):
	conn = MySQLdb.connect(host=HOST,user=USER, passwd=PASS,db=DB)
	try:
		cur = conn.cursor()
		book = xlrd.open_workbook('{}'.format(data))
		sheet = book.sheet_by_index(0)
		sql = 'update va set no_va=%s where nik=%s'
		for r in range(1,sheet.nrows):
			nik = sheet.cell(r,0).value
			va = sheet.cell(r,1).value
			text = (va, nik)
			cur.execute(sql, text)
		conn.commit()
		cur.close()
		conn.close()
		os.remove('{}'.format(data))
		return "Sudah Di Update Mbak Virtualnya, Senyum Dong :p"
	except Exception as e:
		conn.rollback()
		cur.close()
		conn.close()
		logger.exception(e)
		return e[1]
