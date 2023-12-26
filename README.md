# Hvit Jul

Dette systemet svarer på spørsmålet "Var det en hvit jul her tidligere?".

Appen er publisert på https://hvitjul.streamlit.app

**NOTE:** It is only documented in Norwegian as it only works in Norway and is written for use in Norway

## Om prosjektet
Denne løsningen var et hobbyprosjekt i jula 2023 av Andreas P. Lorentzen og Johannes P. Lorentzen som startet i en diskusjon og endte med implementasjon. Vi håper at du og dere liker løsningen, og at det kanskje hjelper med å løse en diskusjon hos dere også.

Løsningen benytter NVE sin API for xgeo.no, som gir data om beregnet snødybde for et gitt punkt. Dette gjorde det enkelt for oss, men er ikke like presist som å bruke målinger fra målestasjoner. API-et leverer data tilbake til 1957, som derfor er satt som tidligste år. Vi bruker Kartverket sin stedsnavn-API for å hente stedsnavn.

Alt er implementert i Python ved bruk av pakken streamlit. Bruker du Python, så anbefaler vi å prøve den ut. Det er derimot noen svakheter med systemet. Spesielt en vi ikke har klart å løse med en treg markør i kartet. Hvis du vil titte på kildekoden ligger den tilgjengelig på GitHub.

Hvis du ønsker å ta kontakt, gjør det gjerne gjennom LinkedIn.

Andreas: https://www.linkedin.com/in/andreas-p-lorentzen

Johannes: https://www.linkedin.com/in/pippidis

God jul

## Hvirkemåte
Appen er tar en posisjon og finner stedsnavn og historisk snø-data fra NVE sitt gts api. Det samme som benyttes i www.xgeo.no og presenterer det på en enkel grafisk måte som svarer på spørsmålet om det var en hvit jul.

## Oppbyggning
