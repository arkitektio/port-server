import django_filters


class GithubRepoFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(field_name="repo", lookup_expr="icontains")
