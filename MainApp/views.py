from django.http import Http404, HttpResponseNotAllowed
from django.shortcuts import get_object_or_404, render, redirect

from MainApp.models import Snippet


def index_page(request):
    context = {'pagename': 'PythonBin'}
    return render(request, 'pages/index.html', context)


def add_snippet_page(request):
    if request.method == 'GET':
        context = {'pagename': 'Добавление нового сниппета'}
        return render(request, 'pages/add_snippet.html', context)
    elif request.method == 'POST':
        name = request.POST.get('name')
        lang = request.POST.get('lang')
        code = request.POST.get('code')
        snippet = Snippet.objects.create(name=name, lang=lang, code=code)
        return redirect(to='snippets-detail', snippet_id=snippet.id)
    else:
        return HttpResponseNotAllowed()


def snippets_page(request):
    snippets = Snippet.objects.all()
    context = {
        'pagename': 'Просмотр сниппетов',
        'snippets': snippets
    }
    return render(request, 'pages/view_snippets.html', context)


def snippet_detail(request, snippet_id):
    snippet = get_object_or_404(Snippet, pk=snippet_id)
    context = {
        'pagename': 'Просмотр сниппета',
        'snippet': snippet
    }
    return render(request, 'pages/snippet.html', context)
