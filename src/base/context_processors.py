from src.search.forms import SearchForm
from src.base.models import Webring


def global_search_form(request):
    return {"search_form": SearchForm(request.GET or None)}

def webrings_context(request):
    return {"webrings": Webring.objects.all()}
