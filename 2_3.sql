INSERT INTO airline VALUES('Jet Blue');

INSERT INTO airport VALUES('JFK', 'NYC','United States','international'), ('PVG', 'Shanghai', 'China', 'international');

INSERT INTO customer VALUES('qy624@nyu.edu', 'c4ca4238a0b923820dcc509a6f75849b', 'Qingyuan Yao', '204', '55 Clark', 'Brooklyn', 'NY', 7186663436, 'E112233', 1124 , 'China', '2000-12-20'), 
                           ('bg1941@nyu.edu', '1125', 'Bowen Gong', '1435', '33 Bond', 'Brooklyn', 'NY', 7186756864, 'E445566', 1026 , 'China', '2001-1-22'),
                           ('ab123@nyu.edu', 'ilovesql', 'Tom Cruise', '110', '370 Jay St', 'Brooklyn', 'NY', 232198841, 'E778899', 0124 , 'United States', '1998-1-10');

INSERT INTO airplane VALUES(100,'Jet Blue', 100,'Boeing', 5),
                           (101,'Jet Blue', 200,'Boeing', 3),
                           (102,'Jet Blue', 250,'Boeing', 1);

INSERT INTO staff VALUES('Jack_Ma', 'Jet Blue', 'cfcd208495d565ef66e7dff9f98764da', 'Jack', 'Ma', '1999-11-11');

INSERT INTO flight VALUES('Jet Blue', 100 ,001, '2022-11-11 02:00:00', 'JFK', '2022-11-11 03:00:00', 'PVG', 1000.00, 'delayed'),
                         ('Jet Blue', 102 ,002, '2023-12-10 11:00:00', 'PVG', '2023-12-11 12:00:00', 'JFK', 2000.00, 'on-time');

INSERT INTO ticket VALUES('Jet Blue', 100, 01, 001, '2022-11-11 02:00:00', 999),
                         ('Jet Blue', 102, 11, 002, '2023-12-10 11:00:00', 2100);

INSERT INTO purchase VALUES(01, 'qy624@nyu.edu', '2022-11-01 10:15:00', 'credit', 11223344, 'Qingyuan Yao', '2027-12-01'),
                           (01, 'bg1941@nyu.edu', '2022-10-21 09:33:00', 'debit', 44556677, 'Bowen Gong', '2023-10-09'),
                           (11, 'qy624@nyu.edu', '2022-11-21 12:12:00', 'debit', 44332211, 'Qingyuan Yao', '2023-12-19'),
                           (11, 'bg1941@nyu.edu', '2023-10-21 11:36:00', 'credit', 77665544, 'Bowen Gong', '2028-11-11');