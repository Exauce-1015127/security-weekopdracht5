# security-weekopdracht5

# Hoe werkt Encrypten
- Run de applicatie in main.py
- Vul een tekst in die je wilt encrypten. Vervolgens klik je op de button 'Versleutel bericht'.
- De tekst wordt versleuteld en weergegeven als key, nonce, ciphertext en tag.
- Klik op de download button om de gegevens te bewaren in een json bestand of kopieer de tekst naar een eigen bestand.
- Deel dit bestand met de ontvanger van het bericht.

# Hoe werkt Decrypten
- Run de applicatie in main.py
- Voer de ontvangen key, nonce, ciphertext en tag in op de daarvoor bestemde invoervelden.
- Klik op de button 'Ontsleutel bericht'.
- De oorspronkelijke tekst wordt weergegeven.

# Encryptie methode en algoritme
De encryptie methode die gebruikt wordt is symmetrische encryptie.
Het algoritme dat gebruikt wordt is AES (Advanced Encryption Standard).
Dit algoritme is gekozen omdat het een van de meest gebruikte en veilige encryptie standaarden is,
vanwege snelheid en efficiëntie.

# Behandeling van symmetrische sleutels
Bij iedere encryptie wordt een nieuwe unieke symmetrische sleutel gegenereerd.
Deze sleutel wordt niet opgeslagen in de applicatie, maar juist weergegeven aan de gebruiker 
om te kopiëren of te downloaden. Hier kan zowel positief als negatief over gedacht worden.

Positief omdat de sleutel niet ergens opgeslagen wordt waar deze mogelijk gestolen kan worden. 
Daarnaast kan er geen gespreksgeschiedenis achterhaald worden, 
omdat er geen database is voor gebruikers en hun verzonden berichten.

Negatief omdat de gebruiker zelf verantwoordelijk is voor het veilig bewaren van de sleutel.
Als de sleutel verloren gaat, kan het bericht niet meer ontsleuteld worden. 
Daarnaast kan er geen extra salting worden toegepast met behulp van wachtwoorden, omdat er geen inlog systeem is.


# Reflectie Kerckhoff's principe
Kerckhoff's principe stelt dat een cryptosysteem veilig moet zijn, zelfs als alles over het systeem bekend is, behalve de sleutel. 
In deze applicatie wordt dit principe nageleefd door gebruik te maken van een sterk en algemeen bekend algoritme (AES) voor encryptie.
De keys blijven geheim doordat het pas wordt gegenereerd en getoond aan de gebruiker bij het encrypten van een bericht.
Nadat de gebruiker deze keys heeft gekopieerd of gedownload, worden ze niet opgeslagen in de applicatie.
Zelfs als een aanvaller het algoritme en de werking van de applicatie kent, 
kan hij geen toegang krijgen tot de versleutelde berichten zonder de juiste sleutel.