import re

from bs4 import BeautifulSoup
import requests


def getCookies(resultsLink):
    session = requests.Session()
    res = session.get(resultsLink)

    reg = re.compile(r'xmlhttp.open\("GET","(.+?)".+?"\+(.+?)\+.+?\+(.+?),')
    matches = reg.search(res.text)

    return session, matches.groups('1:4')


def getResultsPage(rollNo, session, baseLink, id, accessToken):
    baseLink = ('https://jntuaresults.ac.in/' + baseLink + rollNo + '&id='
                + id + '&accessToken=' + accessToken)

    res = session.get(baseLink)
    return res.text


def convertToCSV(content):
    soup = BeautifulSoup(content, 'lxml')

    res = [
        [elem.next_sibling.text.strip() for elem in soup.findAll('b')],
        [elem.text.strip() for elem in soup.findAll('th') if elem.text]]

    for elem in soup.findAll('tr'):
        tmp = []
        for child in elem.findAll('td'):
            if child.text:
                tmp.append(child.text)
        if tmp:
            res.append(tmp)

    res = [','.join(row) for row in res]
    return res


def generateCSV(rollNos, link, filename):
    cookies = getCookies(link)
    with open(filename, 'w') as f:
        for rollNo in rollNos:
            for row in convertToCSV(getResultsPage(rollNo, cookies[0], *cookies[1])):
                f.write(row + '\n')
            print(rollNo + '\r', end='', flush=False)
            f.write('\n'*3)


if __name__ == '__main__':
    rollNos = [
        '19bf1a05e1',
        '19bf1a05e2',
        '19bf1a05e3',
        '19bf1a05e4',
        '19bf1a05e5',
    ]
    generateCSV(
        rollNos, 'https://jntuaresults.ac.in/view-results-56736469.html', 'results.csv')
