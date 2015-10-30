# -*- coding: utf-8 -*-
import os
from inspectors.app import create_app
from inspectors.settings import ProdConfig, DevConfig


def test_production_config():
    os.environ['CONFIG'] = 'inspectors.settings.ProdConfig'
    app = create_app()
    assert app.config['ENV'] == 'prod'
    assert app.config['DEBUG'] is False
    assert app.config['DEBUG_TB_ENABLED'] is False
    assert app.config['ASSETS_DEBUG'] is False


def test_dev_config():
    os.environ['CONFIG'] = 'inspectors.settings.DevConfig'
    app = create_app()
    assert app.config['ENV'] == 'dev'
    assert app.config['DEBUG'] is True
    assert app.config['ASSETS_DEBUG'] is True
