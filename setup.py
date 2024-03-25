from setuptools import setup, find_packages

setup(
    name='project',
    version='1.0.0',
    packages=find_packages(),
    install_requires=[
        'setuptools==69.1.0',
        # was
        'sconfig==0.0.3',  # configuration toolkit
        'pydantic==1.10.14',  # Data validation
        'stringcase==1.2.0',  # convert string case
        'Werkzeug==3.0.1',  # util
        # ex
        'more-itertools==10.2.0',  # lodash
        # 타입 분석
        "mypy==1.8.0",  # type check
        'watchdog==3.0.0',  # shell util
        'requests==2.31.0',  # API requests
        'types-requests==2.31.0.20240218',  # request type check
        'python_dotenv==1.0.1',  # env
        # mypy greenlet 3.0.3 version은 intel cpu를 지원하지 않는다
        'greenlet==2.0.2',
        'ccxt==4.2.82',
        'pandas==2.2.1'
    ],
)
