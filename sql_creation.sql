CREATE TABLE dataprocessor (
    id integer NOT NULL,
    name character varying(100) NOT NULL,
    state character varying(100) NOT NULL,
    country character varying(100) NOT NULL
);

INSERT INTO dataprocessor(id,name,state,country)
values(1,'test1','state1','country1');
--
INSERT INTO dataprocessor(id,name,state,country)
values(2,'test2','state2','country2');
--
INSERT INTO dataprocessor(id,name,state,country)
values(3,'test1','state1','country1');
--
INSERT INTO dataprocessor(id,name,state,country)
values(4,'test4','state4','country4');
--
INSERT INTO dataprocessor(id,name,state,country)
values(5,'test5','state5','country5');
--
INSERT INTO dataprocessor(id,name,state,country)
values(6,'test6','state6','country6');
--
INSERT INTO dataprocessor(id,name,state,country)
values(7,'test7','state7','country7');
--
INSERT INTO dataprocessor(id,name,state,country)
values(8,'test8','state8','country8');
--
INSERT INTO dataprocessor(id,name,state,country)
values(9,'test9','state9','country9');
--
INSERT INTO dataprocessor(id,name,state,country)
values(10,'test10','state10','country10');
--
commit;