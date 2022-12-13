from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Whale)
admin.site.register(GithubRepo)
admin.site.register(RepoScan)
