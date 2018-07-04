import os
from flask import Flask, session
from flask_nav import Nav, register_renderer
from flask_nav.renderers import Renderer
from flask_nav.elements import Navbar, View, Subgroup
from dominate import tags
import subprocess as sp
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_login import LoginManager


# Custom render for Sidebar Nav from sb admin 2 lib
class Sba2SidebarNav(Renderer):
    def visit_Navbar(self, node):
        sub = []
        for item in node.items:
            sub.append(self.visit(item))
        return tags.ul(
            *sub,
            _class='nav',
            id="side-menu"
        )

    def visit_Subgroup(self, node):
        return tags.li(
            tags.a(
                node.title,
                tags.span(_class="fa arrow"),
                href='#'
            ),
            tags.ul(
                *[self.visit(item) for item in node.items],
                _class='nav nav-second-level'
            )
        )

    def visit_View(self, node):
        return tags.li(
            tags.a(
                node.text,
                href=node.get_url()
            )
        )


def create_app():

    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object('config')
    if "CUSTOM_SALESCRM_CONFIG" in os.environ:
        app.config.from_pyfile(os.getenv('CUSTOM_SALESCRM_CONFIG'), silent=True)
    if "FLASK_CONFIG_FILE" in os.environ:
        app.config.from_envvar('FLASK_CONFIG_FILE', silent=True)
    #app.config = path_builds(app.config)
    app.db = SQLAlchemy(app)
    app.bootstrap = Bootstrap(app)
    nav = Nav()
    nav.init_app(app)
    register_renderer(app, 'sba2_sidebar_nav', Sba2SidebarNav)

    @nav.navigation()
    def menuRoles():
        return role_selector(session['auth_type'])['top_navbar']

    @nav.navigation()
    def menuAdmin():
        return role_selector(session['auth_type'])['side_navbar']

    src = os.path.join(
        os.getcwd(),
        'app',
        'static',
        'css')
    dst = os.path.join(
        os.getcwd(),
        'app',
        'static',
        'css')
    the_call = ' '.join(['lessc', src, dst])
    sp.call(the_call, shell=True)

    src = os.path.join(
        os.getcwd(),
        'app',
        'static',
        'css')
    dst = os.path.join(
        os.getcwd(),
        'app',
        'static',
        'css')
    the_call = ' '.join(['lessc', src, dst])
    sp.call(the_call, shell=True)

    src = os.path.join(
        os.getcwd(),
        'app',
        'static',
        'css')
    dst = os.path.join(
        os.getcwd(),
        'app',
        'static',
        'css')
    the_call = ' '.join(['lessc', src, dst])
    sp.call(the_call, shell=True)

    # app.login_manager = LoginManager(app)
    # app.login_manager.init_app(app)
    # app.login_manager.login_view = 'main.login'

    return app


def role_selector(role):

    if session['auth_type'] == 'admin':

        side_navbar = Navbar(
            View('x', 'x'),
            Subgroup('Home'),
            Subgroup('Organisation'),
            Subgroup('Contacts'),
            Subgroup('Analytics')

    navbar = {'side_navbar': side_navbar}

    return navbar
