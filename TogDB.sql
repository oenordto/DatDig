CREATE TABLE Jernbanestasjon(
    JernbanestasjonID INTEGER NOT NULL,
    JernbanestasjonNavn VARCHAR(30) NOT NULL UNIQUE,
    Moh INTEGER NOT NULL,
    CONSTRAINT Jernbanestasjon_PK PRIMARY KEY (JernbanestasjonID)
);

CREATE TABLE Operator(
    OperatorID INTEGER NOT NULL,
    OperatorNavn VARCHAR(30) NOT NULL UNIQUE,
    CONSTRAINT Operator_PK PRIMARY KEY (OperatorID)
);

CREATE TABLE Ukedag(
    UkedagID INTEGER NOT NULL,
    Ukedag VARCHAR NOT NULL UNIQUE,
    CONSTRAINT Ukedag_PK PRIMARY KEY (UkedagID)
);

CREATE TABLE Kunde(
    KundeNr INTEGER NOT NULL,
    Navn VARCHAR(30) NOT NULL, 
    Epost VARCHAR(30) NOT NULL UNIQUE,
    TelefonNr INTEGER NOT NULL UNIQUE,
    CONSTRAINT Kunde_PK PRIMARY KEY (KundeNr)
);

CREATE TABLE KundeOrdre(
    OrdreNr INTEGER NOT NULL,
    KjopsDato VARCHAR(30) NOT NULL,
    KjopsKlokkeslett VARCHAR(30) NOT NULL,
    KundeNr INTEGER NOT NULL,
    CONSTRAINT KundeOrdre_PK PRIMARY KEY (OrdreNr),
    CONSTRAINT KundeOrdre_FK FOREIGN KEY (KundeNr) REFERENCES Kunde(KundeNr)
        ON UPDATE CASCADE
        ON DELETE CASCADE
);

CREATE TABLE Banestrekning(
    BanestrekningID INTEGER NOT NULL,
    BanestrekningNavn VARCHAR(30) NOT NULL UNIQUE,
    Fremdriftsenergi VARCHAR NOT NULL,
    StartStasjon INTEGER NOT NULL,
    SluttStasjon INTEGER NOT NULL,
    CONSTRAINT Banestrekning_PK PRIMARY KEY (BanestrekningID),
    CONSTRAINT Banestrekning_FK1 FOREIGN KEY (StartStasjon) REFERENCES Jernbanestasjon(JernbanestasjonID)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    CONSTRAINT Banestrekning_FK2 FOREIGN KEY (SluttStasjon) REFERENCES Jernbanestasjon(JernbanestasjonID)
        ON UPDATE CASCADE
        ON DELETE CASCADE
);

CREATE TABLE Togrute(
    TogruteID INTEGER NOT NULL,
    TogruteNavn VARCHAR(50) NOT NULL UNIQUE,
    Avgang VARCHAR(30) NOT NULL,
    Ankomst VARCHAR(30) NOT NULL,
    OperatorID INTEGER NOT NULL,
    StartStasjon INTEGER NOT NULL,
    SluttStasjon INTEGER NOT NULL, 
    BanestrekningID INTEGER NOT NULL,
    CONSTRAINT Togrute_PK PRIMARY KEY (TogruteID),
    CONSTRAINT Togrute_FK1 FOREIGN KEY (OperatorID) REFERENCES Operator(OperatorID)
        ON UPDATE CASCADE
        ON DELETE CASCADE,    
    CONSTRAINT Togrute_FK2 FOREIGN KEY (StartStasjon) REFERENCES Jernbanestasjon(JernbanestasjonID)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    CONSTRAINT Togrute_FK3 FOREIGN KEY (SluttStasjon) REFERENCES Jernbanestasjon(JernbanestasjonID)
        ON UPDATE CASCADE
        ON DELETE CASCADE, 
    CONSTRAINT Togrute_FK4 FOREIGN KEY (BanestrekningID) REFERENCES Banestrekning(BanestrekningID)
        ON UPDATE CASCADE
        ON DELETE CASCADE
);

CREATE TABLE Togrute_Ukedag(
    TogruteID INTEGER NOT NULL,
    UkedagID INTEGER NOT NULL,
    CONSTRAINT Togrute_Ukedag_PK PRIMARY KEY (TogruteID, UkedagID),
    CONSTRAINT Togrute_Ukedag_FK1 FOREIGN KEY (TogruteID) REFERENCES Togrute(TogruteID)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    CONSTRAINT Togrute_Ukedag_FK2 FOREIGN KEY (UkedagID) REFERENCES Ukedag(UkedagID)
        ON UPDATE CASCADE
        ON DELETE CASCADE
);

CREATE TABLE Togruteforekomst(
    TogruteforekomstID INTEGER NOT NULL,
    Dato VARCHAR(30) NOT NULL,
    TogruteID INTEGER NOT NULL,
    CONSTRAINT TogruteforekomstID_PK PRIMARY KEY (TogruteforekomstID),
    CONSTRAINT TogruteforekomstID_FK FOREIGN KEY (TogruteID) REFERENCES Togrute(TogruteID)
        ON UPDATE CASCADE
        ON DELETE CASCADE
);

