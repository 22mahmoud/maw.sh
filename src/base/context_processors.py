from src.search.forms import SearchForm


def global_search_form(request):
    return {"search_form": SearchForm(request.GET or None)}
