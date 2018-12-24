import requests, bs4
from bottle import run, post, request as bottle_request


TELEGRAM = 'https://api.telegram.org/token-here/'
JOB_URL = 'https://www.indeed.com.ph/'


def get_chat_id(data):
    chat_id = data['message']['chat']['id']
    return chat_id


def get_message(data):
    message = data['message']['text']
    return message


def search_job(message):
    job_title = message.replace(' ', '+')
    res = requests.get(JOB_URL + 'jobs?q=' + job_title)
    res.raise_for_status()

    job_soup = bs4.BeautifulSoup(res.text)
    jobs = job_soup.select('.jobtitle')
    for i in range(len(jobs)):
        return jobs[i].getText().strip() + ' - ' + 'https://www.indeed.com.ph' + str(jobs[i].get('href'))


def get_data(data):
    message = get_message(data)
    job_data = search_job(message)

    response = {
        "chat_id": get_chat_id(data),
        "text": job_data
    }
    return response


def send(data):
    url = TELEGRAM + 'sendMessage'
    requests.post(url, json=data)


@post('/')
def main():
    response = bottle_request.json
    data = get_data(response)
    send(data)

    return response


if __name__ == '__main__':
    run(host='localhost', port=8080, debug=True)
