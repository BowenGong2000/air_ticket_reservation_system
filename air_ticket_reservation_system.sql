-- phpMyAdmin SQL Dump
-- version 5.1.1
-- https://www.phpmyadmin.net/
--
-- 主机： localhost:8889
-- 生成日期： 2022-06-30 21:06:07
-- 服务器版本： 5.7.34
-- PHP 版本： 7.4.21

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- 数据库： `air_ticket_reservation_system`
--

-- --------------------------------------------------------

--
-- 表的结构 `airline`
--

CREATE TABLE `airline` (
  `al_name` varchar(30) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- 转存表中的数据 `airline`
--

INSERT INTO `airline` (`al_name`) VALUES
('Jet Blue');

-- --------------------------------------------------------

--
-- 表的结构 `airplane`
--

CREATE TABLE `airplane` (
  `ap_id` decimal(10,0) NOT NULL,
  `al_name` varchar(30) NOT NULL,
  `seat_num` decimal(4,0) NOT NULL,
  `company` varchar(30) NOT NULL,
  `age` decimal(4,0) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- 转存表中的数据 `airplane`
--

INSERT INTO `airplane` (`ap_id`, `al_name`, `seat_num`, `company`, `age`) VALUES
('100', 'Jet Blue', '100', 'Boeing', '5'),
('101', 'Jet Blue', '200', 'Boeing', '3'),
('102', 'Jet Blue', '250', 'Boeing', '1'),
('103', 'Jet Blue', '500', 'Boeing', '2'),
('104', 'Jet Blue', '123', 'Audi', '0');

-- --------------------------------------------------------

--
-- 表的结构 `airport`
--

CREATE TABLE `airport` (
  `apt_name` varchar(30) NOT NULL,
  `city` varchar(30) NOT NULL,
  `country` varchar(30) NOT NULL,
  `apt_type` varchar(30) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- 转存表中的数据 `airport`
--

INSERT INTO `airport` (`apt_name`, `city`, `country`, `apt_type`) VALUES
('JFK', 'NYC', 'United States', 'international'),
('LGA', 'NYC', 'United States', 'International'),
('PVG', 'Shanghai', 'China', 'international');

-- --------------------------------------------------------

--
-- 表的结构 `customer`
--

CREATE TABLE `customer` (
  `email` varchar(30) NOT NULL,
  `pswd` varchar(300) NOT NULL,
  `cus_name` varchar(30) NOT NULL,
  `build_num` varchar(30) DEFAULT NULL,
  `street` varchar(30) DEFAULT NULL,
  `city` varchar(30) DEFAULT NULL,
  `state` char(2) DEFAULT NULL,
  `pho_num` decimal(10,0) DEFAULT NULL,
  `pspt_num` varchar(10) DEFAULT NULL,
  `pspt_exp` date NOT NULL,
  `pspt_country` varchar(30) DEFAULT NULL,
  `dob` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- 转存表中的数据 `customer`
--

INSERT INTO `customer` (`email`, `pswd`, `cus_name`, `build_num`, `street`, `city`, `state`, `pho_num`, `pspt_num`, `pspt_exp`, `pspt_country`, `dob`) VALUES
('123@nyu.edu', '4a7d1ed414474e4033ac29ccb8653d9b', 'Paul', '123', '123', 'Brooklyn', 'NY', '7186756860', '12345', '2022-06-08', 'china', '2022-06-01'),
('ab123@nyu.edu', 'cfcd208495d565ef66e7dff9f98764da\r\n', 'Tom Cruise', '110', '370 Jay St', 'Brooklyn', 'NY', '232198841', 'E778899', '2000-01-24', 'United States', '1998-01-10'),
('bg1941@nyu.edu', 'c21002f464c5fc5bee3b98ced83963b8', 'Bowen Gong', '1435', '33 Bond', 'Brooklyn', 'NY', '7186756864', 'E445566', '2000-10-26', 'China', '2001-01-22'),
('qy624@nyu.edu', 'c4ca4238a0b923820dcc509a6f75849b', 'Qingyuan Yao', '204', '55 Clark', 'Brooklyn', 'NY', '7186663436', 'E112233', '2000-11-24', 'China', '2000-12-20');

-- --------------------------------------------------------

--
-- 表的结构 `email`
--

CREATE TABLE `email` (
  `us_name` varchar(30) NOT NULL,
  `al_name` varchar(30) NOT NULL,
  `email` varchar(30) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- 表的结构 `flight`
--

CREATE TABLE `flight` (
  `al_name` varchar(30) NOT NULL,
  `ap_id` varchar(30) NOT NULL,
  `flt_num` decimal(10,0) NOT NULL,
  `dep_dnt` datetime NOT NULL,
  `dep_apt` varchar(30) NOT NULL,
  `arr_dnt` datetime NOT NULL,
  `arr_apt` varchar(30) NOT NULL,
  `base_price` decimal(6,2) NOT NULL,
  `stts` varchar(30) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- 转存表中的数据 `flight`
--

INSERT INTO `flight` (`al_name`, `ap_id`, `flt_num`, `dep_dnt`, `dep_apt`, `arr_dnt`, `arr_apt`, `base_price`, `stts`) VALUES
('Jet Blue', '100', '1', '2022-11-11 02:00:00', 'JFK', '2022-11-11 03:00:00', 'PVG', '1000.00', 'on-time'),
('Jet Blue', '100', '3', '2022-06-24 22:10:00', 'JFK', '2022-06-25 22:10:00', 'PVG', '1000.00', 'delayed'),
('Jet Blue', '101', '4', '2022-06-30 00:00:00', 'PVG', '2022-07-01 18:13:00', 'JFK', '1200.00', 'delayed'),
('Jet Blue', '102', '2', '2023-12-10 11:00:00', 'PVG', '2023-12-11 12:00:00', 'JFK', '2000.00', 'on-time');

-- --------------------------------------------------------

--
-- 表的结构 `phone_num`
--

CREATE TABLE `phone_num` (
  `us_name` varchar(30) NOT NULL,
  `al_name` varchar(30) NOT NULL,
  `pho_num` decimal(9,0) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- 表的结构 `purchase`
--

CREATE TABLE `purchase` (
  `tkt_id` decimal(20,0) NOT NULL,
  `email` varchar(30) NOT NULL,
  `purch_dnt` datetime NOT NULL,
  `card_type` varchar(30) NOT NULL,
  `card_num` decimal(30,0) NOT NULL,
  `card_name` varchar(30) NOT NULL,
  `exp_date` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- 转存表中的数据 `purchase`
--

INSERT INTO `purchase` (`tkt_id`, `email`, `purch_dnt`, `card_type`, `card_num`, `card_name`, `exp_date`) VALUES
('1', 'bg1941@nyu.edu', '2022-04-21 09:33:00', 'debit', '44556677', 'Bowen Gong', '2023-10-09'),
('1', 'qy624@nyu.edu', '2022-06-01 10:15:00', 'credit', '11223344', 'Qingyuan Yao', '2027-12-01'),
('11', 'bg1941@nyu.edu', '2022-06-21 11:36:00', 'credit', '77665544', 'Bowen Gong', '2028-11-11'),
('11', 'qy624@nyu.edu', '2022-11-21 12:12:00', 'debit', '44332211', 'Qingyuan Yao', '2023-12-19');

-- --------------------------------------------------------

--
-- 表的结构 `rate`
--

CREATE TABLE `rate` (
  `al_name` varchar(30) NOT NULL,
  `ap_id` varchar(30) NOT NULL,
  `flt_num` decimal(10,0) NOT NULL,
  `dep_dnt` datetime NOT NULL,
  `email` varchar(30) NOT NULL,
  `rate` decimal(2,1) NOT NULL,
  `com` varchar(200) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- 转存表中的数据 `rate`
--

INSERT INTO `rate` (`al_name`, `ap_id`, `flt_num`, `dep_dnt`, `email`, `rate`, `com`) VALUES
('Jet Blue', '101', '4', '2022-06-30 00:00:00', 'bg1941@nyu.edu', '5.0', 'love the plane!!!');

-- --------------------------------------------------------

--
-- 表的结构 `staff`
--

CREATE TABLE `staff` (
  `us_name` varchar(30) NOT NULL,
  `al_name` varchar(30) NOT NULL,
  `pswd` varchar(300) NOT NULL,
  `f_name` varchar(30) NOT NULL,
  `l_name` varchar(30) NOT NULL,
  `dob` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- 转存表中的数据 `staff`
--

INSERT INTO `staff` (`us_name`, `al_name`, `pswd`, `f_name`, `l_name`, `dob`) VALUES
('Ashe', 'Jet Blue', '4a7d1ed414474e4033ac29ccb8653d9b', 'Ashe', 'Yan', '2022-06-09'),
('Jack', 'Jet Blue', 'cfcd208495d565ef66e7dff9f98764da\r\n', 'Jack', 'Ma', '1999-11-11');

-- --------------------------------------------------------

--
-- 表的结构 `ticket`
--

CREATE TABLE `ticket` (
  `al_name` varchar(30) NOT NULL,
  `ap_id` varchar(30) NOT NULL,
  `tkt_id` decimal(20,0) NOT NULL,
  `flt_num` decimal(10,0) NOT NULL,
  `dep_dnt` datetime NOT NULL,
  `sold_price` decimal(10,0) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- 转存表中的数据 `ticket`
--

INSERT INTO `ticket` (`al_name`, `ap_id`, `tkt_id`, `flt_num`, `dep_dnt`, `sold_price`) VALUES
('Jet Blue', '100', '1', '1', '2022-11-11 02:00:00', '999'),
('Jet Blue', '102', '11', '2', '2023-12-10 11:00:00', '2100');

--
-- 转储表的索引
--

--
-- 表的索引 `airline`
--
ALTER TABLE `airline`
  ADD PRIMARY KEY (`al_name`);

--
-- 表的索引 `airplane`
--
ALTER TABLE `airplane`
  ADD PRIMARY KEY (`al_name`,`ap_id`);

--
-- 表的索引 `airport`
--
ALTER TABLE `airport`
  ADD PRIMARY KEY (`apt_name`);

--
-- 表的索引 `customer`
--
ALTER TABLE `customer`
  ADD PRIMARY KEY (`email`);

--
-- 表的索引 `email`
--
ALTER TABLE `email`
  ADD PRIMARY KEY (`us_name`,`al_name`,`email`),
  ADD KEY `al_name` (`al_name`);

--
-- 表的索引 `flight`
--
ALTER TABLE `flight`
  ADD PRIMARY KEY (`al_name`,`ap_id`,`flt_num`,`dep_dnt`),
  ADD KEY `dep_apt` (`dep_apt`),
  ADD KEY `arr_apt` (`arr_apt`);

--
-- 表的索引 `phone_num`
--
ALTER TABLE `phone_num`
  ADD PRIMARY KEY (`us_name`,`al_name`,`pho_num`),
  ADD KEY `al_name` (`al_name`);

--
-- 表的索引 `purchase`
--
ALTER TABLE `purchase`
  ADD PRIMARY KEY (`tkt_id`,`email`),
  ADD KEY `email` (`email`);

--
-- 表的索引 `rate`
--
ALTER TABLE `rate`
  ADD PRIMARY KEY (`al_name`,`flt_num`,`dep_dnt`,`email`),
  ADD KEY `al_name` (`al_name`,`ap_id`,`flt_num`,`dep_dnt`),
  ADD KEY `email` (`email`);

--
-- 表的索引 `staff`
--
ALTER TABLE `staff`
  ADD PRIMARY KEY (`us_name`),
  ADD KEY `al_name` (`al_name`);

--
-- 表的索引 `ticket`
--
ALTER TABLE `ticket`
  ADD PRIMARY KEY (`tkt_id`),
  ADD KEY `al_name` (`al_name`,`ap_id`,`flt_num`,`dep_dnt`);

--
-- 限制导出的表
--

--
-- 限制表 `airplane`
--
ALTER TABLE `airplane`
  ADD CONSTRAINT `airplane_ibfk_1` FOREIGN KEY (`al_name`) REFERENCES `airline` (`al_name`);

--
-- 限制表 `email`
--
ALTER TABLE `email`
  ADD CONSTRAINT `email_ibfk_1` FOREIGN KEY (`us_name`) REFERENCES `staff` (`us_name`),
  ADD CONSTRAINT `email_ibfk_2` FOREIGN KEY (`al_name`) REFERENCES `airline` (`al_name`);

--
-- 限制表 `flight`
--
ALTER TABLE `flight`
  ADD CONSTRAINT `flight_ibfk_1` FOREIGN KEY (`al_name`) REFERENCES `airline` (`al_name`),
  ADD CONSTRAINT `flight_ibfk_2` FOREIGN KEY (`dep_apt`) REFERENCES `airport` (`apt_name`),
  ADD CONSTRAINT `flight_ibfk_3` FOREIGN KEY (`arr_apt`) REFERENCES `airport` (`apt_name`);

--
-- 限制表 `phone_num`
--
ALTER TABLE `phone_num`
  ADD CONSTRAINT `phone_num_ibfk_1` FOREIGN KEY (`us_name`) REFERENCES `staff` (`us_name`),
  ADD CONSTRAINT `phone_num_ibfk_2` FOREIGN KEY (`al_name`) REFERENCES `airline` (`al_name`);

--
-- 限制表 `purchase`
--
ALTER TABLE `purchase`
  ADD CONSTRAINT `purchase_ibfk_1` FOREIGN KEY (`tkt_id`) REFERENCES `ticket` (`tkt_id`),
  ADD CONSTRAINT `purchase_ibfk_2` FOREIGN KEY (`email`) REFERENCES `customer` (`email`);

--
-- 限制表 `rate`
--
ALTER TABLE `rate`
  ADD CONSTRAINT `rate_ibfk_1` FOREIGN KEY (`al_name`,`ap_id`,`flt_num`,`dep_dnt`) REFERENCES `flight` (`al_name`, `ap_id`, `flt_num`, `dep_dnt`),
  ADD CONSTRAINT `rate_ibfk_2` FOREIGN KEY (`email`) REFERENCES `customer` (`email`);

--
-- 限制表 `staff`
--
ALTER TABLE `staff`
  ADD CONSTRAINT `staff_ibfk_1` FOREIGN KEY (`al_name`) REFERENCES `airline` (`al_name`);

--
-- 限制表 `ticket`
--
ALTER TABLE `ticket`
  ADD CONSTRAINT `ticket_ibfk_1` FOREIGN KEY (`al_name`,`ap_id`,`flt_num`,`dep_dnt`) REFERENCES `flight` (`al_name`, `ap_id`, `flt_num`, `dep_dnt`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
