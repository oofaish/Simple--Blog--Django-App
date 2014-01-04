from django.db import models
import datetime
from django.utils import timezone
from datetime import datetime
    
class Category( models.Model ):
    name            = models.CharField( max_length=30 )
    subCategoryName = models.CharField( max_length=30, blank=True )
     
    def __unicode__(self):
        return self.name

class Script( models.Model ):
    name    = models.CharField( max_length = 30 ) 
    url     = models.URLField()

    def __unicode__(self):
        return self.name

class Stylesheet( models.Model ):
    name    = models.CharField( max_length = 30 )
    url     = models.URLField()
    
    def __unicode__(self):
        return self.name
    
class Tag( models.Model ):
    name = models.CharField( max_length=100 ) 
    
    def __unicode__(self):
        return self.name

class ThingTag( models.Model ):
    name = models.CharField( max_length=100 ) 
    
    def __unicode__(self):
        return self.name

class Image( models.Model ):
    title = models.CharField( max_length=100 )
    link  = models.CharField( max_length=200 )
    size  = models.CharField( max_length=20  ) #small, #large, #medium

    def __unicode__(self):
        return self.title

class Thing( models.Model ):
    title       = models.CharField(max_length=200)
    description = models.TextField()
    tags        = models.ManyToManyField(ThingTag, blank=True )
    created     = models.DateTimeField(default=datetime.now())
    updated     = models.DateTimeField(auto_now=True)
    reads       = models.PositiveIntegerField(default=0)
    link        = models.URLField(blank=True)
    image       = models.URLField(blank=True)
    video       = models.URLField(blank=True)
    status      = models.PositiveSmallIntegerField(default=1)#0 means dont show it, 1 means show it
    
    def __unicode__(self):
        return self.title
        
class Page( models.Model ):
    title         = models.CharField(max_length=200)
    slug          = models.CharField(max_length=30)
    content       = models.TextField()
    categories    = models.ManyToManyField(Category, blank=True ) #'blogpost', 'static', 'idea',
    tags          = models.ManyToManyField(Tag, blank=True ) #again for blog posts
    created       = models.DateTimeField(default=datetime.now())
    updated       = models.DateTimeField(auto_now=True)
    kudos         = models.PositiveIntegerField(default=0)
    showKudos     = models.BooleanField(default=True)
    reads         = models.PositiveIntegerField(default=0)
    images        = models.ManyToManyField(Image, blank=True )
    stylesheets   = models.ManyToManyField(Stylesheet, blank=True )
    scripts       = models.ManyToManyField(Script, blank=True )
    inlinescript  = models.TextField(blank=True)
    inlinestyle   = models.TextField(blank=True)
    status        = models.PositiveSmallIntegerField(default=1)#0 means dont show it, 1 means show it
    password      = models.CharField(max_length=20,blank=True)

    def __unicode__( self ):
        if not self.status:
            return self.title + ' (Hidden)'
        else:
            return self.title + ' (Visible)'

    def updateReads( self, request ):
        if not request.user.is_authenticated():#only add read for non-logged in users, not for ME!!!
            self.reads += 1
            self.save()

    def pageDict( self ):    
        keys = ( "title", "id", "kudos", "showKudos", 'inlinescript', 'inlinestyle' )
        r = {}
        
        for key in keys:
            r[ key ] = getattr( self, key )
        
        r[ 'longTitle' ] = self.longTitle
        
        scripts = []
        stylesheets = []
        for stylesheet in self.stylesheets.all():
            stylesheets.append(stylesheet.url)
        for script in self.scripts.all():
            scripts.append(script.url)
        
        r[ 'stylesheets' ] = stylesheets
        r[ 'scripts' ] = scripts
        
        return r
    
    @property
    def longTitle(self):
        return 'Ali Cigari - Web and Mobile Developer - ' + self.title

    @property
    def summary(self):
        return self.content[0:min(100,len(self.content))]
    