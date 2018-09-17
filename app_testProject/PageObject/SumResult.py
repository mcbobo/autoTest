from common.BaseAndroidPhone import getPhoneInfo
from common.BaseStatistics import countSum, countInfo, countSumDevices


def statistics_result(**kwargs):
    countSum(kwargs["result"])
    get_phone = getPhoneInfo(kwargs["devices"])
    get_phone["phone_name"] = get_phone["brand"] + "_" + get_phone["model"]
    get_phone["release"] = "android" + "_" + get_phone["release"]

    countInfo(result=kwargs["result"], testInfo=kwargs["testInfo"], caseName=kwargs["caseName"],
              phoneName=get_phone["phone_name"], driver=kwargs["driver"], logTest=kwargs["logTest"],
              devices=kwargs["devices"], testCase=kwargs["testCase"], testCheck=kwargs["testCheck"])

    countSumDevices(kwargs["devices"], kwargs["result"], phone_info=get_phone)
