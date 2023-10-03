import pandas as pd


def getColumnNamesWithRow(dataFrame, search_string):
    '''
    Function for getting the Column names and Row numbers
    of the DataFrame of the search_string
    '''
    cols_total = []
    filter_column = (dataFrame.applymap(lambda x: isinstance(x, str) and search_string in x)).any(0)
    filter_row = (dataFrame.applymap(lambda x: isinstance(x, str) and search_string in x)).any(1)
    df_row_filtered = dataFrame[filter_row]
    df_row_filtered_value = df_row_filtered.fillna('no entry')

    idx_row = [row_name for row_name in df_row_filtered[df_row_filtered.columns].index]
    found = 0
    for lf, i in zip(filter_column, range(len(filter_column))):
        if lf:
            found = 1
            found_corresponding_cols = filter_column.index[i]
            cols_total.append(found_corresponding_cols)
            idx_rows = df_row_filtered_value[df_row_filtered_value[found_corresponding_cols].str.contains(search_string)].index
            print(f'Search String {search_string} fond at column:', found_corresponding_cols, 'in row ', 
            idx_rows.to_list())
    return cols_total
    if found == 0:
        print('not found')

