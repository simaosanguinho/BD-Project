DROP TABLE IF EXISTS bank CASCADE;
DROP TABLE IF EXISTS loan CASCADE;
DROP TABLE IF EXISTS depositor CASCADE;
DROP TABLE IF EXISTS borrower CASCADE;
DROP TABLE IF EXISTS Customer CASCADE;
DROP TABLE IF EXISTS Sale CASCADE;
DROP TABLE IF EXISTS Pay CASCADE;
DROP TABLE IF EXISTS Employee CASCADE;
DROP TABLE IF EXISTS Process CASCADE;
DROP TABLE IF EXISTS Department CASCADE;
DROP TABLE IF EXISTS Workplace CASCADE;
DROP TABLE IF EXISTS Works CASCADE;
DROP TABLE IF EXISTS Office CASCADE;
DROP TABLE IF EXISTS Warehouse CASCADE;
DROP TABLE IF EXISTS Product CASCADE;
DROP TABLE IF EXISTS EAN_Product CASCADE;
DROP TABLE IF EXISTS Supplier CASCADE;
DROP TABLE IF EXISTS contains_ CASCADE;
DROP TABLE IF EXISTS supply_contract CASCADE;
DROP TABLE IF EXISTS Delivery CASCADE;
DROP TABLE IF EXISTS Order_ CASCADE;


CREATE TABLE Customer (
  cust_no INT PRIMARY KEY,
  name VARCHAR,
  email VARCHAR UNIQUE,
  phone NUMERIC(9),
  address VARCHAR
);

CREATE TABLE Order_ (
  order_no INT PRIMARY KEY,
  date DATE,
  cust_no INT  NOT NULL,
  FOREIGN KEY (cust_no) REFERENCES Customer(cust_no)
);

CREATE TABLE Sale (
  order_no INT PRIMARY KEY,
  FOREIGN KEY (order_no) REFERENCES Order_(order_no)
);

CREATE TABLE pay (
  order_no INT,
  cust_no INT NOT NULL,
  PRIMARY KEY (order_no, cust_no),
  FOREIGN KEY (order_no) REFERENCES Order_(order_no),
  FOREIGN KEY (cust_no) REFERENCES Customer(cust_no)
);

CREATE TABLE Employee (
  ssn VARCHAR(11) PRIMARY KEY,
  TIN NUMERIC(9, 0) UNIQUE,
  bdate DATE,
  name VARCHAR
);

CREATE TABLE process (
  ssn VARCHAR(11),
  order_no INT,
  PRIMARY KEY (ssn, order_no),
  FOREIGN KEY (ssn) REFERENCES Employee(ssn),
  FOREIGN KEY (order_no) REFERENCES Order_(order_no)
);

CREATE TABLE Department (
  name VARCHAR PRIMARY KEY
);

CREATE TABLE Workplace (
  address VARCHAR PRIMARY KEY,
  latitude NUMERIC(6, 4),
  longitude NUMERIC(7, 4),
  UNIQUE(latitude, longitude)
);

CREATE TABLE works (
  ssn VARCHAR(11),
  name VARCHAR,
  address VARCHAR,
  PRIMARY KEY (ssn, name, address),
  FOREIGN KEY (ssn) REFERENCES Employee(ssn),
  FOREIGN KEY (name) REFERENCES Department(name),
  FOREIGN KEY (address) REFERENCES Workplace(address)
);

CREATE TABLE Office (
  address VARCHAR PRIMARY KEY,
  FOREIGN KEY (address) REFERENCES Workplace(address)
);

CREATE TABLE Warehouse (
  address VARCHAR PRIMARY KEY,
  FOREIGN KEY (address) REFERENCES Workplace(address)
);

CREATE TABLE Product (
  sku VARCHAR PRIMARY KEY,
  name VARCHAR,
  description VARCHAR,
  price INT     -- in cents
);


CREATE TABLE EAN_Product (
  sku VARCHAR PRIMARY KEY,
  ean NUMERIC(13, 0),
  FOREIGN KEY (sku) REFERENCES Product(sku)
);

CREATE TABLE Supplier (
  TIN NUMERIC(9, 0) PRIMARY KEY,
  name VARCHAR,
  address VARCHAR
);

CREATE TABLE contains_ (
  order_no INT,
  sku VARCHAR ,
  quantity INT CHECK (quantity > 0),
  PRIMARY KEY (order_no, sku),
  FOREIGN KEY (order_no) REFERENCES Order_(order_no),
  FOREIGN KEY (sku) REFERENCES Product(sku)
);

CREATE TABLE supply_contract (
  TIN NUMERIC(9, 0),
  sku VARCHAR,
  date DATE,
  PRIMARY KEY (TIN, sku),
  FOREIGN KEY (TIN) REFERENCES Supplier(TIN),
  FOREIGN KEY (sku) REFERENCES Product(sku)
);

CREATE TABLE Delivery (
  address VARCHAR,
  TIN NUMERIC(9, 0),
  PRIMARY KEY (address, TIN),
  FOREIGN KEY (address) REFERENCES Warehouse(address),
  FOREIGN KEY (TIN) REFERENCES Supplier(TIN)
);