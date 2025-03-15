from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database.orm import Base

DATABASE_URL = "mysql+pymysql://root:todos@127.0.0.1:3306/todos"


engine = create_engine(DATABASE_URL)
SessionFactory = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 데이터베이스 연결 및 테이블 생성
def create_tables():
    # 여기서 모든 모델을 생성합니다
    Base.metadata.create_all(bind=engine)


def get_db():
    session = SessionFactory()
    try:
        yield session
    finally:
        session.close()


# 테이블 생성 호출
create_tables()