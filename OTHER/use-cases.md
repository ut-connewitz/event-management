# use cases


## volunteering notification
1. Eine allgemeine, userbezogene Einstellungsmöglichkeit liegt in `Setting`, zum Beispiel
> Erinnerung an einem gewählten Task `X` Stunden vor Beginn
>

mit `setting_name="volunteering notification"`

2. `SettingType` wäre vlt sowas wie `USER_SPECIFIC_GLOBAL` und `ValueType` `INT`

3. User A hat auf einer Einstellungsseite die Möglichkeit in einem Feld eine Stundenzahl einzugeben, zum Beispiel 10.

5. In der `UserSettingValue` Tabelle wird ein Eintrag mit `username`("A"), `setting_name`("volunteering notification") und `id`(1) erzeugt, womit erstmal nur die spezifische Einstellung identifiziert wird.

6. Der eigentliche Wert liegt in einer der drei ISA Tabellen, in diesem Fall in `IntValue`, weil sonst alle `UserSettingValue` für jeden insgesamt möglichen Datentyp ein eigenes Attribut bräuchten, in denen für jeden ungenutzten Typ Null Werte lägen.

7. User A meldet sich für einen `Task` und es entsteht eine `Volunteering` Instanz, welche eine `VolunteeringNotification` triggert.

8. jetzt schaut die `VolunteeringNotification` mit dem gegebenen `username="A"` in  `UserSettingValue JOIN Setting on setting_name` nach, ob Einstellungen mit `SettingType=USER_SPECIFIC_GLOBAL` vorhanden sind.

9. es findet die Einstellung mit der `id=1` und sieht den `ValueType=INT`

10. Der konkrete Wert muss also in der `IntValue` Tabelle liegen, wo er über die `user_setting_value_id` gefunden werden kann

11. Die `Notification` berechnet und speichert anhand dem `int_value=10`, wann sie abgeschickt werden soll.
