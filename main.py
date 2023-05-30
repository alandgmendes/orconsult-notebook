def foo():
    print('ello foo')

def dadosTab1(program):
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
    return relevantValues

def dadosTab2(program, values):
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(program, 'html.parser')
    data = {}

    tables = soup.find_all('table')
    # Iterate over the tables
    for table in tables:
        # Find all input elements within the table
        input_elements = table.find_all('input')
        
        # Extract the values from the input elements
        for input_element in input_elements:
            # Get the id and value attributes of the input element
            input_id = input_element['id']
            value = input_element['value']
            
            # Store the id-value pair in the data dictionary
            data[input_id] = value

    # Print the extracted data
    for input_id, value in data.items():
        values[input_id] = value
    planilhaKeys = []
    for key, value in values.items():
        planilhaKeys.append(key)
    return values

def dadosTab3(program, valuestab2):
    from bs4 import BeautifulSoup
    values = valuestab2
    soup = BeautifulSoup(program, 'html.parser')
    class FieldCaixa:
        def __init__(self, label, value):
            self.label = label
            self.value = value

    soup = BeautifulSoup(program, 'html.parser')

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
            
            # Check if the row contains the 'fieldcaixa' class
            fieldcaixa = row.find(class_='fieldcaixa')
            
            # If 'fieldcaixa' class is present, extract the label and add it to the label field
            if fieldcaixa:
                label = fieldcaixa.text.strip()
            
            # Store the label-value pair in the data dictionary
            data[label] = value

    # Remove 'fundamentação' data
    data2 = {}
    for label, value in data.items():
        if not label.startswith('Decisão Fundamentada'):
            data2[label] = value
    def extract_info(html_content):
        soup = BeautifulSoup(html_content, 'html.parser')

        # Extracting Description
        descricao = soup.find('tr', {'class': 'descricao'}).find_next('td', {'class': 'fieldCaixa'}).text.strip()

        # Extracting Observação
        observacao = soup.find('tr', {'class': 'observacao'}).find_next('td', {'class': 'fieldCaixa'}).text.strip()

        # Extracting Critérios de Seleção
        criterios_selecao = soup.find('tr', {'class': 'criteriosDeSelecao'}).find_next('td', {'class': 'fieldCaixa'}).text.strip()

        # Storing the information in a dictionary
        info_dict = {
            'Descricao': descricao,
            'Observacao': observacao,
            'CriteriosSelecao': criterios_selecao
        }

        return info_dict
    infodict = extract_info(program)
    for label, value in infodict.items():
            data2[label] = value
    return data2

def obterDadosConsolidados(uri, inputValues):
    from pymongo import MongoClient
    import ast
    import pandas as pd
    from datetime import datetime

    client = MongoClient(uri)
    programas = client.Orconsult.programas
    relevantValues = inputValues
    # Sort the results by ID_PROGRAMA
    sort = [('ID_PROGRAMA', 1)]

    # Limit the number of results to 100
    limit = 10000

    # Perform the query
    query = {"ANO_DISPONIBILIZACAO": 2023}
    cursor = programas.find(query).sort(sort).limit(limit)

    # Iterate over the cursor and print the results
   
    def fix_date_value(value):
        if pd.isna(value) or value == 'nan':
            return 'nan'
        
        try:
            date_str = value.split('/')[0]
            date = datetime.datetime.strptime(date_str, '%d/%m/%Y').date()
            return date.strftime('%d/%m/%Y')
        except ValueError:
            return value

    # Example ill-formed objects array
    ill_formed_objects = cursor

    def create_dataframe(objects):
        return pd.DataFrame(objects)
    df = create_dataframe(ill_formed_objects)
    df['Unicity'] = df['ID_PROGRAMA'].astype(str) + df['UF_PROGRAMA'].astype(str) +\
    df['NATUREZA_JURIDICA_PROGRAMA'].astype(str) + \
    df['MODALIDADE_PROGRAMA'].astype(str) 
    
    keysrelev = relevantValues.keys()
    for key, value in relevantValues.items():
        print(f'campo: {key} || valor: {value}')
    return df