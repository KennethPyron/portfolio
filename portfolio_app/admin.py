from django.contrib import admin


from .models import Student, Portfolio, Project


class MyAdminSite(admin.AdminSite):
    site_header = "Monty Python administration"

admin.site.register(Student)
admin.site.register( Project)
admin.site.register( Portfolio)

