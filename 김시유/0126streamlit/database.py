# import os

# from deta import Deta  # pip install deta
# from dotenv import load_dotenv  # pip install python-dotenv


# # load the environment variables
# load_dotenv(".env")
# DETA_KEY = os.getenv('DETA_KEY')

from deta import Deta  # pip install deta

DETA_KEY = "c0f58ysq_SEoRv7hE5wFeVsb4LfCoM4Fk4YDuu9Dr"


# initailize with a project key
deta = Deta(DETA_KEY)

# this is how to create/connect a database
db = deta.Base('monthly_report')

# 데이터베이스에 특정 기간의 값을 삽입


def insert_period(period, incomes, expenses, comment):
    """Returns the report on a successful creation, otherwise raises an error"""
    return db.put({"key": period, "incomes": incomes, "expenses": expenses, "comment": comment})

# selectbox채우기 위해 모든 기간 가져오기


def fetch_all_periods():
    """Returns a dict of all periods"""
    res = db.fetch()
    return res.items

# 특정기간 모든 값 가져와서 데이터 플롯


def get_period(period):
    """If not found, the function will return None"""
    return db.get(period)


# deta.sh siu2388 Govlchfhd0! Dashboard
