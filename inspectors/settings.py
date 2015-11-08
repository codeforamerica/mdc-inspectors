# -*- coding: utf-8 -*-
import os

os_env = os.environ


class Config(object):
    SECRET_KEY = os_env.get('INSPECTORS_SECRET', 'secret-key')  # TODO: Change me
    SQLALCHEMY_DATABASE_URI = os_env.get(
        'DATABASE_URL',
        'postgresql://localhost/mdc_inspectors')
    APP_DIR = os.path.abspath(os.path.dirname(__file__))  # This directory
    PROJECT_ROOT = os.path.abspath(os.path.join(APP_DIR, os.pardir))
    BCRYPT_LOG_ROUNDS = 13
    ASSETS_DEBUG = False
    DEBUG_TB_ENABLED = False  # Disable Debug toolbar
    DEBUG_TB_INTERCEPT_REDIRECTS = False
    CACHE_TYPE = 'simple'  # Can be "memcached", "redis", etc.
    TYPEFORMIO_KEY = '70b84fe857c39c5653f17fd845143f11'
    ADMIN_EMAIL = os_env.get('ADMIN_EMAIL', 'ehsiung@codeforamerica.org')
    MAIL_USERNAME = os_env.get('MAIL_USERNAME')
    MAIL_PASSWORD = os_env.get('MAIL_PASSWORD')
    MAIL_SERVER = os_env.get('MAIL_SERVER')
    MAIL_DEFAULT_SENDER = os_env.get(
        'MAIL_DEFAULT_SENDER',
        'no-reply@miamidade.gov')
    FEEDBACK_SENDER = os_env.get(
        'FEEDBACK_SENDER',
        'feedbackbot@miamidade.gov')
    MAIL_PORT = 587
    MAIL_USE_SSL = False
    MAIL_USE_TLS = True


class ProdConfig(Config):
    """Production configuration."""
    ENV = 'prod'
    DEBUG = False
    DEBUG_TB_ENABLED = False  # Disable Debug toolbar
    MAIL_USERNAME = os_env.get('SENDGRID_USERNAME')
    MAIL_PASSWORD = os_env.get('SENDGRID_PASSWORD')
    MAIL_SERVER = 'smtp.sendgrid.net'
    MAIL_MAX_EMAILS = 100


class DevConfig(Config):
    """Development configuration."""
    ENV = 'dev'
    DEBUG = True
    DEBUG_TB_ENABLED = True
    ASSETS_DEBUG = True  # Don't bundle/minify static assets
    CACHE_TYPE = 'simple'  # Can be "memcached", "redis", etc.
    MAIL_SERVER = 'smtp.gmail.com'  # Use gmail in dev: https://support.google.com/mail/answer/1173270?hl=en
    ADMIN_EMAIL = os_env.get(
        'ADMIN_EMAIL',
        'mdcfeedbackdev@gmail.com')
    MAIL_USERNAME = 'mdcfeedbackdev@gmail.com'
    MAIL_PASSWORD = 'miamidade305'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    # MAIL_SUPPRESS_SEND = True


class TestConfig(Config):
    TESTING = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os_env.get(
        'TEST_DATABASE_URL',
        'postgresql://localhost/mdc_inspectors_test')
    BCRYPT_LOG_ROUNDS = 1  # For faster tests
    WTF_CSRF_ENABLED = False  # Allows form testing
