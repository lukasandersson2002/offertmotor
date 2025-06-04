# Offertmotor för laddboxar

## Beskrivning
Det här är en Flask-app som tar emot offertförfrågningar för laddboxar, genererar PDF-offert med AI-rekommendation, skickar via e-post och visar inkomna förfrågningar i en adminpanel.

## Kör lokalt

Installera dependencies:pip install -r requirements.txt
 Kör appen:python app.py

 Besök:
- http://localhost:5000/  (formulär)
- http://localhost:5000/admin (adminpanel)

## Konfigurera e-post

Ändra `MAIL_USERNAME` och `MAIL_PASSWORD` i `app.py` till din Gmail och app-lösenord.

## Deploy

Följ instruktionerna för att deploya på Render eller annan server.
git add .
git commit -m "Lägger till offertmotor med AI, pdf, mail och adminpanel"
git push origin main
   
