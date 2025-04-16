
import pandas as pd
from py2neo import Graph

def init_connection():
    """
    Function initializes a connection to the Neo4j database.
    """
    # define connection parameters
    DATABASE_URL = "bolt://localhost:7687"
    USERNAME = "neo4j"
    PASSWORD = "test1234"

    # create graph object with the connection parameters
    graph = Graph(DATABASE_URL, auth=(USERNAME, PASSWORD))

    # check if the connection is successful
    if graph:
        print("Connected to the database")
        return graph


# function to create a node with a label and properties 
def get_all_labels(graph: Graph):
    """
    Function to retrieve all labels from the Neo4j database.
    """
    query = "CALL db.labels()"
    result = graph.run(query)
    labels = [record['label'] for record in result]
    return labels


def create_worksheet_lists(file_path: pd.ExcelFile):
    """
    Function creating two lists: one for node worksheets and one for relationship worksheets.
    It reads an Excel file containing the knowledge graph data and categorizes the sheets based on their names.
    """

    # get all sheet names from the xlsx file
    worksheets = file_path.sheet_names

    # init node worksheet list and relationship worksheet list (initally empty)
    node_worksheets = []
    rel_worksheets = []

    # iterate over all sheets in the xlsx file
    for worksheet in worksheets:
        # check if the sheet name contains "REL" to determine if it is a relationship sheet
        if "REL" in worksheet:
            # append all worksheets that contain "REL" to the relationship worksheet list
            if len(pd.read_excel(file_path, worksheet)) > 0:
                rel_worksheets.append(worksheet)
        else:
            # append all other worksheets to the node worksheet list
            if len(pd.read_excel(file_path, worksheet)) > 0:
                node_worksheets.append(worksheet)
            

    # print node and relationship worksheets to the console
    print("Node worksheets: ", node_worksheets)
    print("Relationship worksheets: ", rel_worksheets, "\n")

    # return the two lists
    return node_worksheets, rel_worksheets


def create_nodes(worksheets: list[str], file_path: pd.ExcelFile, graph):
    """
    This function creates nodes in the Neo4j database based on the data from the node worksheets.
    It reads each worksheet, formats the properties of each node, and executes a Cypher query to create the nodes.
    """

    # iterate over all node worksheets
    for worksheet in worksheets:
        # define dataframe from the worksheet
        df = pd.read_excel(file_path, worksheet)
        
        # iterate over all rows in the dataframe
        for _, row in df.iterrows():
            # format the properties of the node because only the value should be in quotes
            formatted_props = "{" + ", ".join(f"{key}: \"{value}\"" for key, value in row.to_dict().items()) + "}"

            # define query to create a node
            query = f"CREATE (:{worksheet} {formatted_props})"

            # run the query
            graph.run(query)
        
        # print the number of nodes created for the current worksheet
        print(f"Created {len(df)} nodes with the label '{worksheet}'")

    # print the total number of node types created
    print("All nodes have been created successfully. In total: ", len(worksheets), " node types.\n")



def create_relationships(worksheets: list[str], file_path: pd.ExcelFile, graph: Graph):
    """
    This function creates relationships in the Neo4j database based on the data from the relationship worksheets.
    It reads each worksheet, extracts the necessary information, and executes a Cypher query to create the relationships.
    """

    # iterate over all relationship worksheets
    for worksheet in worksheets:
        # define dataframe from the worksheet
        df = pd.read_excel(file_path, worksheet)

        # iterate over all rows in the dataframe
        for _, row in df.iterrows():
            # init variables
            start_node_label = worksheet.split("_")[1]
            start_node_name = row['start_node_name']
            end_node_label = row['end_node_label']
            end_node_name = row['end_node_name']
            rel_type = row['rel_type']

            # define query to create a relationship
            query = f"MATCH (n:{start_node_label} {{name: '{start_node_name}'}}), (m:{end_node_label} {{name: '{end_node_name}'}}) CREATE (n)-[:{rel_type}]->(m)"

            # run query
            graph.run(query)

        # print the number of relationships created for the current worksheet
        print(f"Created {len(df)} relationships from a '{worksheet.split("_")[1]}' node")

    # print the total number of relationship types created
    print("All relationships have been created successfully.\n")