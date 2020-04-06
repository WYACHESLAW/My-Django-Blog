from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from .models import StDocument
from .forms import StForm
from django.utils import timezone
from django.shortcuts import redirect

def document(request):
    documents = StDocument.objects.all()
    return render(request, 'main/document.html', { 'documents':documents })

def doc_detail(request, pk):
    document = get_object_or_404(StDocument, pk=pk)
    return render(request, 'main/docdetail.html', { 'document':document })

def login(request):
    return render(request, 'main/login.html')  
  
def index(request):
    sts = St.objects.filter(is_active=True)[:10]
    context = { 'sts': sts }
    return render(request, 'main/index.html', context) 

from django.db.models import Q
from .models import SubRubric, St,Comment
from .forms import SearchForm,  UserCommentForm, GuestCommentForm
from django.contrib import messages
   

def st_rubric(request, rubric_pk, pk):
    rubric = get_object_or_404(SubRubric, pk=pk)
    sts = St.objects.filter(is_active=True, rubric=pk)
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        q = Q(title__icontains=keyword) | Q(content__icontains=keyword)
        sts = sts.filter(q)
    else:
        keyword = ''
    form = SearchForm(initial={'keyword': keyword})
    paginator = Paginator(sts, 4)
    if 'page' in request.GET:
        page_num = request.GET['page']
    else:
        page_num = 1
    page = paginator.get_page(page_num)
    context = {'rubric':rubric, 'page':page, 'sts':page.object_list, 'form':form}
    return render(request, 'main/st_rubric.html', context)
    
@login_required
def st_detail(request, pk):
    st = get_object_or_404(St, pk=pk)
    #ais = st.additionalimage_set.all()
    context = {'st': st, 'pk':pk}
    return render(request, 'main/st_detail.html', context)

@login_required
def st_edit(request, pk):
    st = get_object_or_404(St, pk=pk)
    if request.method == "POST":
        form = StForm(request.St, instance=st)
        if form.is_valid():
            st = form.save(commit=False)
            st.author = request.user
            st.created_at = timezone.now()
            st.save()
            return redirect('st_detail', pk=st.pk)
    else:
        form = StForm(instance=st)
    return render(request, 'main/st_edit.html', {'form': form})

