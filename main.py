def foo():
    print('ello foo')

def addData1(program):
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(program, 'html.parser')

    #print(soup.prettify())
    rows = soup.find_all('tr')

    data = {}

    # Iterate over the rows
    for row in rows:
        # Find the cells (td) in each row
        cells = row.find_all('td')
        
        # Extract the label and value from the cells
        if len(cells) == 2:
            label = cells[0].text.strip()
            value = cells[1].text.strip()
            
            # Store the label-value pair in the data dictionary
            data[label] = value

    #remove fundamentação data
    relevantValues = {}
    for label, value in data.items():
        if (not label.startswith('Decisão Fundamentada')):
            relevantValues[label] = value
