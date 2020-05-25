


def column_dropdown_options():
    good_columns = ['total_cases_per_million',
       'total_deaths_per_million',
                    'total_cases', 'new_cases',
                    'total_deaths', 'new_deaths',
                    'new_cases_per_million', 
                    'new_deaths_per_million'
                    ]
    options = [{'label': column.replace('_', ' '), 'value': column} for column in good_columns]
    return options
