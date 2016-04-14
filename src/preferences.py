import datetime

class Preferences():
    gradeLevel = '1'  # 1 = freshman, 2 = sophomore, 3 = junior, 4 = senior
    semester = 'FA15'
    webdriver = '0'  # 0 = firefox, 1 = phantom
    MAXCLASSES = 7
    MAXLINKEDCLASSES = 3
    botTimeout = 2.5 # time in seconds

    freshStart = datetime.datetime.strptime(
                "4/20/15/07/00/02", "%m/%d/%y/%H/%M/%S")
    sophoStart = datetime.datetime.strptime(
                "4/20/15/07/00/02", "%m/%d/%y/%H/%M/%S")
    juniorStart = datetime.datetime.strptime(
                "4/20/15/07/00/02", "%m/%d/%y/%H/%M/%S")
    seniorStart = datetime.datetime.strptime(
                "4/20/15/07/00/02", "%m/%d/%y/%H/%M/%S")
