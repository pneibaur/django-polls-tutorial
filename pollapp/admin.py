from django.contrib import admin

# Register your models here.
from .models import Question, Choice


# below, it used to say: class ChoiceInline(admin.StackedInline):
class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3


# first way of doing it...
# admin.site.register(Question)

# improved way:
# class QuestionAdmin(admin.ModelAdmin):
#     fields = ["pub_date", "question_text"]

# even more improved way!
class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {"fields": ["question_text"]}),
        ("date information", {"fields": [
         "pub_date"], "classes": ["collapse"]}),
    ]
    inlines = [ChoiceInline]
    # this changest the display to look more like a list, and gives the fields to display in that list view. 
    list_display = ("question_text", "pub_date", "was_pub_recently")
    # this adds a "filter" sidebar that lets ppl filter the change list by the pub_date field. 
    list_filter = ["pub_date"]
    # this adds a search field up top! it uses a LIKE query in SQL, so limit the number of searchable fields so it's easier on your DB.  
    search_fields = ['question_text']
    """
    Nows also a good time to note that change lists give you free pagination. 
    The default is to display 100 items per page. Change list pagination, 
    search boxes, filters, date-hierarchies, and column-header-ordering 
    all work together like you think they should.
    """


admin.site.register(Question, QuestionAdmin)
# you *could* register a choice this way, but it's better to do it another way!
# admin.site.register(Choice)
