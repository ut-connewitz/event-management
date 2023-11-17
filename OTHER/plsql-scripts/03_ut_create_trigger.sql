--trigger --
create or replace trigger UT_Event_ID
before insert on UT_Event
for each row
when (new.EventID is null)
begin
    :new.EventID := UT_sequence_EventID.nextval;
end;
