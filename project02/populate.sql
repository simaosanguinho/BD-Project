INSERT INTO Customer
VALUES
(13, 'João Faria', 'joao.faria@gmail.com', '913789392', 'Rua Camoes, 123'),
(2, 'Jorge Nunes', 'jorge.n@hotmail.com', '987712312', 'Rua Amarela, 123'),
(35, 'Ana Lampreia', 'ana.lamp@gmailcom', '91203456', 'Rua dos Cravos, 12');

INSERT INTO Order_
VALUES
(101, '2023-05-01', 13),
(102, '2023-05-02', 2),
(103, '2023-05-03', 35);

INSERT INTO Sale
VALUES
(101),
(102);

INSERT INTO pay 
VALUES
(101, 13),
(102, 2);

INSERT INTO Employee
VALUES
('12345678910', 243678525, '1999-01-01', 'Sofia Barbosa'),
('10987654321', 125637263, '1985-05-10', 'Diogo Silva');

INSERT INTO process
VALUES
('12345678910', 101),
('10987654321', 102);

INSERT INTO Department
VALUES
('Sales'),
('Accounting');

INSERT INTO Workplace 
VALUES
('Rua 25 de Abril, 15', 37.1234, -122.5678),
('Avenida das Pombas, 2', 38.9876, -121.3456);


INSERT INTO works 
VALUES
('12345678910', 'Sales', 'Rua 25 de Abril, 15'),
('10987654321', 'Accounting', 'Avenida das Pombas, 2');

INSERT INTO Office 
VALUES
('Rua 25 de Abril, 15');

INSERT INTO Warehouse 
VALUES
('Avenida das Pombas, 2');

INSERT INTO Product 
VALUES
('1001A', 'Caneta', 'caneta preta', 100),
('1002B', 'Móvel', 'móvel branco de madeira', 3500),
('1003C', 'Cama', 'Cama Queen-Size', 29900);

INSERT INTO EAN_Product
VALUES
('1001A', 5607260022122),
('1002B', 5602727273111);

INSERT INTO Supplier
VALUES
(983747222, 'Joana Pereira', 'Rua Verde, 230'),
(124455551, 'Jacinto Torres', 'Rua Azul, 123'),
(525258733, 'Miguel Leal', 'Rua Camoes, 17');

INSERT INTO contains_
VALUES
(101, '1001A', 2),
(102, '1002B', 1),
(103, '1003C', 1);

INSERT INTO supply_contract
VALUES
(983747222, '1001A', '2022-05-01'),
(124455551, '1002B', '2022-05-02'),
(525258733, '1003C', '2022-05-03');



INSERT INTO Delivery
VALUES
('Avenida das Pombas, 2', 983747222),
('Avenida das Pombas, 2', 124455551),
('Avenida das Pombas, 2', 525258733);
