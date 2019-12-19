# Simple Telegram Bot
#### Install
install python versi 3.6.7

#### Install Modul
```python
pip install -r requiretment.txt
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