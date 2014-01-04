from django.contrib import admin
from simple.models import Page, Tag, Image, Category, Stylesheet, Script, Thing, ThingTag

admin.site.register(Page)
admin.site.register(Thing)
admin.site.register(ThingTag)
admin.site.register(Tag)
admin.site.register(Image)
admin.site.register(Category)
admin.site.register(Script)
admin.site.register(Stylesheet)

