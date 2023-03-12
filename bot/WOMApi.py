from datetime import datetime

import requests

BASE_URL = "https://api.wiseoldman.net/v2"


def create(
        title: str,
        metric: str,
        startsAt: datetime,
        endsAt: datetime,
        groupId: int,
        groupVerificationCode: str,
):
    endpoint = "/competitions"
    dateFormat = "%Y-%m-%dT%H:%M:%S.%fZ"
    params = {
        "title": title,
        "metric": metric,
        "startsAt": startsAt.strftime(dateFormat),
        "endsAt": endsAt.strftime(dateFormat),
        "groupId": groupId,
        "groupVerificationCode": groupVerificationCode,
    }
    requestUrl = __build_url(BASE_URL, endpoint)
    return requests.post(requestUrl, json=params)


def delete(sotwId: int, verificationCode: str):
    endpoint = "/competitions/{}"
    params = {"verificationCode": verificationCode}
    requestUrl = __build_url(BASE_URL, endpoint, [sotwId])
    return requests.delete(requestUrl, data=params)


def get(sotwId: int):
    endpoint = "/competitions/{}"
    requestUrl = __build_url(BASE_URL, endpoint, [sotwId])
    return requests.get(requestUrl)


def updateAllParticipants(sotwId: int, verificationCode: str):
    endpoint = "/competitions/{}/update-all"
    params = {"verificationCode": verificationCode}
    requestUrl = __build_url(BASE_URL, endpoint, [sotwId])
    return requests.post(requestUrl, data=params)


def __build_url(baseurl: str, endpoint: str, args: list = None):
    if args is None:
        return baseurl + endpoint
    else:
        return (baseurl + endpoint).format(*args)
