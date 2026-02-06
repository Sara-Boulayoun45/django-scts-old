import datetime 

from django.db import models
from django.utils import timezone


# Der Bauplan für die Umfrage_Fragen
class Question(models.Model):
    # Ein Textfeld für die Frage(max. 200 Zeichen)
    question_text = models.CharField(max_length=200)
    # Ein Feld für Datum und Uhrzeit der Veröffentlichung
    pub_date = models.DateTimeField("date published")

    # Damit die Frage ihren Text anzeigt
    def __str__(self):
        return self.question_text
    
    # Prüft ob die Frage jünger als 24 Stunden ist
    def was_published_recently(self):
        return self.pub_date >= timezone() - datetime.timedelta(days=1)


# Der Bauplan für die Antwortmöglichkeiten
class Choice(models.Model):
    # Jede Antwort gehört zu einer bestimmte Frage 
    # CASCADE = Wenn die Frage gelöscht wird, verschwindet auch die Antwort
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    # Ein Zähler für die Stimmen(startet bei 0)
    votes = models.IntegerField(default=0)

    # Damit die Antwort ihren Text anzeigt
    def _str_(self):
        return self.choice_text