-- Borrado tablas si estás trabajando en usuario system
-- Ejecutar desde usuario system
drop table rents cascade constraints;

drop table rooms cascade constraints;

drop table payments;

drop table houses cascade constraints;

drop table addresses;

drop table users;

-- Borrado tablas si estás trabajando en otro usuario que no sea system
-- Ejecutar desde usuario system
BEGIN
   FOR t IN (SELECT table_name FROM all_tables WHERE owner = 'RENTASTAY') LOOP
      EXECUTE IMMEDIATE 'DROP TABLE RENTASTAY.' || t.table_name || ' CASCADE CONSTRAINTS';
   END LOOP;
END;
/

-- Borrado funciones si estás trabajando en otro usuario que no sea system
BEGIN
   FOR f IN (SELECT object_name FROM all_objects WHERE object_type = 'FUNCTION' AND owner = 'RENTASTAY') LOOP
      EXECUTE IMMEDIATE 'DROP FUNCTION RENTASTAY.' || f.object_name;
   END LOOP;
END;
/

-- Borrado secuencias si estás trabajando en otro usuario que no sea system
BEGIN
   FOR s IN (SELECT sequence_name FROM all_sequences WHERE sequence_owner = 'RENTASTAY' AND sequence_name NOT LIKE 'ISEQ$%') LOOP
      EXECUTE IMMEDIATE 'DROP SEQUENCE RENTASTAY.' || s.sequence_name;
   END LOOP;
END;
/