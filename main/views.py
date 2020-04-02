from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404
from django.template import TemplateDoesNotExist
from django.template.loader import get_template
from django.contrib.auth.views import LoginView
from django.contrib.auth.views import LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import UpdateView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from django.contrib.auth.views import PasswordChangeView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import AdvUser
from .forms import ChangeUserinfoForm
from .forms import RegisterUserForm
from django.views.generic.base import TemplateView
from django.core.signing import BadSignature
from django.views.generic.edit import CreateView
from django.views . generic.edit import DeleteView
from django.contrib.auth import logout
from django.contrib import messages
from django.shortcuts import redirect
from .forms import StForm
from .utilities import signer

class STR_LoginView(LoginView):
    template_name = 'main/login.html'
def other_page(request, page):
    try:
        template = get_template('main/' + page + '.html')
    except TemplateDoesNotExist:
        raise Http404
    return HttpResponse(template.render(request=request))
def index(request):
    sts = St.objects.filter(is_active=True)[:10]
    context = { 'sts': sts }
    return render(request, 'main/index.html', context)

from .models import StDocument 

def document(request):
    documents = StDocument.objects.all()
   
    return render(request, 'main/document.html', { 'documents':documents })



class STR_LogoutView(LoginRequiredMixin, LogoutView):
    #pdb.set_trace()
    #input()
    template_name = 'main/logout.html'
    
class ChangeUserinfoView(SuccessMessageMixin, LoginRequiredMixin,
                         UpdateView) :
    model = AdvUser
    template_name = 'main/change_user_info.html'
    form_class = ChangeUserinfoForm
    success_url = reverse_lazy('main:profile')
    success_message = 'личные данные пользователя изменены'
    def dispatch(self, request, *args, **kwargs):
        self . user_id = request.user.pk
        return super() .dispatch(request, *args, **kwargs)
    def get_object(self, queryset=None):
        if not queryset:
            queryset = self.get_queryset()
            return get_object_or_404(queryset, pk=self.user_id)

class STR_PasswordChangeView(SuccessMessageMixin, LoginRequiredMixin,
                           PasswordChangeView) :
    template_name = 'main/password_change.html' 
    success_url = reverse_lazy('main:profile')
    success_message = 'Пароль пользователя изменен'
    

class RegisterUserView(CreateView):
    model = AdvUser
    template_name = 'main/register_user.html'
    form_class = RegisterUserForm
    succes_url = reverse_lazy('main:register_done')
    
class RegisterDoneView(TemplateView):
    template_name = 'main/register_done.html'
    
    
def user_activate(request, sign):
    try:
        username = signer.unsign(sign)
    except BadSignature:
        return render(request, 'main/bad_signature.html')
    user = get_object_or_404(AdvUser, username=username)
    if user.is_activated:
        template = 'main/user is activated.html'
    else:
        template = 'main/ac tivation done.html'
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
 

from django.db.models import Q
from .models import SubRubric, St,Comment
from .forms import SearchForm,  UserCommentForm, GuestCommentForm

def by_rubric(request, pk):
    rubric = get_object_or_404(SubRubric, pk=pk)
    sts = St.objects.filter(is_active=True, rubric=pk)
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        q = Q(title__icontains=keyword) | Q(content__icontains=keyword)
        sts = sts.filter(q)
    else:
        keyword = ''
    form = SearchForm(initial={'keyword': keyword})
    paginator = Paginator(sts, 2)
    if 'page' in request.GET:
        page_num = request.GET['page']
    else:
        page_num = 1
    page = paginator.get_page(page_num)
    context = {'rubric':rubric, 'page':page, 'sts':page.object_list, 'form':form}
    return render(request, 'main/by_rubric.html', context)
    

def detail(request, rubric_pk, pk):
    st = get_object_or_404(St, pk=pk)
    #ais = st.additionalimage_set.all()
    comments = Comment.objects.filter(st=pk, is_active=True)
    initial = {'st': st.pk}
    if request.user.is_authenticated:
        initial['author'] = request.user.username
        form_class = UserCommentForm
    else:
        form_class = GuestCommentForm
    form = form_class(initial=initial)
    if request.method == 'POST':
        c_form = form_class(request.POST)
        if c_form.is_valid():
            c_form.save()
            messages.add_message(request, messages.SUCCESS,
                                 'Комментарий добавлен')
        else:
            form = c_form
            messages.add_message(request, messages.WARNING,
                                 'Комментарий не добавлен')
    context = {'st': st, 'comments': comments, 'form': form}
    return render(request, 'main/detail.html', context)

