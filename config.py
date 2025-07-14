import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    MODEL_PATH = 'app/models/mental_health_model.pkl'
    PREPROCESSOR_PATH = 'app/models/preprocessor.pkl'
    SUBMISSIONS_PATH = 'data/submissions'
    
class DevelopmentConfig(Config):
    DEBUG = True
    
class ProductionConfig(Config):
    DEBUG = False

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}