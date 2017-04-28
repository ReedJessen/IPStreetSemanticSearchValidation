import json
import collections
import requests
import pandas
import plotly.plotly as py
import plotly.graph_objs as go

def read_in_file(file):
    """reads tsv file and returns pandas data frame"""
    data = pandas.read_csv(file, sep='\t',header=None)
    return data


def search_full_text(text, ipstreet_api_key):
    """sends input text to /full_text semantic search endpoint. returns json results"""
    endpoint = 'https://api.ipstreet.com/v2/full_text'
    headers = {'x-api-key': ipstreet_api_key}
    payload = json.dumps({'raw_text': str(text),
                          'q': {
                              'start_date': '1976-01-01',
                              'start_date_type': 'application_date',
                              'end_date': '2017-03-10',
                              'end_date_type': 'application_date',
                              'applied': True,
                              'granted': True,
                              'expired': True,
                              'max_expected_results': 500,
                              'page_size': 500,
                          }
                          })
    r = requests.post(endpoint, headers=headers, data=payload)

    return r.json()

def generate_results_index(file):
    """generates counter summary dict required to produce a lorez curve of the results"""
    with open(file, 'r') as tsv:
        results = [line.strip().split('\t') for line in tsv]
    scores = []
    for result in results:
        target = result[0]
        candidates = result[1:11]

        if target in candidates:
            scores.append(candidates.index(target))
        else:
            scores.append(0)
    scores_clean = [score + 1 for score in scores]

    return collections.Counter(scores_clean)

def generate_lorez_curve_for_search_results(data):
    """
    Generate a pseudo-Lorenz curve of pecertage of results vs. retured index position i
    Input is a counter dict of position data ourputs a plotly chart
    You will need to follow the steps at https://plot.ly/python/getting-started/ to initialize online plotting
    """

    # get total number of positions in dataset
    num_of_positions = len(data)
    total_values = 0
    for value in data:
        total_values += data[value]
    print(total_values)

    #sum data set up over all positions
    x_values = [i for i in data]
    y_values = [((data[i]/total_values)*100) for i in data]
    print(x_values)
    print(y_values)

    trace0 = go.Scatter(
        x = x_values,
        y = y_values)

    layout = dict(title='Claim Text Searched Against claim_only Endpoint \n Semantic Results Lorez Curve',
                  xaxis=dict(
                      range=[.7, num_of_positions],
                      tick0=1,
                      showticklabels=True,
                      nticks=num_of_positions,
                      zeroline=True,
                      title='Index Position within Search Results '
                  ),
                  yaxis=dict(
                      title='% of Target Inputs Returned at Given Index Position',
                      type='percent',
                      range=[0, 100],
                      autotick=True,
                      showticklabels=True,
                      ticksuffix="%",


                  )
                  )



    data = [trace0]
    fig = go.Figure(data=data, layout=layout)
    url = py.plot(fig, filename='Semantic Results Lorez Curve- Claim Text Searched Against claim_only Endpoint')
    print(url)


if __name__ == '__main__':

    # Get you IP Street API key from ipstreet.com
    ipstreet_api_key = "ipstreet_api_key"

    # Read in data, can run test over data/no102.txt data/yes102.txt or any combination thereof
    texts = read_in_file("data/no102.txt")

    # create new list to hold results
    results = []
    # initiate counter to be used later
    counter = 1

    # range is based on size of test desired
    for i in range(0, 500):
        # try/catch structure here is used to mitigate possible networking issues
        while True:
            try:
                # run full_text semantic query with summary text as search seed
                response = search_full_text(texts[11][i],ipstreet_api_key)
                # extract assets from json response
                assets = [i for i in response['Assets']]
                # extract a list of the top ten most semantically similar assets, could be set to any size
                top_10 = [i['application_number'] for i in assets[0:11]]
                # insert the seed patent's application number as the first value in the list
                top_10.insert(0,str(texts[0][i]))
                # append the top ten list to the list of results
                results.append(top_10)
                # increment counter
                counter += 1
                # write list of results to file if batch size hits desired size, size can be set to any size
                if counter % 2 == 0:
                    with open('results.tsv', 'a') as file:
                        file.writelines('\t'.join(i) + '\n' for i in results)
                    results = []
            except:
                print("error, trying again")
                continue
            break

    # After all data is completed, summarize all data into a colletions.Counter object
    data = generate_results_index('results.tsv')
    # Generate a plotly charts of results, it will open in your browser
    generate_lorez_curve_for_search_results(data)