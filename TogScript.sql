INSERT INTO Jernbanestasjon VALUES (null, "Trondheim", 5.1);
INSERT INTO Jernbanestasjon VALUES (null, "Steinkjer", 3.6);
INSERT INTO Jernbanestasjon VALUES (null, "Mosjøen", 6.8);
INSERT INTO Jernbanestasjon VALUES (null, "Mo i Rana", 3.5);
INSERT INTO Jernbanestasjon VALUES (null, "Fauske", 34.0);
INSERT INTO Jernbanestasjon VALUES (null, "Bodø", 4.1);

INSERT INTO Banestrekning VALUES (null, "Nordlandsbanen", "Diesel", 1, 6);

INSERT INTO Delstrekning VALUES (null, 120, "Dobbeltspor", 1, 2, 1);
INSERT INTO Delstrekning VALUES (null, 280, "Enkeltspor", 3, 2, 1);
INSERT INTO Delstrekning VALUES (null, 90, "Enkeltspor", 3, 4, 1);
INSERT INTO Delstrekning VALUES (null, 170, "Enkeltspor", 5, 4, 1);
INSERT INTO Delstrekning VALUES (null, 60, "Enkeltspor", 5, 6, 1);

INSERT INTO Operator VALUES (null, "SJ");

INSERT INTO Ukedag VALUES (null, "Mandag");
INSERT INTO Ukedag VALUES (null, "Tirsdag");
INSERT INTO Ukedag VALUES (null, "Onsdag");
INSERT INTO Ukedag VALUES (null, "Torsdag");
INSERT INTO Ukedag VALUES (null, "Fredag");
INSERT INTO Ukedag VALUES (null, "Lørdag");
INSERT INTO Ukedag VALUES (null, "Søndag");

INSERT INTO Togrute VALUES (null, "Dagtog fra Trondheim til Bodø", "07:49", "17:34", 1, 1, 6, 1);
INSERT INTO Togrute VALUES (null, "Nattog fra Trondheim til Bodø", "23:05", "09:05", 1, 1, 6, 1);
INSERT INTO Togrute VALUES (null, "Morgentog fra Mo i Rana til Trondheim", "08:11", "14:13", 1, 4, 1, 1);

INSERT INTO Vogn VALUES (null, "SJ-Sittevogn-1", 1, 1);
INSERT INTO Vogn VALUES (null, "SJ-Sittevogn-1", 2, 1);
INSERT INTO Sittevogn VALUES (1, 3, 12);
INSERT INTO Sittevogn VALUES (2, 3, 12);

INSERT INTO Vogn VALUES (null, "SJ-Sittevogn-1", 1, 2);
INSERT INTO Vogn VALUES (null, "SJ-Sovevogn-1", 2, 2);
INSERT INTO Sittevogn VALUES (3, 3, 12);
INSERT INTO Sovevogn VALUES (4, 4);

INSERT INTO Vogn VALUES (null, "SJ-Sittevogn-1", 1, 3);
INSERT INTO Sittevogn VALUES (5, 3, 12);

INSERT INTO Togrute_Ukedag VALUES (1, 1);
INSERT INTO Togrute_Ukedag VALUES (1, 2);
INSERT INTO Togrute_Ukedag VALUES (1, 3);
INSERT INTO Togrute_Ukedag VALUES (1, 4);
INSERT INTO Togrute_Ukedag VALUES (1, 5);

INSERT INTO Togrute_Ukedag VALUES (2, 1);
INSERT INTO Togrute_Ukedag VALUES (2, 2);
INSERT INTO Togrute_Ukedag VALUES (2, 3);
INSERT INTO Togrute_Ukedag VALUES (2, 4);
INSERT INTO Togrute_Ukedag VALUES (2, 5);
INSERT INTO Togrute_Ukedag VALUES (2, 6);
INSERT INTO Togrute_Ukedag VALUES (2, 7);

INSERT INTO Togrute_Ukedag VALUES (3, 1);
INSERT INTO Togrute_Ukedag VALUES (3, 2);
INSERT INTO Togrute_Ukedag VALUES (3, 3);
INSERT INTO Togrute_Ukedag VALUES (3, 4);
INSERT INTO Togrute_Ukedag VALUES (3, 5);

INSERT INTO MellomStopp VALUES (1, 2, "09:51", "09:49");
INSERT INTO MellomStopp VALUES (1, 3, "13:20", "13:18");
INSERT INTO MellomStopp VALUES (1, 4, "14:31", "14:29");
INSERT INTO MellomStopp VALUES (1, 5, "16:49", "16:47");

INSERT INTO MellomStopp VALUES (2, 2, "00:59", "00:57");
INSERT INTO MellomStopp VALUES (2, 3, "04:41", "04:39");
INSERT INTO MellomStopp VALUES (2, 4, "05:55", "05:53");
INSERT INTO MellomStopp VALUES (2, 5, "08:19", "08:17");

INSERT INTO MellomStopp VALUES (3, 3, "09:14", "09:12");
INSERT INTO MellomStopp VALUES (3, 2, "12:31", "12:29");

INSERT INTO Togrute_Delstrekning VALUES (1, 1);
INSERT INTO Togrute_Delstrekning VALUES (1, 2);
INSERT INTO Togrute_Delstrekning VALUES (1, 3);
INSERT INTO Togrute_Delstrekning VALUES (1, 4);
INSERT INTO Togrute_Delstrekning VALUES (1, 5);

INSERT INTO Togrute_Delstrekning VALUES (2, 1);
INSERT INTO Togrute_Delstrekning VALUES (2, 2);
INSERT INTO Togrute_Delstrekning VALUES (2, 3);
INSERT INTO Togrute_Delstrekning VALUES (2, 4);
INSERT INTO Togrute_Delstrekning VALUES (2, 5);

INSERT INTO Togrute_Delstrekning VALUES (3, 3);
INSERT INTO Togrute_Delstrekning VALUES (3, 2);
INSERT INTO Togrute_Delstrekning VALUES (3, 1);
 
INSERT INTO Togruteforekomst VALUES (null, "03.04.2023" ,1);
INSERT INTO Togruteforekomst VALUES (null, "03.04.2023" ,2);
INSERT INTO Togruteforekomst VALUES (null, "03.04.2023" ,3);
INSERT INTO Togruteforekomst VALUES (null, "04.04.2023" ,1);
INSERT INTO Togruteforekomst VALUES (null, "04.04.2023" ,2);
INSERT INTO Togruteforekomst VALUES (null, "04.04.2023" ,3);