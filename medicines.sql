-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Jun 22, 2025 at 01:37 PM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.0.30

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `medicines`
--

-- --------------------------------------------------------

--
-- Table structure for table `meddata`
--

CREATE TABLE `meddata` (
  `Med_id` int(100) NOT NULL,
  `Name` varchar(100) NOT NULL,
  `Quantity` int(50) NOT NULL,
  `Price` double(10,2) NOT NULL,
  `Expiry` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `meddata`
--

INSERT INTO `meddata` (`Med_id`, `Name`, `Quantity`, `Price`, `Expiry`) VALUES
(1, 'Paracetamol', 10, 500.00, '2025-11-10'),
(2, 'Amoxicillin', 100, 120.00, '2026-06-15'),
(4, 'Ibuprofen', 150, 65.25, '2025-10-01'),
(5, 'Cetirizine', 80, 40.00, '2026-01-20'),
(6, 'Metformin', 120, 90.00, '2025-08-10'),
(7, 'Azithromycin', 60, 85.00, '2025-11-05'),
(8, 'Loratadine', 90, 55.00, '2026-03-22'),
(9, 'Omeprazole', 110, 45.75, '2025-09-30'),
(10, 'Ciprofloxacin', 130, 78.00, '2026-04-18'),
(11, 'Aspirin', 300, 30.00, '2026-01-01'),
(12, 'Doxycycline', 70, 92.00, '2026-02-14'),
(13, 'Losartan', 95, 88.50, '2025-10-25'),
(14, 'Hydrochlorothiazide', 85, 65.00, '2025-11-30'),
(15, 'Simvastatin', 150, 72.25, '2026-05-10'),
(16, 'Clarithromycin', 100, 99.99, '2026-07-07'),
(17, 'Levothyroxine', 140, 60.00, '2025-12-12'),
(18, 'Prednisone', 75, 43.00, '2026-06-06'),
(19, 'Ranitidine', 105, 34.50, '2026-03-03'),
(20, 'Naproxen', 200, 70.00, '2025-08-08'),
(21, 'Vitamin C', 250, 25.00, '2026-09-09');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `meddata`
--
ALTER TABLE `meddata`
  ADD PRIMARY KEY (`Med_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `meddata`
--
ALTER TABLE `meddata`
  MODIFY `Med_id` int(100) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=22;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
