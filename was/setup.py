from setuptools import setup, find_packages

setup(
    name='project',
    version='1.0.0',
    packages=find_packages(),
    install_requires=[
        'setuptools==79.0.0',
        # was
        'sconfig==0.0.3',  # configuration toolkit
        'pydantic==2.11.3',  # Data validation
        'stringcase==1.2.0',  # convert string case
        'Werkzeug==3.1.3',  # util
        # ex
        'more-itertools==10.7.0',  # lodash
        # 타입 분석
        "mypy==1.15.0",  # type check
        'watchdog==6.0.0',  # shell util
        'requests==2.32.3',  # API requests
        'types-requests==2.32.0.20250328',  # request type check
        'python_dotenv==1.1.0',  # env
        # mypy greenlet 3.0.3 version은 intel cpu를 지원하지 않는다
        'greenlet==3.2.1',
        'ccxt==4.4.77',
        'openpyxl==3.1.5',
        'pyupbit==0.2.34',
        'PyJWT==2.10.1'
    ],
)
