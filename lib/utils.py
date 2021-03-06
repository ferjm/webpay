import json

from curling.lib import API
from slumber.exceptions import HttpClientError


class SlumberWrapper(object):
    """
    A wrapper around the Slumber API.
    """

    def __init__(self, url, oauth):
        self.slumber = API(url)
        self.slumber.activate_oauth(oauth.get('key'), oauth.get('secret'))
        self.api = self.slumber.api.v1

    def parse_res(self, res):
        if res == '':
            return {}
        if isinstance(res, (str, unicode)):
            return json.loads(res)
        return res

    def safe_run(self, command, *args, **kwargs):
        try:
            res = command(*args, **kwargs)
        except HttpClientError as e:
            res = self.parse_res(e.response.content)
            for key, value in res.iteritems():
                res[key] = [self.errors[v] for v in value]
            return {'errors': res}
        return res
