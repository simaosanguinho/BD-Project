BEGIN;
INSERT INTO workplace VALUES ('Test Address 2', 34.052235, -118.243683);
INSERT INTO warehouse VALUES ('Test Address 2');
COMMIT;

DELETE FROM warehouse WHERE address = 'Test Address 2';
DELETE FROM workplace WHERE address = 'Test Address 2';
