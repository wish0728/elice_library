# orm을 적용하기 위해서는 config.py라는 파일이 필요. 루트디렉터리에 config.py 파일 생성

import os

BASE_DIR = os.path.dirname(__file__) # 폴더 구조가 달라져도, 현재 폴더를 가져와서 사용할 수 있도록 설정

SQLALCHEMY_DATABASE_URI = 'sqlite:///{}'.format(os.path.join(BASE_DIR, 'elicelibrary.db'))    # db의 접속 주소.  BASE_DIR은 루트디렉토리인 elice_project
# os.path.join(BASE_DIR, 'user.db')를 사용하면, ~~~/user.db와 같은 디렉토리 구조 문자열이 반환됨.
SQLALCHEMY_TRACK_MODIFICATIONS = False   # SQLAlchemy의 이벤트를 처리하는 옵션. 지금은 필요하지 않아 false로 비활성화(켜두면 메모리 사용량이 늘어남)

# -> 이 과정을 통해 elicelibrary.db라는 데이터베이스 파일을 프로젝트의 루트 리텍토리에 저장하려함.