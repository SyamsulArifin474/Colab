# jembatan antara api pedatren dengan database
from app import api, logger
from app import common
from config import text_messages, conf
from datetime import datetime
from pedatren import cetakExcel


def getPerson(cari):
    return api.santri(cari)


def pilih_bulan():
    hasil = common._useMysql('pilih_bulan')
    temp = []
    for i in hasil:
        temp.append(i[0])
    return temp


def absen(data, bulan):
    temp = []
    for ambil in data:
        content = api.santri(ambil)
        for i in content:
            hasil_absen = common._useMysql('absen', i.get('nik'), bulan)
            if len(hasil_absen) > 0:
                for hasil in hasil_absen:  #
                    bulan = datetime.strptime(
                        str(hasil[6]), "%Y-%m-%d").strftime("%Y-%m")
                    catatan_santri = catatan(i["uuid"], bulan)
                    text = text_messages['absen'].format(
                        i.get('nis'),
                        i['nama'],
                        i.get('blok'),
                        i.get('kamar'),
                        i.get('lembaga'),
                        hasil[1],  # Ubudiyah
                        hasil[2],  # Alquran
                        hasil[3],  # Belajar
                        hasil[4],  # Sekolah
                        hasil[5],  # Diniyah
                        hasil[6],  # Bulan
                    )

                    for catat in catatan_santri:
                        text += "Materi : {}\nPredikat : {}\nCatatan : {}\n\n".format(
                            catat.get("materi") or "-",
                            catat.get("skor") or "-",
                            catat.get("catatan") or "-",
                        )
                    temp.append(text)
            else:
                temp.append(
                    "Absen Belum Kami Input Untuk Nanda {}".format(i['nama']))
    return temp


def virtual(data):
    temp = []
    for ambil in data:
        content = api.santri(ambil)
        for i in content:
            hasil = common._useMysql('va', i['nik'])
            if hasil:
                text = text_messages['va'].format(
                    i.get('nis'),
                    i['nama'],
                    i['blok'],
                    i['kamar'],
                    i['lembaga'],
                    hasil[0][0] or "-", )
                sisa_tagihan = 0
                for va in hasil:
                    if va[1] > 0:
                        sisa_tagihan += va[1]
                        bulan = datetime.strptime(
                            str(va[2]), "%Y-%m-%d").strftime("%B %Y")
                        text += "Bulan : {}\nTagihan : Rp. {:,.0f} \n\n".format(
                            bulan, va[1])
                if sisa_tagihan == 0:
                    text += "Alhamdulillah \n\nSudah Lunas Semua"
                else:
                    text += "Total Tagihan : Rp. {:,.0f}".format(sisa_tagihan)
                temp.append(text)
            else:
                temp.append("Mohon Maaf, Data Tidak Ditemukan")
    return temp


def rekap_virtual(cid, lembaga=None, daerah=None):
    try:
        hasil = common._useMysql('cek_va')
        content = api.all_santri(lembaga=lembaga, daerah=daerah)

        bayar = [c for c in content if c.get('nik') in (d[0] for d in hasil)]

        temp = []
        temp.append([
            'NO', 'NIK', 'NAMA LENGKAP', 'NO. VA', 'TAGIHAN', 'BULAN', 'LEMBAGA', 'KELAS',
            'JURUSAN', 'WILAYAH', 'DAERAH', 'KAMAR'
        ])

        for jum in range(len(bayar)):
            detail_tagihan = []
            for mysql in hasil:
                if bayar[jum]['nik'] == mysql[0]:
                    tagihan = {
                        'tagihan': mysql[2],
                        'bulan': mysql[3]
                    }
                    detail_tagihan.append(tagihan)
                    bayar[jum]['no_va'] = conf["bri"] + \
                        "{}".format(mysql[1])  # "70397{}".format(mysql[1])
            # bayar[jum]['no_va'] = "70397{}".format(mysql[1])
            bayar[jum]['detail_tagihan'] = detail_tagihan
            bayar[jum]['no'] = jum + 1

        for i in bayar:
            data = (
                i.get('no'), i.get('nik') or i.get(
                    'no_passport'), i.get('nama'), i.get('no_va'),
                i['detail_tagihan'][0]['tagihan'], i['detail_tagihan'][0]['bulan'], i.get(
                    'lembaga'), i.get('kelas'),
                "{} {}".format(i.get('jurusan') or "", i.get('rombel') or ""),
                i.get('wilayah'), i.get('blok'), i.get('kamar')
            )
            temp.append(data)
            # i.get('detail_tagihan'):
            for jum in range(1, len(i.get('detail_tagihan'))):
                data = (
                    None, None, None, None, i['detail_tagihan'][jum]['tagihan'], i['detail_tagihan'][jum]['bulan']
                )
                temp.append(data)

        cetakExcel(cid, temp, formula=True)

    except Exception as e:
        logger.exception(e)


def isAdmin(cid):
    return common._useMysql('admin', cid)


def isOrtu(cid):
    return common._useMysql('get_nik', cid)


