from django.contrib import auth
from django.http import Http404, HttpResponseNotAllowed
from django.shortcuts import get_object_or_404, render, redirect

from MainApp.models import Snippet
from MainApp.forms import SnippetForm


def index_page(request):
    context = {'pagename': 'PythonBin'}
    return render(request, 'pages/index.html', context)


def add_snippet_page(request):
    if request.method == 'GET':
        form = SnippetForm()
        context = {
            'pagename': 'Добавление нового сниппета',
            'form': form
        }
        return render(request, 'pages/add_snippet.html', context)
    elif request.method == 'POST':
        form = SnippetForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user if request.user.is_authenticated else None
            instance.save()
            return redirect(to='snippets-detail', snippet_id=instance.id)
        return render(request, 'add_snippet.html', {'form': form})
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


def login_page(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request, user)
            print(username, "/", password)
    else:
        raise Http404
    return redirect(request.META.get('HTTP_REFERER', '/'))


def logout_page(request):
    auth.logout(request)
    return redirect(request.META.get('HTTP_REFERER', '/'))

