from module.database import init_database
from module.case import get_cases

if __name__ == '__main__':
    init_database()

    for case in get_cases():
        case().run()