from balder.types import BalderObject
from haven import models


class GithubRepo(BalderObject):
    class Meta:
        model = models.GithubRepo


class Whale(BalderObject):
    class Meta:
        model = models.Whale
