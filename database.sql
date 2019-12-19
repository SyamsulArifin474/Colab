-- phpMyAdmin SQL Dump
-- version 4.9.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Dec 19, 2019 at 12:29 PM
-- Server version: 10.4.8-MariaDB
-- PHP Version: 7.3.11

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `daltim`
--

-- --------------------------------------------------------

--
-- Table structure for table `absen`
--

CREATE TABLE `absen` (
  `id` int(11) NOT NULL,
  `nik` varchar(16) NOT NULL,
  `ubudiyah` int(3) NOT NULL,
  `alquran` int(3) NOT NULL,
  `belajar` int(3) NOT NULL,
  `sekolah` int(3) NOT NULL,
  `diniyah` int(3) NOT NULL,
  `bulan` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Triggers `absen`
--
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

-- --------------------------------------------------------

--
-- Table structure for table `admin`
--

CREATE TABLE `admin` (
  `id` int(5) NOT NULL,
  `nama` varchar(25) DEFAULT NULL,
  `chat_id` int(10) DEFAULT NULL,
  `level` enum('Admin','Staf') DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `admin`
--

INSERT INTO `admin` (`id`, `nama`, `chat_id`, `level`) VALUES
(1, 'Syafiqiyah Adhimi', 567400538, 'Admin'),
(2, 'Kak Umam', 222329532, 'Staf'),
(3, 'Faizul Amaly', 329627396, 'Admin'),
(4, 'Telegram Daltim Pesantren', 372628748, 'Staf');

-- --------------------------------------------------------

--
-- Table structure for table `va`
--

CREATE TABLE `va` (
  `id` int(8) NOT NULL,
  `nik` varchar(16) NOT NULL,
  `no_va` char(10) DEFAULT NULL,
  `tagihan` int(8) NOT NULL DEFAULT 0,
  `jum_bayar` int(8) NOT NULL DEFAULT 0,
  `sisa_tagihan` int(10) NOT NULL,
  `tanggal_rekap` date NOT NULL DEFAULT '2018-12-01',
  `bulan` date NOT NULL DEFAULT '2018-12-01'
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Triggers `va`
--
DELIMITER $$
CREATE TRIGGER `insertva` BEFORE INSERT ON `va` FOR EACH ROW BEGIN
DECLARE msg varchar(65);
IF (EXISTS(SELECT 1 FROM va WHERE no_va = NEW.no_va)) THEN
	SET msg = CONCAT('Gagal Insert No VA, Karena terdapat Duplikat No VA', ' ', NEW.no_va);
	SIGNAL SQLSTATE '45000'
    SET MESSAGE_TEXT = msg;
ELSEIF (EXISTS(SELECT 1 FROM va WHERE nik = NEW.nik)) THEN
	SET msg = CONCAT('Gagal Insert No VA, Karena terdapat Duplikat NIK', ' ', NEW.nik);
	SIGNAL SQLSTATE '45000'
    SET MESSAGE_TEXT = msg;
ELSEIF NEW.nik NOT REGEXP "^[0-9]{16}$|^[a-zA-Z]{2}[0-9]{7}$" THEN
	SET msg = CONCAT("Gagal Insert Data, Karena NIK/PASSPORT Tidak Sesuai ", NEW.nik);
	SIGNAL SQLSTATE '45000'
    SET MESSAGE_TEXT = msg;
ELSEIF NEW.no_va NOT REGEXP "^[0-9]{10}$" THEN
	SET msg = CONCAT("Gagal, Karena No VA Harus Berupa Angka 10 Digits ", NEW.no_va);
	SIGNAL SQLSTATE '45000'
    SET MESSAGE_TEXT = msg;
ELSEIF NEW.no_va = '' or NEW.no_va IS NULL THEN
	SIGNAL SQLSTATE '45000'
    SET MESSAGE_TEXT = "Gagal Insert Data, Karena No VA tidak boleh kosong";    
END IF;
END
$$
DELIMITER ;

-- --------------------------------------------------------

--
-- Table structure for table `wilayah`
--

CREATE TABLE `wilayah` (
  `uuid` char(36) NOT NULL,
  `nik` varchar(16) DEFAULT NULL,
  `nis` char(10) DEFAULT NULL,
  `chat_id` char(9) DEFAULT NULL,
  `aktif` enum('Y','T') NOT NULL DEFAULT 'Y'
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Triggers `wilayah`
--
DELIMITER $$
CREATE TRIGGER `update_wilayah` BEFORE UPDATE ON `wilayah` FOR EACH ROW BEGIN
IF NEW.chat_id NOT REGEXP '^[0-9]{9}$' THEN
  SIGNAL SQLSTATE '45000'
    SET MESSAGE_TEXT = "Chat ID Harus Berapa Angka 9 Digits";
END IF;
END
$$
DELIMITER ;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `absen`
--
ALTER TABLE `absen`
  ADD PRIMARY KEY (`id`),
  ADD KEY `bulan` (`bulan`),
  ADD KEY `nik` (`nik`);

--
-- Indexes for table `admin`
--
ALTER TABLE `admin`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `chat_id` (`chat_id`);

--
-- Indexes for table `va`
--
ALTER TABLE `va`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `nik` (`nik`),
  ADD KEY `no_va` (`no_va`);

--
-- Indexes for table `wilayah`
--
ALTER TABLE `wilayah`
  ADD PRIMARY KEY (`uuid`),
  ADD UNIQUE KEY `nik` (`nik`),
  ADD KEY `chat_id` (`chat_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `admin`
--
ALTER TABLE `admin`
  MODIFY `id` int(5) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `va`
--
ALTER TABLE `va`
  MODIFY `id` int(8) NOT NULL AUTO_INCREMENT;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
