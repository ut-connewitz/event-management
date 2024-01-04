-- create index --
--Indizes sollten im eigens dafür vorgesehenen tablespace INDX erstellt--

--benutzerdefinierter basic lexer--
begin
   ctx_ddl.create_preference('mylexer', 'BASIC_LEXER' );
   ctx_ddl.set_attribute ( 'mylexer', 'mixed_case', 'NO' );
end;
/

--storage preference--
begin
   ctx_ddl.create_preference('mystore', 'BASIC_STORAGE');
   ctx_ddl.set_attribute('mystore', 'I_TABLE_CLAUSE', 'tablespace INDX');
   ctx_ddl.set_attribute('mystore', 'K_TABLE_CLAUSE', 'tablespace INDX');
   ctx_ddl.set_attribute('mystore', 'R_TABLE_CLAUSE', 'tablespace INDX');
   ctx_ddl.set_attribute('mystore', 'N_TABLE_CLAUSE', 'tablespace INDX');
   ctx_ddl.set_attribute('mystore', 'I_INDEX_CLAUSE', 'tablespace INDX');
   ctx_ddl.set_attribute('mystore', 'P_TABLE_CLAUSE', 'tablespace INDX');
end;
/

--index press text--
CREATE INDEX press_text ON UT_Event(PressText)
   INDEXTYPE IS CTXSYS.CONTEXT
   PARAMETERS ( 'LEXER mylexer STORAGE mystore SYNC (ON COMMIT)' );

--index description text--
CREATE INDEX description_text ON UT_Event(Description)
   INDEXTYPE IS CTXSYS.CONTEXT
   PARAMETERS ( 'LEXER mylexer STORAGE mystore SYNC (ON COMMIT)' );

   --index title text--
CREATE INDEX title_text ON UT_Event(EventTitle)
   INDEXTYPE IS CTXSYS.CONTEXT
   PARAMETERS ( 'LEXER mylexer STORAGE mystore SYNC (ON COMMIT)' );

   --index audio description text--
CREATE INDEX audio_text ON UT_Event(AudioDescription)
   INDEXTYPE IS CTXSYS.CONTEXT
   PARAMETERS ( 'LEXER mylexer STORAGE mystore SYNC (ON COMMIT)' );

   --index light description text--
CREATE INDEX light_text ON UT_Event(LightDescription)
   INDEXTYPE IS CTXSYS.CONTEXT
   PARAMETERS ( 'LEXER mylexer STORAGE mystore SYNC (ON COMMIT)' );
