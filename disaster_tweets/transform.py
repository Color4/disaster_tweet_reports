#   Copyright 2012 Palantir Technologies
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
import copy

MISSING_VALUE = '!__MISSING_VALUE__!'


def trim_tweet(tweet):
    fields = (
        u'user',
        u'place',
        u'text',
        u'created_at',
        u'coordinates'
    )
    trimmed_tweet = trim_map(tweet, fields)
    trimmed_tweet[u'user'] = trim_user(trimmed_tweet[u'user'])
    return trimmed_tweet


def trim_user(user):
    fields = (
        u'id',
        u'screen_name',
        u'name',
    )
    return trim_map(user, fields)


def trim_map(src, fields, dst=None):
    #fields = map(lambda x: unicode(x, 'utf-8'), fields)
    if not dst:
        dst = {}

    for field in fields:
        if(field in src):
            dst[field] = src[field]
        else:
            dst[field] = MISSING_VALUE
    return dst


class Decorator:

    def __init__(self, name):
        self.name = name

    def decorate(self, tweet):
        return tweet


class RemoveHandle(Decorator):

    def __init__(self, name, handle):
        Decorator.__init__(self, name)
        self.handle = handle

    def decorate(self, tweet):
        text = tweet[u'text']
        trim_length = len(self.handle) + 2
        tweet[u'pretty_text'] = text[trim_length:]
        return tweet


def decorate_tweet(tweet, decorators):
    for decorator in decorators:
        try:
            scratch_copy = copy.deepcopy(tweet)
            tweet = decorator.decorate(scratch_copy)
        except Exception, e:
            # drop this decorator
            print 'decorator failed (skipping): %s' % e
    return tweet
