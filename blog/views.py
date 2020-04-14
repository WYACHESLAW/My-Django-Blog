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
from django.views.generic.base import TemplateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.views.generic.list import ListView
from .models import Rubric, Profile
from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import UserPassesTestMixin
from .forms import LoginForm, UserRegistrationForm
from django.contrib.auth import authenticate, login
#from django.contrib import messages
from django.contrib import messages
#from actions.utils import create_action
#from django.contrib.auth import get_user_model

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request,
                                username=cd['username'],
                                password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponse('Authenticated '\
                                        'successfully')
                else:
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse('Invalid login')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})


class STR_PasswordChangeView(SuccessMessageMixin, LoginRequiredMixin,
                           PasswordChangeView) :
    template_name = 'blog/password_change.html' 
    success_url = reverse_lazy('blog:profile')
    success_message = 'Пароль пользователя изменен'

class PostLogoutView(LoginRequiredMixin, LogoutView):
    template_name = 'logout.html'

class Post_LoginView(LoginView):
    template_name = 'login.html'
   

def index(request):
    rubrics = Rubric .objects.all()
    posts = Post.objects.all()
    paginator = Paginator(posts, 5)
    if 'page' in request.Get:
        page_num = request.Get('page')
    else:
        page_num = 1
        page = paginator.get_page(page_num)
        context = {'rubrics': rubrics, 'page': page, 'posts': page.object_list}
    return render(request, 'index.html', context)
@login_required
def profile(request):
    posts = Post.objects.filter(author=request.user.pk)
    context = {'posts': posts}
    return render(request, 'profile.html', context)

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
            #post =form.save() 
            form.save()
            #formset = AIFormSet(request.POST, request.FILES, instance=st)
            #if formset.is_valid():
             #formset. save ()
            messages.add_message(request, messages.SUCCESS, 'Объявление добавлено')
            return redirect('profile')
    else:
        form = PostForm(initial={'author':request.user.pk})
      #  formset = AIFormSet()
        context = {'form':form}
        return render(request, 'profile_post_add.html', context)
@login_required
def profile_post_change(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post = form.save()
            #formset = AIFormSet(request.POST, request.FILES, instance=st)
            #if formset.is_valid():
                #formset.save()
            messages.add_message(request, messages.SUCCESS, 'Объявление исправлено')
            return redirect('profile')
    else:
        form = PostForm(instance=post)
        #formset = AIFormSet(instance=st)
        context = {'form':form}
        return render(request, 'profile_post_change.html', context) 
@login_required
def profile_post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        post.delete()
        messages.add_message(request, messages.SUCCESS, 'Объявление удалено')
        return redirect ('profile')
    else:
        context = {'post':post}
        return render(request, 'profile_post_delete.html', context)
    
    
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
    if UserPassesTestMixin:
        posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
        paginator = Paginator(posts, 5) # По 3 статьи на каждой странице.
        page = request.GET.get('page')
        try:
            posts = paginator.page(page)
        except PageNotAnInteger:
 	 # Если страница не является целым числом, возвращаем первую страницу. 
 	        posts = paginator.page(1)
        except EmptyPage:
            posts = paginator.page(paginator.num_pages)

        return render(request, 'blog/post_list.html', {'page': page, 'posts': posts})
#def post_list(request, tag_slug=None):
#    object_list = Post.published.all()
#    tag = None

#    if tag_slug:
#        tag = get_object_or_404(Tag, slug=tag_slug)
#        object_list = object_list.filter(tags__in=[tag])

#    paginator = Paginator(object_list, 3) # 3 posts in each page
#    page = request.GET.get('page')
#    try:
#        posts = paginator.page(page)
#    except PageNotAnInteger:
        # If page is not an integer deliver the first page
#        posts = paginator.page(1)
#    except EmptyPage:
        # If page is out of range deliver last page of results
#        posts = paginator.page(paginator.num_pages)

#    return render(request,
#                  'blog/post/list.html',
#                  {'page': page,
#                   'posts': posts,
#                   'tag': tag})
 

@login_required
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

    
class RegisterDoneView(TemplateView):
    template_name = 'register_done.html'
 
@login_required
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

def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            # Create a new user object but avoid saving it yet
            new_user = user_form.save(commit=False)
            # Set the chosen password
            new_user.set_password(user_form.cleaned_data['password'])
            # Save the User object
            new_user.save()
            # Create the user profile
            Profile.objects.create(user=new_user)
#            create_action(new_user, 'has created an account')
            return render(request, 'register_done.html', {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request,'register.html', {'user_form': user_form})

from .forms import ChangeUserinfoForm
from django.views.generic.edit import UpdateView
from .models import AdvUser
class ChangeUserinfoView(SuccessMessageMixin, LoginRequiredMixin,
                         UpdateView) :
    model = AdvUser
    template_name = 'blog/change_user_info.html'
    form_class = ChangeUserinfoForm
    success_url = reverse_lazy('blog:profile')
    success_message = 'личные данные пользователя изменены'
    def dispatch(self, request, *args, **kwargs):
        self . user_id = request.user.pk
        return super() .dispatch(request, *args, **kwargs)
    def get_object(self, queryset=None):
        if not queryset:
            queryset = self.get_queryset()
            return get_object_or_404(queryset, pk=self.user_id)

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

