import django_filters


class GithubRepoFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(field_name="repo", lookup_expr="icontains")


class WhaleFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(field_name="identifier", lookup_expr="icontains")