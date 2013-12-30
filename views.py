from django.shortcuts import render
from django import forms
from django.core.mail import send_mail
from django.http import HttpResponseNotFound
from django.http import Http404
from django.http import HttpResponse
from django.core.serializers.json import DjangoJSONEncoder
from django.views.generic import ListView
from simple.models import Page, Category
from django.template import loader, Context
from django.shortcuts import get_object_or_404
from django.core.exceptions import PermissionDenied
from django.conf import settings
import re
import json
from django.db.models import Q

class ContactForm( forms.Form ):
    defaultAttr = [ ( 'required', '' ), ( 'class', 'input' ) ]
    
    subject     = forms.CharField( max_length=100, widget = forms.TextInput(attrs = dict( defaultAttr + [ ( 'placeholder', 'Subject' ) ] ) ) )
    message     = forms.CharField( max_length=1000, widget = forms.Textarea(attrs=dict( defaultAttr + [ ( 'placeholder', 'Message' ) ] ) ), label="Message" )
    sendername  = forms.CharField( max_length=100, label="Name", widget = forms.TextInput(attrs=dict( defaultAttr + [ ( 'placeholder', 'Your Name' ) ] ) ) )
    senderemail = forms.EmailField( label="Email", widget = forms.TextInput(attrs=dict( defaultAttr + [ ( 'placeholder', 'Your Email' ) ]  ) ) )

def ensurePermission( page, request ):
    if page.status == 0 and not request.user.is_authenticated():
        raise PermissionDenied
    page.updateReads( request )

def paragraphedPageContent( content ):
    paras = re.split(r'[\r\n]+', content)
    newParas = []
    
    for p in paras:
        beginsWithTag = re.search( r'^<([\w]+)', p )
        addPTag = True;
        if beginsWithTag:
            firstTag = beginsWithTag.groups(0)
            addPTag = firstTag in [ 'em', 'strong', 'span' ]
        if addPTag:
            newParas.append('<p>%s</p>' % p.strip() )
        else:
            newParas.append(p.strip() )
    
    return '\n'.join(newParas)

def renderWithDefaults( request, context ):
    form = ContactForm()
    aboutMePage = Page.objects.get(slug='hidden-about-me')
    newContext = dict( [( 'contactform', form ), ( 'aboutMe', paragraphedPageContent( aboutMePage.content ) ) ] + context.items() )
    
    return render( request, 'simple/page.html', newContext ) 


def catPageViewStuff( category, year, slug, json, request ):
    ensureList( category )

    myCat = Category.objects.get(name=category).subCategoryName
    page = get_object_or_404( Page, slug=slug, created__year=year, categories__name=myCat )

    ensurePermission( page, request )
    
    if json:
        returnDic = page.pageDict() 
    else:
        returnDic = {'page':page}

    templateName = 'simple/subs/' + myCat + '.html'
    pageContent = paragraphedPageContent( page.content )
    returnDic[ 'htmlContent' ] = loader.render_to_string( templateName, { 'page': page, 'pageContent': pageContent } )

    return returnDic


def catPageView( request, category, year, slug ):
    context = catPageViewStuff( category, year, slug, False, request )    
    return renderWithDefaults( request, context )
    
def catPageViewJson( request, category, year, slug ):
    returnDic = catPageViewStuff( category, year, slug, True, request )
    return HttpResponse( json.dumps( returnDic , cls=DjangoJSONEncoder), content_type = 'application/json' )

def ensureList( category ):
    category = Category.objects.get(name=category)
    if len( category.subCategoryName ) == 0:
        raise Http404

def listViewStuff( category, json, request ):
    ensureList( category )
    page = Page.objects.get(slug=category)
    ensurePermission( page, request )
    posts = Page.objects.filter( categories__name=page.categories.all()[ 0 ].subCategoryName ).order_by( '-created' )
    
    if json:
        returnDic = page.pageDict()
    else:
        returnDic = {'page':page}

    templateName = 'simple/subs/' + category + '.html'
    pageContent = paragraphedPageContent( page.content );
    returnDic[ 'htmlContent' ] = loader.render_to_string( templateName, { 'page': page, 'pageContent':pageContent, 'posts': posts} )

    return returnDic

def listView( request, category ):
    context = listViewStuff( category, False, request )    
    return renderWithDefaults( request, context )
    
def listViewJson( request, category ):
    returnDic = listViewStuff( category, True, request )
    return HttpResponse( json.dumps( returnDic , cls=DjangoJSONEncoder), content_type = 'application/json' )

def staticViewInstance( request, slug ):
    try:
        #pageInstance = Page.objects.get(slug=slug).
        pageInstance = Page.objects.filter(slug=slug).filter(Q(categories__name='static') | Q(categories__name='gallery')).all()
        if len( pageInstance ) != 1:
            raise Http404
        pageInstance = pageInstance[ 0 ]
        ensurePermission( pageInstance, request )
    except Page.DoesNotExist:
        raise Http404
    
    return pageInstance
    
def staticViewJson( request, slug='home' ):
    pageInstance = staticViewInstance( request, slug )
    returnDic = pageInstance.pageDict()
    pageContent = paragraphedPageContent( pageInstance.content );
    returnDic[ 'htmlContent' ] = loader.render_to_string( 'simple/subs/static.html', {'pageContent':pageContent })
    
    return HttpResponse( json.dumps( returnDic , cls=DjangoJSONEncoder), content_type = 'application/json' )

def staticView( request, slug='home' ):
    pageInstance = staticViewInstance( request, slug )
    pageContent = paragraphedPageContent( pageInstance.content );
    html = loader.render_to_string( 'simple/subs/static.html', {'pageContent':pageContent})

    return renderWithDefaults( request, {'page': pageInstance, 'htmlContent': html } )
    
def submitContactForm( request ):
    if request.is_ajax():
        form = ContactForm(request.POST)
        if form.is_valid():
            subject     = form.cleaned_data[     'subject' ]
            message     = form.cleaned_data[     'message' ]
            sendername  = form.cleaned_data[  'sendername' ]
            senderemail = form.cleaned_data[ 'senderemail' ] 
            recipients = [ x[ 1 ] for x in settings.ADMINS ]            
            messageText = 'From: %s (%s)\n--------\n%s'%(sendername, senderemail,message)
            send_mail(subject , messageText, senderemail, recipients )
            return HttpResponse( json.dumps( {'done':True } ), content_type = 'application/json' )
        else:
            return HttpResponse( json.dumps( {'error':form.errors } ), content_type = 'application/json' )
    else:
        raise Http404

def submitKudos( request ):
    if request.is_ajax():
        if 'kudo' in request.POST:
            val = 1
        else:
            val = -1
        id = int( request.POST['id'] ); 
        pageInstance = get_object_or_404( Page, id = id ) 
        pageInstance.kudos += val
        pageInstance.kudos = max( 0, pageInstance.kudos )
        pageInstance.save()    
        return HttpResponse( json.dumps( {'done':True } ), content_type = 'application/json' )
    else:
        raise Http404

def handler404(request):
    form = ContactForm()
    html = loader.render_to_string( 'simple/404.html', {'contactform':form})
    return HttpResponseNotFound(html)

def handler403(request):
    form = ContactForm()
    html = loader.render_to_string( 'simple/403.html', {'contactform':form})
    return HttpResponseNotFound(html)
