from django.contrib import admin

from tenants.utils import tenant_from_request

from .models import Choice, Question


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3
    readonly_fields = ['tenant', ]


class QuestionAdmin(admin.ModelAdmin):
    search_fields = ['question_text']
    list_filter = ['pub_date']
    list_display = ('question_text', 'pub_date', 'was_published_recently')
    fieldsets = [
        ('None', {'fields': ['question_text']}),
        ('Date Information', {'fields': ['pub_date']})
    ]
    inlines = [ChoiceInline]

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        tenant = tenant_from_request(request)
        queryset = queryset.filter(tenant=tenant)
        return queryset

    def save_model(self, request, obj, form, change):
        tenant = tenant_from_request(request)
        obj.tenant = tenant
        super().save_model(request, obj, form, change)

    def save_formset(self, request, form, formset, change):
        tenant = tenant_from_request(request)
        instances = formset.save(commit=False)
        for obj in formset.deleted_objects:
            obj.delete()

        for instance in instances:
            instance.tenant = tenant
            instance.save()

        formset.save_m2m()


admin.site.register(Question, QuestionAdmin)
