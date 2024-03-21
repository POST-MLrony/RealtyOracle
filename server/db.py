import sqlalchemy
import databases
import ormar

# Определение URL базы данных (в данном случае, PostgreSQL)
DATABASE_URL = "sqlite:///./test.db"
# Инициализация объекта базы данных с использованием databases
database = databases.Database(DATABASE_URL)

# Инициализация объекта метаданных для работы с SQLAlchemy
metadata = sqlalchemy.MetaData()

# Определение метакласса BaseMeta для использования в ормар-моделях
class BaseMeta(ormar.ModelMeta):
    # Указание объекта метаданных и базы данных для моделей
    metadata = metadata
    database = database
    
# Импорт моделей из модуля api.models
from api import models
