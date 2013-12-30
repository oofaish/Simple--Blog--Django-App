from simple.models import Category, Tag, Page, Script, Stylesheet

class InitDB:
    tagNames       = []
    pages          = []
    categoryNames  = []
    
    def __init__( self ):
        self.categoryNames = ( 'blogpost', 'static', 'gallery', 'idea', 'blog', 'ideas' )
        self.tagNames      = ( 'coding', 'django', 'cycling', 'rowing', 'travelling', 'web development', 'jquery', 'css', 'html5', 'random thoughts', 'music' )
        self.pages         = ({ 'title': 'Home',
                                'slug':  'home',
                                'content': 'this is the home page',
                                'category': 'static',
                                'showKudos': False,
                                },
                              {
                                'title': 'CountdownCube',
                                'slug':  'countdown',
                                'content': 'Here is an example of countdown cube:',
                                'category': 'static',
                                'showKudos': True,
                                },
                              { 'title': 'Gallery',
                                'slug':  'gallery',
                                'content': 'This is the gallery',
                                'category': 'gallery'
                                },
                              { 'title': 'Portfolio',
                                'slug':  'portfolio',
                                'content': 'this is the portfolio',
                                'category': 'static'
                                },
                              { 'title': 'Ideas',
                                'slug':  'ideas',
                                'content': 'list of ideas',
                                'category': 'ideas',
                                'showKudos': False,
                                },
                              { 'title': 'Blog',
                                'slug':  'blog',
                                'content': 'list of blog posts',
                                'category': 'blog',
                                'showKudos': False,
                                },
                              
                              { 'title': 'blog post 1',
                                'slug':  'blog_post_1',
                                'content': 'this is blog post 1',
                                'category': 'blogpost'
                               },
                              { 'title': 'idea 1',
                                'slug':  'idea_1',
                                'content': 'this is idea 1',
                                'category': 'idea'
                               }
                              )
    def add( self ):  
        for tagName in self.tagNames:
            tag, created = Tag.objects.get_or_create( name = tagName )
            tag.save()
            

        for categoryName in self.categoryNames:
            if categoryName == 'blog':
                defaults = {'subCategoryName': 'blogpost' }
            elif categoryName == 'ideas':
                defaults = {'subCategoryName': 'idea' }
            else:
                defaults = {}
            Category.objects.get_or_create( name = categoryName, defaults=defaults )
        
        s = Script(name="countdowncube.js",url='http://cigari.co.uk/countdowncube.js')
        s.save()
        s = Script(name="countdown.js", url="http://cigari.co.uk/countdown.js" )
        s.save()
        s = Stylesheet(name="countdowncube.css", url="http://cigari.co.uk/countdowncube.css")
        s.save()
        s = Stylesheet(name="countdown.css", url="http://cigari.co.uk/countdown.css")
        s.save()
        
        
        
    def addPages( self ):
        for page in self.pages:
            categoryName = page.pop( 'category' )
            slug         = page.pop( 'slug' )
            pageInstance, created = Page.objects.get_or_create( slug = slug, defaults=page )
            category = Category.objects.get(name=categoryName)
            pageInstance.categories.add( category )
            if slug == 'countdown':
                stylesheet = Stylesheet.objects.get(name="countdowncube.css")
                pageInstance.stylesheets.add( stylesheet )
                stylesheet = Stylesheet.objects.get(name="countdown.css")
                pageInstance.stylesheets.add( stylesheet )
                script = Script.objects.get(name="countdowncube.js")
                pageInstance.scripts.add( script )
                script = Script.objects.get(name="countdown.js")
                pageInstance.scripts.add( script )
                
            pageInstance.save()
        
i = InitDB()
i.add()
i.addPages()