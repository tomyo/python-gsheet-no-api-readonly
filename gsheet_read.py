import requests
import json
import re
from typing import List, Dict, Any

def table_to_objects(gsheet_array: List[List[Any]]) -> List[Dict[str, Any]]:
    """
    Converts a 2D array (representing Google Sheets data) into a list of dictionaries.

    Args:
        gsheet_array (List[List[Any]]): A 2D array where the first row contains headers and subsequent rows contain data.

    Returns:
        List[Dict[str, Any]]: A list of dictionaries where each dictionary represents a row in the spreadsheet,
                              with keys corresponding to the column headers.
    """
    # Array containing the JSON objects
    final_object: List[Dict[str, Any]] = []

    # Iterate over the gsheet array from the second row to the end
    for row_values in range(1, len(gsheet_array)):
        # Each row in the gsheet array will represent an object
        row = gsheet_array[row_values]
        # Create a temporary object to hold the values of each row
        temp_object: Dict[str, Any] = {}
        
        # Loop over each value in the row
        for index_value in range(len(row)):
            # Get each value and assign it as a value to the respective key
            value = row[index_value]
            temp_object[gsheet_array[0][index_value]] = value

        # Append the current temporary object to the final array of objects
        final_object.append(temp_object)

    # Return the final array of JSON objects
    return final_object

def get_sheet_data(id: str = "", gid: str = "") -> List[Dict[str, Any]]:
    """
    Fetches data from a Google Sheet.

    Returns:
        List[Dict[str, Any]]: A list of dictionaries where each dictionary represents a row in the spreadsheet,
                              with keys corresponding to the column headers.
    """
    # Google Sheets document ID and sheet GID

    url = f"https://docs.google.com/spreadsheets/d/{id}/gviz/tq?tqx=out:json&tq?gid={gid}"
    
    # Fetch the data from the Google Sheets URL
    response = requests.get(url)
    txt = response.text

    # Extract the JSON part from the fetched data
    match = re.search(r'(?<="table":).*(?=}\);)', txt)
    json_string = match.group(0) if match else ""
    json_data = json.loads(json_string)
    table: List[List[Any]] = []

    # Extract headers from the JSON data
    row: List[str] = [col['label'] for col in json_data['cols']]
    table.append(row)
    
    # Extract rows from the JSON data
    for r in json_data['rows']:
        row = []
        for cell in r['c']:
            # Get the cell value, prefer the formatted value if available
            value = cell.get('f', cell['v']) if cell else ""
            row.append(value)
        table.append(row)

    # Convert the table array to a list of JSON objects
    return table_to_objects(table)