def register(cid, nik):
    cid = str(cid)
    temp = []
    content = api.santri(nik)
    for i in content:
        hasil = common._useMysql('cek_chatid', i['uuid'])
        if hasil:
            if hasil[0] == cid:
                temp.append(text_messages['terdaftar'].format(name=i['nama']))
            else:
                temp.append(text_messages['terisi'].format(name=i['nama']))
        else:
            common._useMysql('insert_chatid', cid, i['uuid'])
            data = text_messages['chat_id'].format(i['nis'],
                                                   i['nama'],
                                                   i['blok'],
                                                   i['kamar'],
                                                   i.get('lembaga')
                                                   )
            temp.append(data)
    return temp


def pedatren(pilih):
    hasil = common._useMysql('cek_data')
    content = api.all_santri()
    logger.info(len(content))
    try:
        if pilih == 'INPUT':
            for i in content:
                if i['uuid'] not in (item[0] for item in hasil):
                    common._useMysql('input', i['uuid'], i['nik'], i["nis"])
        elif pilih == 'DELETE':
            for i in hasil:
                if i[0] not in (a['uuid'] for a in content):
                    common._useMysql('del', i[0])
        else:
            return "Tidak Ada Dalam Daftar :("
        return "Mantul (Mantap Betul)"
    except Exception as e:
        logger.exception(e)


def jumlahRegister():
    jum = common._useMysql('jum_register')
    total = api.total_santri()
    persentase = (float(jum[0]) / float(total)) * 100
    pesan = "Total Santri : {}\nJumlah Register : {}\nPersentase Santri Register : {:.0f} %\nAyoooo Semangat :p".format(
        total, jum[0], persentase
    )
    return pesan


def catatan(uuid, bulan):
    temp = []
    data = api.catatan(uuid)
    saring = ("Kebersihan", "Akhlak", "Baca Al-Qur'an", "Furudhul 'Ainiyah")
    data = [i for i in data if i.get("materi") in (a for a in saring)]
    for i in data:
        bulan_api = datetime.strptime(i.get("created_at").split(
            " ")[0], "%Y-%m-%dT%H:%M:%S.%fZ").strftime("%Y-%m")
        if bulan_api == bulan:
            catatannya = {
                "materi": i.get("materi"),
                "skor": i.get("score"),
                "catatan": i.get("catatan"),
            }
            temp.append(catatannya)
    return temp


def resetID(cid):
    common._useMysql("reset_chatid", cid)


def kirim_absensi():
    waktu = datetime.now()
    sekarang = "{}-{:02d}".format(waktu.year, waktu.month)  # - 1)
    kir = common._useMysql("kirim", sekarang)
    try:
        all_santri = api.all_santri()
        santris = [i for i in all_santri if i.get(
            "nik") in (a[0] for a in kir)]
        for jum in range(len(santris)):
            for mysql in kir:
                if santris[jum]["nik"] == mysql[0]:
                    santris[jum].__setitem__("chat_id", mysql[1])
                    santris[jum].__setitem__("ubudiyah", mysql[2])
                    santris[jum].__setitem__("alquran", mysql[3])
                    santris[jum].__setitem__("belajar", mysql[4])
                    santris[jum].__setitem__("sekolah", mysql[5])
                    santris[jum].__setitem__("diniyah", mysql[6])
                    santris[jum].__setitem__("bulan", mysql[7])
        return santris
    except Exception as e:
        logger.exception(e)


def rekapRegister(cid):
    register = common._useMysql("rekap_reg")
    siswas = api.all_santri()
    try:
        temps = []
        siswa = [i for i in siswas if i.get("nik") in (a[0] for a in register)]
        temps.append(["NIK", "NAMA LENGKAP", "BLOK",
                      "KAMAR", "LEMBAGA", "KELAS", "JURUSAN"])
        for i in siswa:
            data = (
                i.get("nik"), i.get("nama"), i.get("blok"), i.get("kamar"),
                i.get("lembaga") or "-", i.get("kelas") or "-",
                "{} {}".format(i.get("jurusan") or "-",
                               i.get("rombel") or "-"),
            )
            temps.append(data)
        cetakExcel(cid, temps)
    except Exception as e:
        logger.exception(e)


def filter(pilih=None):
    try:
        if pilih == "lembaga":
            return api.filter(pilih)
        else:
            return api.filter()
    except Exception as e:
        logger.exception(e)


def gakPunyaVA(cid):
    va = common._useMysql("gakpunyava")
    santri = api.all_santri()
    try:
        temp = []
        santriGakPunyaVA = [i for i in santri if i.get(
            "nis") not in (c[0] for c in va)]
        temp.append(["NO", "NIK", "NAMA LENGKAP", "DAERAH", "KAMAR"])
        no = 1
        for i in santriGakPunyaVA:
            data = (
                no, i.get("nik"), i.get("nama"), i.get(
                    "blok") or "-", i.get("kamar") or "-"
            )
            temp.append(data)
            no += 1
        cetakExcel(cid, temp)
    except Exception as e:
        logger.exception(e)

def simpanJSON(cid):
    api.simpanAllPerson()