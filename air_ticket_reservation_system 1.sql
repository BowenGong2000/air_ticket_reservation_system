CREATE TABLE airline(
    al_name varchar(30) NOT NULL,
    PRIMARY KEY (al_name));

CREATE TABLE airport(
    apt_name varchar(30) NOT NULL,
    city varchar(30) NOT NULL,
    country varchar(30) NOT NULL,
    apt_type varchar(30) NOT NULL,
    PRIMARY KEY (apt_name));
    
CREATE TABLE staff(
    us_name varchar(30) NOT NULL,
    al_name varchar(30) NOT NULL,
    pswd varchar(300) NOT NULL,
    f_name varchar(30) NOT NULL,
    l_name varchar(30) NOT NULL,
    dob DATE NOT NULL,
    PRIMARY KEY (us_name),
    FOREIGN KEY (al_name) REFERENCES airline(al_name));
  
CREATE TABLE phone_num(
    us_name varchar(30) NOT NULL,
    al_name varchar(30) NOT NULL,
    pho_num numeric(9,0) NOT NULL,
    PRIMARY KEY (us_name, al_name, pho_num),
    FOREIGN KEY (us_name) REFERENCES staff(us_name),
    FOREIGN KEY (al_name) REFERENCES airline(al_name));
 
CREATE TABLE email(
    us_name varchar(30) NOT NULL,
    al_name varchar(30) NOT NULL,
    email varchar(30) NOT NULL,
    PRIMARY KEY (us_name, al_name, email),
    FOREIGN KEY (us_name) REFERENCES staff(us_name),
    FOREIGN KEY (al_name) REFERENCES airline(al_name));
    
CREATE TABLE airplane(
    ap_id numeric(10,0) NOT NULL,
    al_name varchar(30) NOT NULL,
    seat_num numeric(4,0) NOT NULL,
    company varchar(30) NOT NULL,
    age numeric(4,0) NOT NULL,
    PRIMARY KEY (al_name, ap_id),
    FOREIGN KEY (al_name) REFERENCES airline(al_name));
    
CREATE TABLE flight(
    al_name varchar(30) NOT NULL,
    ap_id varchar(30) NOT NULL,
    flt_num numeric(10,0) NOT NULL,
    dep_dnt DATETIME NOT NULL,
    dep_apt varchar(30) NOT NULL,
    arr_dnt DATETIME NOT NULL,
    arr_apt varchar(30) NOT NULL,
    base_price numeric(6,2) NOT NULL,
    stts varchar (30),
    PRIMARY KEY (al_name, ap_id ,flt_num, dep_dnt),
    FOREIGN KEY (al_name) REFERENCES airline(al_name),
    FOREIGN KEY (dep_apt) REFERENCES airport(apt_name),
    FOREIGN KEY (arr_apt) REFERENCES airport(apt_name)); 

CREATE TABLE ticket(
    al_name varchar(30) NOT NULL,
    ap_id varchar(30) NOT NULL,
    tkt_id numeric(20,0) NOT NULL,
    flt_num numeric(10,0) NOT NULL,
    dep_dnt DATETIME NOT NULL,
    sold_price numeric(10,0) NOT NULL,
    PRIMARY KEY (tkt_id),
    FOREIGN KEY (al_name, ap_id, flt_num, dep_dnt) REFERENCES flight(al_name, ap_id,flt_num, dep_dnt));

CREATE TABLE customer(
    email varchar(30) NOT NULL,
    pswd varchar(300) NOT NULL,
    cus_name varchar(30) NOT NULL,
    build_num varchar(30),
    street varchar(30),
    city varchar(30),
    state char(2),
    pho_num numeric(10,0),
    pspt_num varchar(10),
    pspt_exp DATE NOT NULL,
    pspt_country varchar(30),
    dob DATE NOT NULL,
    PRIMARY KEY (email));
    
CREATE TABLE purchase(
    tkt_id numeric(20,0) NOT NULL,
    email varchar(30) NOT NULL,
    purch_dnt DATETIME NOT NULL,
    card_type varchar(30) NOT NULL,
    card_num numeric(30,0) NOT NULL,
    card_name varchar(30) NOT NULL,
    exp_date DATE NOT NULL,
    PRIMARY KEY (tkt_id, email),
    FOREIGN KEY (tkt_id) REFERENCES ticket(tkt_id),
    FOREIGN KEY (email) REFERENCES customer(email));
    
CREATE TABLE rate(
    al_name varchar(30) NOT NULL,
    ap_id varchar(30) NOT NULL,
    flt_num numeric(10,0) NOT NULL,
    dep_dnt DATETIME NOT NULL,
    email varchar(30) NOT NULL,
    rate numeric(2,1) NOT NULL,
    com varchar(200) NOT NULL,
    PRIMARY KEY (al_name, flt_num, dep_dnt, email),
    FOREIGN KEY (al_name, ap_id, flt_num, dep_dnt) REFERENCES flight(al_name, ap_id,flt_num, dep_dnt),
    FOREIGN KEY (email) REFERENCES customer(email));