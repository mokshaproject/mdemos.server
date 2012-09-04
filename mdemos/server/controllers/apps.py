# This file is part of Moksha.
# Copyright (C) 2008-2010  Red Hat, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# Authors: Luke Macken <lmacken@redhat.com>

import moksha.common.utils

from tg import expose, tmpl_context

from moksha.wsgi.widgets.api.containers import DashboardContainer
from moksha.wsgi.lib.helpers import Category, MokshaApp, MokshaWidget
from moksha.common.exc import ApplicationNotFound


class AppWidgetContainer(DashboardContainer):
    template = "${applist_widget(category='main', layout=layout)}"

    # It's context-aware!
    def prepare(self):
        super(AppWidgetContainer, self).prepare()
        self.tmpl_context = tmpl_context

appwidget_container = AppWidgetContainer(id='appwidget')


class AppController(object):

    @expose()
    def _lookup(self, app, *remainder):
        if app not in moksha.common.utils._apps:
            raise ApplicationNotFound(app)
        return moksha.common.utils.get_app(app), remainder

    @expose('mako:moksha.templates.widget')
    def container(self, application, height=675, width=910, left=55,
                  top=50, **kw):
        """ Return an application rendered in a Moksha Widget Container """
        app = moksha.common.utils.get_app(application)
        if not app:
            raise ApplicationNotFound(application)

        tmpl_context.widget = appwidget_container

        options = {}
        options['layout'] = [
            Category('main', [
                MokshaWidget(None, 'moksha_container', params={
                    'id': application + '_container',
                    'title': app['name'],
                    'content': appwidget_container(layout=[
                        Category('main', [MokshaApp(None, application,
                                                    params=kw)])]),
                    'height': 675,
                    'width': 910,
                    'left': 55,
                    'top': 50,
                    })
                ]),
        ]

        return dict(options=options)
