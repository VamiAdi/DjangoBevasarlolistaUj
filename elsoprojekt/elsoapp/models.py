from django.db import models

# Create your models here.


class Tanulo(models.Model):

	nev = models.CharField(max_length=128)
	fnev = models.CharField(max_length=128)
	jelszo = models.CharField(max_length=128)
	email = models.CharField(max_length=128)

	class Meta:
		verbose_name = 'Tanuló'
		verbose_name_plural = 'Tanulók'

	def __str__(self):
		return f"{self.nev} ({self.fnev} - {self.jelszo})"

	def feltoltes():
		with open('tanulo_input.tsv', 'r') as f:
			for t in f.readlines():
				tan = t.split('\t')
				Tanulo.objects.create(nev = tan[0], fnev=tan[1], jelszo = tan[2], email=tan[3])

	def azonositas(fn, j):
		return Tanulo.objects.filter(fnev=fn, jelszo=j).count()!=0

class Foglalkozas(models.Model):
	nev = models.CharField(max_length=128)
	maxdb = models.IntegerField()
	db = models.IntegerField()
	

	class Meta:
		verbose_name = 'Foglalkozás'
		verbose_name_plural = 'Foglalkozások'

	def __str__(self):
		return f"{self.nev} ({self.db}/{self.maxdb})"
	

class Valasztas(models.Model):
	tanulo = models.ForeignKey(Tanulo, on_delete=models.CASCADE)
	foglalkozas = models.ForeignKey(Foglalkozas, on_delete=models.CASCADE)

	class Meta:
		verbose_name = 'Választás'
		verbose_name_plural = 'Választások'

	def __str__(self):
		return f"{self.tanulo.nev} -> {self.foglalkozas.nev}"

	def formrol(post):
		print("POST request érkezet!!! :)")
		print(f"A {post['felhasznalonev']} felhasználónevű tanuló a {post['jelszo']} jelszót beírva a {post['valasztas']} foglalkozást választaná")

		tlista = list(Tanulo.objects.filter(fnev=post['felhasznalonev'], jelszo=post['jelszo']))

		uzenetek = ""

		if not Tanulo.azonositas(post['felhasznalonev'], post['jelszo']):
			print("sikertelen azonosítás!")
			uzenetek += "Hibás a felhasználónév vagy a jelszó!"
			return uzenetek

		print("sikeres azonosítás.")
		uzenetek += "Sikeresen azonosítottuk a felhasználót."

		fogl = list(Foglalkozas.objects.filter(nev=post['valasztas']))[0] # ez a választott foglalkozás
		if	fogl.db>0:
			print('jelentkezés sikeres!')
			uzenetek += 'jelentkezés sikeres!'
			Valasztas.objects.create(tanulo=tlista[0], foglalkozas=fogl)
			# v = Valasztas(tanulo=tlista[0], foglalkozas=fogl)
			# v.save()
			fogl.db-=1
			fogl.save()
		else:
			print('jelentkezés sikertelen')
			uzenetek += 'jelentkezés sikertelen, mert közben már elvitték a helyet!'

		return uzenetek





# teendők:

# Átjelentkezés:
# - Egy diák ne tudjon két foglalkozásra jelentkezni!
# - Az új jelentkezés írja felül a régit! (hogy ne kelljen jelentkezéstörléssel bajlódni)
# - Ha valaki így tesz, akkor az átjelentkezés tényét írja ki a felhasználónak!

# - ha az admin site-on keresztül törölnek egy választást, akkor a szabad helyek száma is frissüljön! desktruktorokkal kell játszani majd.
