from setuptools import setup, find_packages

setup(
    name='project',
    version='1.0.0',
    packages=find_packages(),
    install_requires=[
        'setuptools==79.0.0',
        # was
        'Flask==3.1.0',
        'sconfig==0.0.3',
        'pydantic==2.11.3',
        'stringcase==1.2.0',
        'flask-cors==5.0.1',
        # DB
        'SQLAlchemy==2.0.40',
        'Flask-SQLAlchemy==3.1.1',
        'alembic==1.15.2',
        'psycopg2-binary==2.9.10',
        # ex
        'pytz==2025.2',
        'more-itertools==10.7.0',
        'types-pytz==2025.2.0.20250326',
        # 타입 분석
        "mypy==1.15.0",
        'watchdog==6.0.0',
        'requests==2.32.3',
        'types-requests==2.32.0.20250328',
        'python_dotenv==1.1.0',
        'Werkzeug==3.1.3',
        # job scheduler
        'APScheduler==3.11.0',
        # mypy greenlet 3.0.3 version은 intel cpu를 지원하지 않는다
        'greenlet==3.2.1',
        'ccxt==4.4.77',
        'openpyxl==3.1.5',
        'pyupbit==0.2.34',
        'PyJWT==2.10.1',
        'pandas==2.2.3'
    ],
)
