from django.contrib import auth
from django.http import Http404, HttpResponseNotAllowed
from django.shortcuts import get_object_or_404, render, redirect

from MainApp.models import Snippet
from MainApp.forms import CommentForm, SnippetForm, UserRegistrationForm


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


def snippet_update(request, snippet_id):
    if request.method == 'GET':
        snippet = get_object_or_404(Snippet, pk=snippet_id)
        form = SnippetForm(instance=snippet)
        context = {
            'pagename': 'Редактирование сниппета',
            'form': form
        }
        return render(request, 'pages/add_snippet.html', context)
    elif request.method == 'POST':
        snippet = get_object_or_404(Snippet, pk=snippet_id)
        form = SnippetForm(request.POST, instance=snippet)
        if form.is_valid():
            form.save()
            return redirect(to='snippets-detail', snippet_id=snippet_id)
        return render(request, 'add_snippet.html', {'form': form})
    else:
        return HttpResponseNotAllowed()


def snippet_delete(request, snippet_id):
    if request.method == 'GET':
        snippet = get_object_or_404(Snippet, pk=snippet_id)
        form = SnippetForm(instance=snippet)
        context = {
            'pagename': 'Вы уверены, что хотите удалить запись ',
            'form': form
        }
        print(form.fields)
        return render(request, 'pages/delete_snippet.html', context)
    elif request.method == 'POST':
        snippet = get_object_or_404(Snippet, pk=snippet_id)
        snippet.delete()
        return redirect(to='snippets-list')
    else:
        return HttpResponseNotAllowed()


def snippet_detail(request, snippet_id):
    try:
        snippet = Snippet.objects.prefetch_related('comments').get(pk=snippet_id)
    except Snippet.DoesNotExist:
        raise Http404
    comments = snippet.comments.all()
    comment_form = CommentForm()
    context = {
        'pagename': 'Просмотр сниппета',
        'snippet': snippet,
        'comment_form': comment_form,
        'comments': comments
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


def registration(request):
    if request.method == "GET":
        form = UserRegistrationForm()
        context = {
            "form": form
        }
        return render(request, 'pages/registration.html', context)
    elif request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
        else:
            context = {
                "form": form
            }
            return render(request, 'pages/registration.html', context)
        return redirect('home')


def comment_add(request):
    if request.method == "POST":
        comment_form = CommentForm(request.POST)
        snippet_id = request.POST['snipped_id']
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.author = request.user
            comment.snippet = Snippet.objects.get(id=snippet_id)
            comment.save()
            return redirect('snippets-detail', snippet_id)

    return HttpResponseNotAllowed()