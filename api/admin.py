from django.contrib import admin

from .models import Company, Worker


class WorkerAdmin(admin.ModelAdmin):
    list_display = ("name", "position", "private_phone", "work_phone", "fax", "company")
    search_fields = ("name",)
    list_filter = ("name",)
    empty_value_display = "-пусто-"
    actions = ('update', 'delete',)


class CompanyAdmin(admin.ModelAdmin):
    list_display = ("title", "info", "address", 'author')
    search_fields = ("title",)
    list_filter = ("title",)
    empty_value_display = "-пусто-"


admin.site.register(Worker, WorkerAdmin)
admin.site.register(Company, CompanyAdmin)

