-- phpMyAdmin SQL Dump
-- version 5.1.0
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Mar 09, 2022 at 11:03 AM
-- Server version: 10.4.18-MariaDB
-- PHP Version: 8.0.3

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `clinictest`
--

-- --------------------------------------------------------

--
-- Table structure for table `clinic`
--

CREATE TABLE `clinic` (
  `clinicID` int(11) NOT NULL,
  `emailID` varchar(255) NOT NULL,
  `clinicName` varchar(255) DEFAULT NULL,
  `clinicPass` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `clinic`
--

INSERT INTO `clinic` (`clinicID`, `emailID`, `clinicName`, `clinicPass`) VALUES
(1, 'clinic1@gmail.com', 'A', '123456'),
(2, 'clinic2@gmail.com', 'B', 'qwe'),
(4, '', 'C', 'gsg'),
(5, '', 'clinic-test', 'clinic-test'),
(7, 'sayantan.bose286@gmail.com', 'clinic-test-1', 'clinic-test-1'),
(10, 'sdg9535@gmail.com', 'testSDG', 'testSDG134'),
(11, 'sayantan.bose2866@gmail.com ', 'SayantanClinic', 'SayantanClinic');

-- --------------------------------------------------------

--
-- Table structure for table `doctor`
--

CREATE TABLE `doctor` (
  `clinicID` int(11) DEFAULT NULL,
  `doctorID` int(11) NOT NULL,
  `doctorName` varchar(255) DEFAULT NULL,
  `specialization` varchar(255) DEFAULT NULL,
  `DOB` varchar(8) NOT NULL,
  `phoneNo` int(12) NOT NULL,
  `emailID` varchar(255) NOT NULL,
  `time` varchar(255) DEFAULT NULL,
  `day` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `doctor`
--

INSERT INTO `doctor` (`clinicID`, `doctorID`, `doctorName`, `specialization`, `DOB`, `phoneNo`, `emailID`, `time`, `day`) VALUES
(1, 1, 'SDG', 'eye', '', 0, '', '7 PM', 'thrusday'),
(1, 2, 'x', 'heart', '', 123456781, '', '8 pM', 'sat'),
(2, 3, 'y', 'eye', '', 0, '', '9pm', 'sat'),
(1, 4, 'E', 'heart', '', 123456789, '', '7:30 pm', 'wed'),
(2, 5, 'R', 'gyno', '', 0, '', '8pm', 'tue'),
(5, 6, 'Doctor-A', 'ENT', '03081999', 123456789, 'wddwaf', '5pm', 'thrusday'),
(5, 8, 'Doctor-A', 'ENT', '03081999', 123456781, 'wddwaf', '5pm', 'thrusday'),
(7, 9, 'd-clinic-7', 'Heart', '03081999', 123456789, 'fvaffae', '9.00 pm', 'sun'),
(7, 10, 'd1-clinic-7', 'Heart', '03081999', 123456789, 'fvaffae', '9.00 pm', 'sun'),
(7, 11, 'd2-clinic-7', 'h', '', 0, '', '', ''),
(2, 12, 'd-clinic-2', 'Heart', '1355', 123456789, 'fvaffae', '5pm', 'sun'),
(2, 13, 'd1-clinic-2', 'Heart', '424', 123456789, 'dawf', '8pm', 'sun'),
(2, 14, 'd1-clinic-2', 'Heart', '424', 123456789, 'dawf', '8pm', 'sun'),
(2, 15, 'd1-clinic-2', 'Heart', '424', 123456789, 'dawf', '8pm', 'sun'),
(2, 16, 'd1-clinic-2', 'Heart', '424', 123456789, 'dawf', '8pm', 'sun'),
(2, 17, 'd1-clinic-2', 'Heart', '424', 123456789, 'dawf', '8pm', 'sun'),
(10, 18, 'dfg', 'eye', '12345', 123456789, '12@gmail.com', '11', '4q');

-- --------------------------------------------------------

--
-- Table structure for table `patient`
--

CREATE TABLE `patient` (
  `clinicID` int(11) DEFAULT NULL,
  `patientID` int(11) NOT NULL,
  `patientName` varchar(255) DEFAULT NULL,
  `patientMobile` int(10) DEFAULT NULL,
  `doctorName` varchar(255) DEFAULT NULL,
  `specialization` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `patient`
--

INSERT INTO `patient` (`clinicID`, `patientID`, `patientName`, `patientMobile`, `doctorName`, `specialization`) VALUES
(5, 1, 'clinic5-patient1', 123456, 'Doctor-A', 'Heart'),
(1, 3, 'clinic-1-patient1', 1234568, 'SDG', 'eye'),
(10, 22, 'Subhadeep Ghosh', 1234567890, 'dfg', 'eye');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `clinic`
--
ALTER TABLE `clinic`
  ADD PRIMARY KEY (`clinicID`);

--
-- Indexes for table `doctor`
--
ALTER TABLE `doctor`
  ADD PRIMARY KEY (`doctorID`),
  ADD KEY `clinicID` (`clinicID`);

--
-- Indexes for table `patient`
--
ALTER TABLE `patient`
  ADD PRIMARY KEY (`patientID`),
  ADD KEY `clinicID` (`clinicID`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `clinic`
--
ALTER TABLE `clinic`
  MODIFY `clinicID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=12;

--
-- AUTO_INCREMENT for table `doctor`
--
ALTER TABLE `doctor`
  MODIFY `doctorID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=19;

--
-- AUTO_INCREMENT for table `patient`
--
ALTER TABLE `patient`
  MODIFY `patientID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=24;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `doctor`
--
ALTER TABLE `doctor`
  ADD CONSTRAINT `doctor_ibfk_1` FOREIGN KEY (`clinicID`) REFERENCES `clinic` (`clinicID`);

--
-- Constraints for table `patient`
--
ALTER TABLE `patient`
  ADD CONSTRAINT `patient_ibfk_1` FOREIGN KEY (`clinicID`) REFERENCES `clinic` (`clinicID`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
