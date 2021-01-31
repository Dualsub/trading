import urllib.request
import re

# In the website source the symbol of a stock always appears after "<a href="/quote/" and before "?p=",
# which is why these terms are looked up in the html. 

def get_gainers():
    response = urllib.request.urlopen("https://finance.yahoo.com/gainers")
    lines = response.read().decode("utf8").splitlines()
    lines = list(filter(lambda line: (('<a href="/quote/' in line) and ('?p=' in line) and ('title=' in line) and 'class="Fw(600) C($linkColor)"' in line), lines))
    
    stock_symbols = []

    search_str = '<a href="/quote/'
    
    for line in lines:
        idxs = [a.start() for a in list(re.finditer(search_str, line))]
        for i in idxs:
            end = i
            while line[end] != "?" and (i-end) < 10:
                end += 1

            stock_symbols.append(line[i+len(search_str):end])

    return stock_symbols

if __name__ == "__main__":
    for symbol in getGainers():
        print(symbol)
            