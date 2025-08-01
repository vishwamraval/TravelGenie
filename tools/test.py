import requests
from bs4 import BeautifulSoup

def fetch_grid_data(doc_url):
    response = requests.get(doc_url).text
    soup = BeautifulSoup(response, 'html.parser')
    grid = {}
    max_x, max_y = 0, 0
    rows = soup.find_all('tr')
    #skipping the first row as it contains headers
    for row in rows[1:]:  
        cols = row.find_all('td')
        # if len(cols) < 3:
        #     continue
        try:
            x=int(cols[0].text.strip())
            char=cols[1].text.strip()
            y=int(cols[2].text.strip())
        except ValueError:
            continue
        grid[(x, y)] = char
        max_x = max(max_x, x)
        max_y = max(max_y, y)
    return grid, max_x, max_y

def print_grid(grid, max_x, max_y):
    for y in range(max_y + 1):
        line = ''
        for x in range(max_x + 1):
            line += grid.get((x, y), ' ')
        print(line)

def end_to_end(doc_url):
    grid, max_x, max_y = fetch_grid_data(doc_url)
    print_grid(grid, max_x, max_y)
# g,mx,my=fetch_grid_data("https://docs.google.com/document/d/e/2PACX-1vQGUck9HIFCyezsrBSnmENk5ieJuYwpt7YHYEzeNJkIb9OSDdx-ov2nRNReKQyey-cwJOoEKUhLmN9z/pub")
# print_grid(g,mx,my)
end_to_end("https://docs.google.com/document/d/e/2PACX-1vQGUck9HIFCyezsrBSnmENk5ieJuYwpt7YHYEzeNJkIb9OSDdx-ov2nRNReKQyey-cwJOoEKUhLmN9z/pub")
# end_to_end("https://docs.google.com/document/u/0/d/e/2PACX-1vRMx5YQlZNa3ra8dYYxmv-QIQ3YJe8tbI3kqcuC7lQiZm-CSEznKfN_HYNSpoXcZIV3Y_O3YoUB1ecq/pub?pli=1")