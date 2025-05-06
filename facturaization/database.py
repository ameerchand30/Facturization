from sqlalchemy import create_engine, inspect
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from configDict import Setting
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

class DatabaseManager:
    def __init__(self):
        self.setting = Setting()
        self.database_name = self.setting.database_name
        self.SQLALCHEMY_DATABASE_URL = self._get_database_url()
        self.engine = None
        self.SessionLocal = None
        self.Base = declarative_base()

    def _get_database_url(self):
        return f"postgresql://{self.setting.database_username}:{self.setting.database_password}@{self.setting.database_hostname}:{self.setting.database_port}/{self.database_name}"

    def _get_postgres_connection_params(self):
        return {
            'host': self.setting.database_hostname,
            'port': self.setting.database_port,
            'user': self.setting.database_username,
            'password': self.setting.database_password
        }

    def create_database_if_not_exists(self):
        params = self._get_postgres_connection_params()
        try:
            # Try connecting to the target database
            conn = psycopg2.connect(**params, database=self.database_name)
            conn.close()
            print(f"Database '{self.database_name}' already exists")
        except psycopg2.OperationalError:
            # Connect to default postgres database to create new database
            conn = psycopg2.connect(**params, database='postgres')
            conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
            cur = conn.cursor()
            
            try:
                cur.execute(f'CREATE DATABASE "{self.database_name}"')
                print(f"Database '{self.database_name}' created successfully")
            except psycopg2.Error as e:
                print(f"Error creating database: {e}")
                raise e
            finally:
                cur.close()
                conn.close()

    def initialize(self):
        # Create database if it doesn't exist
        self.create_database_if_not_exists()
        
        # Create SQLAlchemy engine and session
        self.engine = create_engine(self.SQLALCHEMY_DATABASE_URL)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        
        # Create all tables
        self.Base.metadata.create_all(bind=self.engine)
        print("Database initialized successfully")

    def get_db(self):
        if not self.SessionLocal:
            raise Exception("Database not initialized. Call initialize() first.")
        
        db = self.SessionLocal()
        try:
            yield db
        finally:
            db.close()

# Create singleton instance
db_manager = DatabaseManager()

# Initialize database and create engine
db_manager.initialize()

# Export commonly used objects
engine = db_manager.engine
SessionLocal = db_manager.SessionLocal
Base = db_manager.Base
get_db = db_manager.get_db