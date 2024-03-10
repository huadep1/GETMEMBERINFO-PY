import re

import requests


def parse_cookies(cookie: str) -> dict:
    cookies = {}
    for item in cookie.split(";"):
        item = item.strip()
        if not item:
            continue
        if "=" not in item:
            continue
        name, value = item.split("=", 1)
        cookies[name] = value
    return cookies


def GET_DTSG(ses: requests.Session) -> str:
    headers = {
        "authority": "www.facebook.com",
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "accept-language": "en-GB,en;q=0.9,vi-VN;q=0.8,vi;q=0.7,en-US;q=0.6",
        "cache-control": "max-age=0",
        "dnt": "1",
        "dpr": "1",
        "sec-ch-prefers-color-scheme": "dark",
        "sec-ch-ua": '"Chromium";v="122", "Not(A:Brand";v="24", "Google Chrome";v="122"',
        "sec-ch-ua-full-version-list": '"Chromium";v="122.0.6261.112", "Not(A:Brand";v="24.0.0.0", "Google Chrome";v="122.0.6261.112"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-model": '""',
        "sec-ch-ua-platform": '"Windows"',
        "sec-ch-ua-platform-version": '"10.0.0"',
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "same-origin",
        "sec-fetch-user": "?1",
        "upgrade-insecure-requests": "1",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        "viewport-width": "1069",
    }

    response = ses.get(
        "https://www.facebook.com/help/contact/571927962827151/", headers=headers
    )
    dtsg = re.findall(
        r'<input type="hidden" name="fb_dtsg" value="([^\\\"]+)"', response.text
    )[0]
    return dtsg


def GET_MEMBER_INFO(ses: requests.Session, dtsg: str, groupdid: str) -> None:
    cursor = ""
    while True:
        try:
            headers = {
                "authority": "www.facebook.com",
                "accept": "*/*",
                "accept-language": "en-US,en;q=0.9,vi;q=0.8",
                "content-type": "application/x-www-form-urlencoded",
                "dpr": "1",
                "origin": "https://www.facebook.com",
                "sec-ch-prefers-color-scheme": "dark",
                "sec-ch-ua": '"Chromium";v="122", "Not(A:Brand";v="24", "Google Chrome";v="122"',
                "sec-ch-ua-full-version-list": '"Chromium";v="122.0.6261.112", "Not(A:Brand";v="24.0.0.0", "Google Chrome";v="122.0.6261.112"',
                "sec-ch-ua-mobile": "?0",
                "sec-ch-ua-model": '""',
                "sec-ch-ua-platform": '"Windows"',
                "sec-ch-ua-platform-version": '"10.0.0"',
                "sec-fetch-dest": "empty",
                "sec-fetch-mode": "cors",
                "sec-fetch-site": "same-origin",
                "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
                "viewport-width": "1537",
                "x-asbd-id": "129477",
                "x-fb-friendly-name": "GroupsCometPeopleProfilesPaginatedListPaginationQuery",
                "x-fb-lsd": "S1JtnYjQJDm1lsySFMVRb9",
            }

            data = {
                "__a": "1",
                "fb_dtsg": dtsg,
                "variables": '{"count":10,"cursor":"'
                + cursor
                + '","groupID":"'
                + groupdid
                + '","membershipType":"MEMBER","scale":1,"search":null,"statusStaticFilter":null,"id":"'
                + groupdid
                + '"}',
                "server_timestamps": "true",
                "doc_id": "24770628242581257",
            }

            response = ses.post(
                "https://www.facebook.com/api/graphql/",
                headers=headers,
                data=data,
            )
            resp = response.json()["data"]["node"]["people_profiles"]
            flag = resp["page_info"]["has_next_page"]

            for i in resp["edges"]:
                print(
                    "{0} | {1} | {2}".format(
                        i["node"]["name"], i["node"]["id"], i["node"]["profile_url"]
                    ),
                )
            if flag:
                cursor = resp["page_info"]["end_cursor"]
            else:
                return
        except Exception as e:
            print(1, e)
            return


if __name__ == "__main__":
    with requests.Session() as ses:
        print("Please enter your cookies: ")
        cookies = input()
        ses.cookies.update(parse_cookies(cookies))
        dtsg = GET_DTSG(ses)
        print("Please enter your group id: ")
        groupid = input()
        GET_MEMBER_INFO(ses, dtsg, groupid)
