from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from .models import StDocument, StSubRubric, StDSubRubric
from .forms import StForm, StDocumentForm 
from django.utils import timezone
from django.shortcuts import redirect

@login_required
def profile_std_change(request, pk):
    std = get_object_or_404(StDocument, pk=pk)
    if request.method == 'POST':
        form = StDocumentForm(request.POST, request.FILES, instance=std)
        if form.is_valid():
            std = form.save()
            messages.add_message(request, messages.SUCCESS, 'Проект исправлен')
            return redirect('main:profile_std')
    else:
        form = StDocumentForm(instance=std)
        context = {'form':form}
        return render(request, 'profile_std_change.html', context) 
@login_required
def profile_std_delete(request, pk):
    std = get_object_or_404(StDocument, pk=pk)
    if request.method == 'POST':
        std.delete()
        messages.add_message(request, messages.SUCCESS, 'Проект будет удален')
        return redirect ('main:profile_std')
    else:
        context = {'std':std}
        return render(request, 'profile_std_delete.html', context)


@login_required
def profile_st_change(request, pk):
    st = get_object_or_404(St, pk=pk)
    if request.method == 'POST':
        form = StForm(request.POST, request.FILES, instance=st)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, 'Проект исправлен')
            return redirect('main:profile_st')
    else:
        form = StForm(instance=st)
        context = {'form':form}
        return render(request, 'profile_st_change.html', context) 
@login_required
def profile_st_delete(request, pk):
    st = get_object_or_404(St, pk=pk)
    if request.method == 'POST':
        st.delete()
        messages.add_message(request, messages.SUCCESS, 'Проект будет удален')
        return redirect ('main:profile_st')
    else:
        context = {'st':st}
        return render(request, 'profile_st_delete.html', context)


@login_required
def profile_std_add(request):
    if request.method == 'POST':
        form = StDocumentForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
#            formset = AIFormSet(request.POST, request.FILES, instance=std)
#            if formset.is_valid():
#             formset. save ()
            messages.add_message(request, messages.SUCCESS, 'Документ добавлен')
            return redirect('main/profile_std')
    else:
        form = StDocumentForm(initial={'author':request.user.pk})
#        formset = AIFormSet()
        context = {'form':form}
        return render(request, 'main/profile_std_add.html', context)


@login_required
def profile_st_add(request):
    if request.method == 'POST':
        form = StForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
#            formset = AIFormSet(request.POST, request.FILES, instance=st)
#            if formset.is_valid():
#             formset. save ()
            messages.add_message(request, messages.SUCCESS, 'Проект добавлен')
            return redirect('profile_st')
    else:
        form = StForm(initial={'author':request.user.pk})
#        formset = AIFormSet()
        context = {'form':form}
        return render(request, 'main/profile_st_add.html', context)

@login_required
def profile_std(request):
    stds = StDocument.objects.filter(author=request.user.pk)
    context = {'stds': stds}
    return render(request, 'main/profile_std.html', context)

@login_required
def profile_st(request):
    sts = St.objects.filter(author=request.user.pk)
    context = {'sts': sts}
    return render(request, 'main/profile_st.html', context)

def by_rubric_st(request, pk):
    strubric = get_object_or_404(StSubRubric, pk=pk)
    sts = St.objects.filter(is_active=True, strubric=pk)
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
    context = {'strubric':strubric, 'page':page, 'sts':page.object_list, 'form':form}
    return render(request, 'main/by_rubric_st.html', context)

def by_rubric_std(request, pk):
    stdrubric = get_object_or_404(StDSubRubric, pk=pk)
    stds = StDocument.objects.filter(is_active=True, stdrubric=pk)
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        q = Q(title__icontains=keyword) | Q(content__icontains=keyword)
        stds = stds.filter(q)
    else:
        keyword = ''
    form = SearchForm(initial={'keyword': keyword})
    paginator = Paginator(stds, 2)
    if 'page' in request.GET:
        page_num = request.GET['page']
    else:
        page_num = 1
    page = paginator.get_page(page_num)
    context = {'stdrubric':stdrubric, 'page':page, 'sts':page.object_list, 'form':form}
    return render(request, 'main/by_rubric_std.html', context)

def document(request):
    documents = StDocument.objects.all()
    return render(request, 'main/document.html', { 'documents':documents })


def login(request):
    return render(request, 'main/login.html')  
  
def index(request):
    sts = St.objects.filter(is_active=True)[:10]
    context = { 'sts': sts }
    return render(request, 'main/index.html', context) 

from django.db.models import Q
from .models import St
from .forms import SearchForm
from django.contrib import messages
    
@login_required
def st_detail(request, pk):
    st = get_object_or_404(St, pk=pk)
    #ais = st.additionalimage_set.all()
    context = {'st': st, 'pk':pk}
    return render(request, 'main/st_detail.html', context)

@login_required
def std_detail(request, pk):
    std = get_object_or_404(StDocument, pk=pk)
    #ais = st.additionalimage_set.all()
    context = {'std': std, 'pk':pk}
    return render(request, 'main/std_detail.html', context)

@login_required
def st_edit(request, pk):
    st = get_object_or_404(St, pk=pk)
    if request.method == "POST":
        form = StForm(request.POST, instance=st)
        if form.is_valid():
            st = form.save(commit=False)
            st.author = request.user
            st.created_at = timezone.now()
            st.save()
            return redirect('main:st_detail', pk=st.pk)
    else:
        form = StForm(instance=st)
    return render(request, 'main/st_edit.html', {'form': form})

def std_edit(request, pk):
    std = get_object_or_404(StDocument, pk=pk)
    if request.method == "POST":
        form = StDocumentForm(request.POST, instance=std)
        if form.is_valid():
            std = form.save(commit=False)
            std.author = request.user
            std.created_at = timezone.now()
            std.save()
            return redirect('main:std_detail', pk=std.pk)
    else:
        form = StDocumentForm(instance=std)
    return render(request, 'main/std_edit.html', {'form': form})