CREATE TABLE Billett(
    BillettID INTEGER NOT NULL,
    PlassNr INTEGER NOT NULL,
    VognID INTEGER NOT NULL,
    OrdreNr INTEGER NOT NULL,
    TogruteforekomstID INTEGER NOT NULL,
    StartStasjon INTEGER NOT NULL,
    SluttStasjon INTEGER NOT NULL, 
    CONSTRAINT Billett_PK PRIMARY KEY (BillettID),
    CONSTRAINT Billett_FK1 FOREIGN KEY (VognID) REFERENCES Vogn(VognID)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    CONSTRAINT Billett_FK2 FOREIGN KEY (OrdreNr) REFERENCES KundeOrdre(OrdreNr)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    CONSTRAINT Billett_FK3 FOREIGN KEY (TogruteforekomstID) REFERENCES Togruteforekomst(TogruteforekomstID)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    CONSTRAINT Togrute_FK4 FOREIGN KEY (StartStasjon) REFERENCES Jernbanestasjon(JernbanestasjonID)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    CONSTRAINT Togrute_FK5 FOREIGN KEY (SluttStasjon) REFERENCES Jernbanestasjon(JernbanestasjonID)
        ON UPDATE CASCADE
        ON DELETE CASCADE
);

CREATE TABLE Delstrekning(
    DelstrekningID INTEGER NOT NULL,
    Lengde INTEGER NOT NULL,
    Sportype INTEGER NOT NULL,
    Stasjon1 INTEGER NOT NULL,
    Stasjon2 INTEGER NOT NULL,
    BanestrekningID INTEGER NOT NULL,
    CONSTRAINT Delstrekning_PK PRIMARY KEY (DelstrekningID),
    CONSTRAINT Delstrekning_FK1 FOREIGN KEY (Stasjon1) REFERENCES Jernbanestasjon(JernbanestasjonID)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    CONSTRAINT Delstrekning_FK2 FOREIGN KEY (Stasjon2) REFERENCES Jernbanestasjon(JernbanestasjonID)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    CONSTRAINT Delstrekning_FK3 FOREIGN KEY (BanestrekningID) REFERENCES Banestrekning(BanestrekningID)
        ON UPDATE CASCADE
        ON DELETE CASCADE
);

CREATE TABLE MellomStopp(
    TogruteID INTEGER NOT NULL,
    JernbanestasjonID INTEGER NOT NULL,
    Avgang VARCHAR(30),
    Ankomst VARCHAR(30),
    CONSTRAINT MellomStopp_PK PRIMARY KEY (TogruteID, JernbanestasjonID),
    CONSTRAINT MellomStopp_FK1 FOREIGN KEY (TogruteID) REFERENCES Togrute(TogruteID)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    CONSTRAINT MellomStopp_FK2 FOREIGN KEY (JernbanestasjonID) REFERENCES Jernbanestasjon(JernbanestasjonID)
        ON UPDATE CASCADE
        ON DELETE CASCADE
);

CREATE TABLE Togrute_Delstrekning(
    TogruteID INTEGER NOT NULL,
    DelstrekningID INTEGER NOT NULL,
    CONSTRAINT Togrute_Delstrekning_PK PRIMARY KEY (TogruteID, DelstrekningID),
    CONSTRAINT Togrute_Delstrekning_FK1 FOREIGN KEY (TogruteID) REFERENCES Togrute(TogruteID)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    CONSTRAINT Togrute_Delstrekning_FK2 FOREIGN KEY (DelstrekningID) REFERENCES Delstrekning(DelstrekningID)
        ON UPDATE CASCADE
        ON DELETE CASCADE
);

CREATE TABLE Vogn(
    VognID INTEGER NOT NULL,
    Navn VARCHAR(30) NOT NULL,
    VognNr INTEGER NOT NULL,
    TogruteID INTEGER NOT NULL,
    CONSTRAINT Vogn_PK PRIMARY KEY (VognID),
    CONSTRAINT Vogn_FK FOREIGN KEY (TogruteID) REFERENCES Togrute(TogruteID)
        ON UPDATE CASCADE
        ON DELETE CASCADE
);

CREATE TABLE Sittevogn(
    VognID INTEGER NOT NULL,
    AntallStolrader INTEGER NOT NULL,
    AntallSeter INTEGER NOT NULL,
    CONSTRAINT Sittevogn_PK PRIMARY KEY (VognID),
    CONSTRAINT Sittevogn_FK FOREIGN KEY (VognID) REFERENCES Vogn(VognID)
        ON UPDATE CASCADE
        ON DELETE CASCADE
);

CREATE TABLE Sovevogn(
    VognID INTEGER NOT NULL,
    AntallSovekupeer INTEGER NOT NULL,
    CONSTRAINT Sovevogn_PK PRIMARY KEY (VognID),
    CONSTRAINT Sovevogn_FK FOREIGN KEY (VognID) REFERENCES Vogn(VognID)
        ON UPDATE CASCADE
        ON DELETE CASCADE
);