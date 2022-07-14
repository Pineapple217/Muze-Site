from datetime import datetime

from leden.models import Lid

def export_shiftlist():
    f = open(f"{datetime.now().strftime('%d-%m-%Y %H-%M-%S')}.csv", "x")
    f.write("Naam,voornaam,email,tel,geboortedatum,gender,straat,huisnr,woonplaats,postcode,discordid,media\n")
    for lid in Lid.objects.all():
        f.write(f"{lid.user.last_name},{lid.user.first_name},{lid.user.email},{lid.tel},{lid.date_of_birth},{lid.gender},{lid.street},{lid.house_number},{lid.residence},{lid.zipcode},{lid.discord_id},{lid.media}\n")
    f.close()