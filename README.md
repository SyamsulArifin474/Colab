# Simple Telegram Bot
#### Install
install python versi 3.6.7

#### Install Modul
```python
pip install -r requiretment.txt
```
#### Buat OS Environment
##### Windows
```shell
set TOKEN_BOT_TELEGRAM=ISI DENGAN TOKEN TELEGRAMMU
set USERNAME_PEDATREN=ISI DENGAN USERNAME PEDATRENMU
set PASSWORD_PEDATREN=ISI DENGAN PASSWORD PEDATRENMU
```
##### Linux
```shell
export TOKEN_BOT_TELEGRAM=ISI DENGAN TOKEN TELEGRAMMU
export USERNAME_PEDATREN=ISI DENGAN USERNAME PEDATRENMU
export PASSWORD_PEDATREN=ISI DENGAN PASSWORD PEDATRENMU
```

#### Jalankan Bot
```python
python Bot.py
```
#### Setting Database
|HOST|USERNAME|PASSWORD|DB NAME|
|---|---------|--------|-------|
|Localhost|root||daltim|

#### Contoh Trigger Insert Absen
```mysql
DELIMITER $$
CREATE TRIGGER `insertabsen` BEFORE INSERT ON `absen` FOR EACH ROW BEGIN
DECLARE msg varchar(65);
IF NEW.nik = '' or NEW.nik IS NULL THEN
	SIGNAL SQLSTATE '45000'
    SET MESSAGE_TEXT = "Gagal Menambah Absensi, Karena NIK/PASSPORT tidak boleh kosong";    
ELSEIF NEW.nik NOT REGEXP "^[0-9]{16}$|^[a-zA-Z]{2}[0-9]{7}$" THEN
	SET msg = CONCAT("Gagal Menambah Absensi, Karena NIK/PASSPORT Tidak Sesuai ", NEW.nik);
	SIGNAL SQLSTATE '45000'
    SET MESSAGE_TEXT = msg;
ELSEIF NEW.bulan > now() THEN
	SIGNAL SQLSTATE '45000'
    SET MESSAGE_TEXT = "Bulan tidak boleh lebih dari hari ini";
END IF;
END
$$
DELIMITER ;
```