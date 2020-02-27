import os
import multiprocessing


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEBUG = os.getenv('DEBUG', True)
CPU_CORE = multiprocessing.cpu_count()
DATABASE_URL = os.getenv(
    'DATABASE_URL', 'postgresql://docker:docker@127.0.0.1/docker')
TEST_DATABASE_URL = os.getenv(
    'DATABASE_URL', 'postgresql://docker:docker@127.0.0.1/docker_test')
