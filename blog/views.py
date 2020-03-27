from django.utils import timezone
from .models import Post, Comment
from django.shortcuts import render, get_object_or_404
from .forms import PostForm, CommentForm
from django.shortcuts import redirect
from django.http import HttpResponse, Http404
from django.template import TemplateDoesNotExist
from django.template.loader import get_template
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import SearchForm
from django.db.models import Q
from .models import SubRubric
from django.views.generic.edit import CreateView
from django.views.generic.base import TemplateView
from django.urls import reverse_lazy
from .forms import RegisterUserForm
from .models import AdvUser
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.views.generic.edit import DeleteView
from django.views.generic.list import ListView
from .models import Post, Rubric
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic.edit import UpdateView
from django.contrib.messages.views import SuccessMessageMixin

class PostLogoutView(LoginRequiredMixin, LogoutView):
    template_name = 'logout.html'

class Post_LoginView(LoginView):
    template_name = 'login.html'

def index(request):
    rubrics = Rubric .objects.all()
    posts = Post.objects.all()
    paginator = Paginator(posts, 2)
    if 'page' in request.Get:
        page_num = request.Get('page')
    else:
        page_num = 1
        page = paginator.get_page(page_num)
        context = {'rubrics': rubrics, 'page': page, 'posts': page.object_list}
    return render(request, 'index.html', context)
@login_required
def profile(request):
    return render(request, 'profile.html')

class PostByRubricView(ListView):
    template_name = 'blog/by_rubric.html'
    context_object_name = 'posts'
    def get_queryset(self):
        return Post.objects.filter(rubric=self.kwargs['rubric_id'])
    def get_context_data(self, *args, **kwargs) :
        context = super() .get_context_data(*args, **kwargs)
        context['rubrics'] = Rubric.objects.all()
        context['current_rubric']
        return context

@login_required
def profile_post_add(request):
    if request.method == 'POST':
        form = PostForm(request.POST,request.FILES)
        if form.is_valid():
            post = form.save()
            #formset = AIFormSet(request.POST, request.FILES, instance=st)
            #if formset.is_valid():
             #formset. save ()
            messages.add_message(request, messages.SUCCESS, 'Объявление добавлено')
            return redirect('blog:profile')
    else:
        form = PostForm(initial={'author':request.user.pk})
      #  formset = AIFormSet()
        context = {'form':form}
        return render(request, 'profile_post_add.html', context)
    
def by_rubric(request, pk):
    rubric = get_object_or_404(SubRubric, pk=pk)
    posts = Post.objects.filter(is_active=True, rubric=pk)
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        q = Q(title__icontains=keyword) | Q(content__icontains=keyword)
        posts = posts.filter(q)
    else:
        keyword = ''
    form = SearchForm(initial={'keyword': keyword})
    paginator = Paginator(posts, 2)
    if 'page' in request.GET:
        page_num = request.GET['page']
    else:
        page_num = 1
    page = paginator.get_page(page_num)
    context = {'rubric':rubric, 'page':page, 'posts':page.object_list, 'form':form}
    return render(request, 'blog/by_rubric.html', context)

def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'blog/post_list.html', {'posts': posts})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})

@login_required
def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})
@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})

def other_page(request, page):
    try:
        template = get_template('blog/'+page+'.html')
    except TemplateDoesNotExist:
        raise Http404
    return HttpResponse(template.render(request=request))

def project_page(request, page):
    try:
        template = get_template('blog/'+ page+ '.html')
    except TemplateDoesNotExist:
        raise Http404
    return HttpResponse(template.render(request=request))

class RegisterUserView(CreateView):
    model = AdvUser
    template_name = 'register_user.html'
    form_class = RegisterUserForm
    succes_url = reverse_lazy('register_user')
    
class RegisterDoneView(TemplateView):
    template_name = 'register_done.html'
    
def user_activate(request, sign):
    try:
        username = signer.unsign(sign)
    except BadSignature:
        return render(request, 'main/bad_signature.html')
    user = get_object_or_404(AdvUser, username=username)
    if user.is_activated:
        template = 'blog/user is activated.html'
    else:
        template = 'blog/activation done.html'
        user.is_active = True
        user.is_activated = True
        user. save ()
    return render(request, template)

class DeleteUserView(LoginRequiredMixin, DeleteView):
    model = AdvUser
    template_name = 'main/delete_user.html'
    success_url = reverse_lazy('main:index')
    def dispatch(self, request, *args, **kwargs):
        self.user_id = request.user.pk
        return super().dispatch(request, *args, **kwargs)
    def post(self, request, *args, **kwargs):
        logout(request)
        messages.add_message(request, messages.SUCCESS, 'Пользователь удален')
        return super() .post(request, *args, **kwargs)
    def get_object(self, queryset=None):
        if not queryset:
            queryset = self.get_queryset()
            return get_object_or_404(queryset, pk=self.user_id)
        
def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'blog/add_comment_to_post.html', {'form': form})

@login_required
def comment_approve(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.approve()
    return redirect('post_detail', pk=comment.post.pk)

@login_required
def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.delete()
    return redirect('post_detail', pk=comment.post.pk)

def home(request):
    postList = Post.objects.filter(visible='1')
    paginator = Paginator(postList, 4)
    page = request.GET.get('page')
    querysetGoods = paginator.get_page(page)
 
    context = {
        "postList": postList,
        "title": "Главная страница блога",
        "desc": "Описание для главной страницы",
        "key": "ключевые, слова",
    }
    return render(request, "partial/home.html", context)
 
def single(request, id=None):
    return render(request, "partial/single.html")

