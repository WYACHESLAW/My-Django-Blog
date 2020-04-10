from .models import StSubRubric, StDSubRubric

def st_context_processor(request):
    context = {}
    context['strubrics'] = StSubRubric.objects.all()
    return context
    context ['keyword'] = ''
    context['all'] = ''
    if 'keyword' in request.GET:
        keyword = request. GET ['keyword']
        if keyword:
            context ['keyword'] = '?keyword=' + keyword
            context ['all'] = context ['keyword']
    if 'page' in request.GET:
        page = request.GET['page']
        if page != '1':
            if context ['all']:
                context['all'] += '&page=' + page
            else:
                context['all'] = 'page=' + page
    return context

def std_context_processor(request):
    context = {}
    context['stdrubrics'] = StDSubRubric.objects.all()
    return context
    context ['keyword'] = ''
    context['all'] = ''
    if 'keyword' in request.GET:
        keyword = request. GET ['keyword']
        if keyword:
            context ['keyword'] = '?keyword=' + keyword
            context ['all'] = context ['keyword']
    if 'page' in request.GET:
        page = request.GET['page']
        if page != '1':
            if context ['all']:
                context['all'] += '&page=' + page
            else:
                context['all'] = 'page=' + page
    return context