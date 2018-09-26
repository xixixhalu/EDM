from utilities.config_util import ConfigUtil

config = ConfigUtil()


class Config:
    UPLOAD_FOLDER = 'input'
    ALLOWED_EXTENSIONS = set(['xml'])
    SEND_FILE_MAX_AGE_DEFAULT = 0
    MONGO_DBNAME = config.get('Mongo_DB', 'db_name')
    MONGO_URI = config.get('Mongo_DB', 'mongo_db_uri')
    LOGIN_DISABLED = False

    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DEBUG = False

runtime_config = {
    'dev': DevelopmentConfig
}

