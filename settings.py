import os


class Config(object):
    DEBUG = False


class DefaultConfig(Config):
    HOST = 'localhost'
    PORT = '5000'
    SQLALCHEMY_DATABASE_URI = 'postgresql://{}:{}@{}:{}/{}'.format(os.environ.get('DB_USER', 'dev'),
                                                                   os.environ.get('DB_PASS', 'dev'),
                                                                   os.environ.get('DB_HOST', 'localhost'),
                                                                   os.environ.get('DB_PORT', '5432'),
                                                                   os.environ.get('DB_NAME', 'dev'))


class DevelopmentConfig(DefaultConfig):
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True


class DevelopmentDockerConfig(DefaultConfig):
    HOST = '0.0.0.0'
    PORT = os.environ.get('PORT', 5000)
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductionConfig(DefaultConfig):
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    HOST = '0.0.0.0'
    PORT = os.environ.get('PORT', 5000)
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')


class ProductionHerokuDockerConfig(DefaultConfig):
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    HOST = '0.0.0.0'
    PORT = os.environ.get('PORT', 5000)
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')


config_dict = {
    'DEVELOPMENT': 'settings.DevelopmentConfig',
    'DEVELOPMENT_DOCKER': 'settings.DevelopmentDockerConfig',
    'PRODUCTION': 'settings.ProductionConfig',
    'PRODUCTION_HEROKU_DOCKER': 'settings.ProductionHerokuDockerConfig'
}

settings_object = config_dict[os.environ.get('FLASK_ENV', 'DEVELOPMENT')]
