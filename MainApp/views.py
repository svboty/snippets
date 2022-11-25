from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.http import Http404, HttpResponseNotAllowed, HttpResponseForbidden
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
        return HttpResponseNotAllowed(permitted_methods='GET/POST')


def snippets_page(request):
    my = request.GET.get('my')
    lang = request.GET.get('lang')
    if my:
        snippets = Snippet.objects.filter(user=request.user)
        page_name = 'Мои сниппеты'
    else:
        snippets = Snippet.objects.filter(public=True)
        if request.user.is_authenticated:
            snippets = snippets | Snippet.objects.filter(user=request.user)
        page_name = 'Просмотр сниппетов'
    if lang:
        snippets = snippets.filter(lang=lang)
    sort = request.GET.get("sort", '')
    if sort == 'name':
        snippets = snippets.order_by('name')
        sort = '-name'
    elif sort == '-name':
        snippets = snippets.order_by('-name')
        sort = ''
    elif sort == '':
        sort = 'name'
    print(sort is None)
    print(sort)
    context = {
        'pagename': page_name,
        'snippets': snippets,
        'sort': sort
    }
    return render(request, 'pages/view_snippets.html', context)


@login_required(login_url='login')
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
        if request.user != snippet.user:
            raise PermissionDenied
        form = SnippetForm(request.POST, instance=snippet)
        if form.is_valid():
            form.save()
            return redirect(to='snippets-detail', snippet_id=snippet_id)
        return render(request, 'add_snippet.html', {'form': form})
    else:
        return HttpResponseNotAllowed(permitted_methods='GET/POST')


@login_required(login_url='login')
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
        if request.user != snippet.user:
            raise PermissionDenied
        snippet.delete()
        return redirect(to='snippets-list')
    else:
        return HttpResponseNotAllowed(permitted_methods='GET/POST')


def snippet_detail(request, snippet_id, comment_form=None):
    try:
        snippet = Snippet.objects.prefetch_related('comments').get(pk=snippet_id)
    except Snippet.DoesNotExist:
        raise Http404
    comments = snippet.comments.all()
    if comment_form is None:
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


@login_required(login_url='login')
def comment_add(request):
    if request.method == "POST":
        comment_form = CommentForm(request.POST, request.FILES)
        snippet_id = request.POST['snipped_id']
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.author = request.user
            comment.snippet = Snippet.objects.get(id=snippet_id)
            comment.save()
            return redirect('snippets-detail', snippet_id)
        else:
            return snippet_detail(request, snippet_id, comment_form)
    return HttpResponseNotAllowed(permitted_methods='POST')
