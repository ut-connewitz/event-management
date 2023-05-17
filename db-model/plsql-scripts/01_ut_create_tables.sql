--create tables--

create table UT_Event (
    EventID number(7) primary key,
    EventTitle varchar2(100) not null,
    EventType varchar2(50),
    PressText varchar2(1000),
    Description varchar2(2000),
    PreOrderPrice float(2),
    AudioDescription varchar2(500),
    LightDescription varchar2(500),
    EventImage blob,
    EventLinks varchar2(1000)
);

create sequence UT_sequence_EventID
minvalue 1
start with 1
increment by 1
cache 10;

create table UT_EventDay (
    EventDate date primary key,
    EventID number(7) not null,
    constraint FK_EventDay foreign key (EventID)
    references UT_Event(EventID) on delete cascade,
    EventTime timestamp not null,
    EventDuration float(2),
    AdmissionTime timestamp,
    KitchenTime timestamp,
    WorkBegin timestamp,
    VolunteersNeeded number(3)
);

create table UT_Management (
    Username varchar2(20) primary key,
    Password varchar2(30) not null,
    Email varchar2(50) not null
);

create table UT_Volunteer (
    UT_Identifier varchar2(20) primary key,
    Name varchar2(20) not null,
    Email varchar2(30),
    Address varchar2(100),
    TelNumber varchar2(20)
);

create table UT_Team (
    TeamName varchar2(20) primary key
);

create table UT_Act (
    ActName varchar2(50) primary key,
    ActFood varchar2(500),
    PersonCount number(3),
    ActLink varchar2(500),
    MusicExample blob
);

create table UT_Responsibility (
    Username varchar2(30) not null,
    constraint FK_Username_Responsibility foreign key (Username)
    references UT_Management(Username) on delete cascade,
    EventID number(7) not null,
    constraint FK_EventID_Responsibility foreign key (EventID)
    references UT_Event(EventID) on delete cascade,
    PRIMARY KEY (Username, EventID)
);

create table UT_Help (
    UT_Identifier varchar2(20) not null,
    constraint FK_Volunteer_Help foreign key (UT_Identifier)
    references UT_Volunteer(UT_Identifier),
    EventDate date not null,
    constraint FK_EventDay_Help foreign key (EventDate)
    references UT_EventDay(EventDate),
    PRIMARY KEY (UT_Identifier, EventDate),
    HelpType varchar2(20),
    Commitment varchar2(20)
);

create table UT_Volunteer_Team (
    UT_Identifier varchar2(20) not null,
    constraint FK_Volunteer_Volunteer_Team foreign key (UT_Identifier)
    references UT_Volunteer(UT_Identifier),
    TeamName varchar2(20)  not null,
    constraint FK_Team_Volunteer_Team foreign key (TeamName)
    references UT_Team(TeamName),
    PRIMARY KEY (UT_Identifier, TeamName)
);

create table UT_Event_Act (
    ActName varchar2(50) not null,
    constraint FK_Act_Event_Act foreign key (ActName)
    references UT_Act(ActName),
    EventID number(7) not null,
    constraint FK_Event_Event_Act foreign key (EventID)
    references UT_Event(EventID),
    PRIMARY KEY (ActName, EventID)
);
