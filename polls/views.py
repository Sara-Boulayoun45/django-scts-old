from django.db.models import F # Hilft beim direkten Hochzählen in der Datenbank
from django.http import HttpResponse, HttpResponseRedirect 
# 'render' ist ein Werkzeug, das eine HTML-Datei nimmt, Daten hineinfüllt und das fertige Ergebnis an den Browser schickt
# Importiert get_object_or_404, um Fehler abzufangen, falls eine ID nicht existiert
from django.shortcuts import get_object_or_404, render
from django.urls import reverse 
# 'generic' enthält die fertigen Bausteine (Klassen) von Django
from django.views import generic
# Import den Bauplan-Model für die Fragen
from .models import Choice, Question

class IndexView(generic.ListView):
    # Welches Design soll benutzt werden?
    template_name = "polls/index.html"
    context_object_name = "latest_question_list"

    def get_queryset(self):
         # Holt die letzten 5 Fragen aus der Datenbank
        return Question.objects.order_by("-pub_date")[:5]
    
class DetailView(generic.DetailView):
    model = Question
    template_name = "polls/detail.html"

class ResultsView(generic.DetailView):
    model = Question
    template_name = "polls/results.html"       


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        # Versucht die gewählte Antwort aus dem Formular zu holen
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        # Wenn nichts ausgewählt wurde: Zurück zum Formular + Fehlermeldung
        return render(
            request,
            "polls/detail.html",
            {
                "question": question,
                "error_message": "Du hast keine Antwort ausgewählt.",
            },
        )
    else:
        # Stimme in der Datenbank hochzählen
        selected_choice.votes = F("votes") + 1
        selected_choice.save()
        # Nach dem Speichern: Umleitung zur Ergebnisseite
        return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))
