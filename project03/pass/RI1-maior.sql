BEGIN;
INSERT INTO employee
VALUES
('5001', '9001', '1985-05-10', 'Diogo MaiordeIdade');
COMMIT;

BEGIN;
DELETE FROM employee WHERE ssn='5001';
COMMIT;
