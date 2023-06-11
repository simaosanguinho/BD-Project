BEGIN;
INSERT INTO workplace VALUES ('Test Address 1', 40.712776, -74.005974);
INSERT INTO office VALUES ('Test Address 1');
COMMIT;

DELETE FROM office WHERE address = 'Test Address 1';
DELETE FROM workplace WHERE address = 'Test Address 1';
