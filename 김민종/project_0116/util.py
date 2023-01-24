from datetime import datetime
def str2time(rows, n):
    ll = list(rows)
    ll.sort(key=lambda x: datetime.strptime(x[n], "%Y/%m/%d %H:%M:%S"), reverse=True)
    return ll

def check_session(s):
    if s == None:
        return False
    else:
        return True