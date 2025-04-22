import timeit
import pandas as pd
from py2neo import Graph
from termcolor import colored

def init_connection() -> Graph | None:
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
def get_all_labels(graph: Graph) -> list[str]:
    """
    Function to retrieve all labels from the Neo4j database.
    """

    # define query to get all labels of the current database state
    query = "CALL db.labels()"

    # run the query and store the result as a variable
    result = graph.run(query)

    # iterate over all record in the result and store the values as a list
    labels = [record['label'] for record in result]

    # return the list of labels
    return labels


def create_worksheet_lists(excel_file: pd.ExcelFile) -> tuple[list[str]]:
    """
    Function creating two lists: one for node worksheets and one for relationship worksheets.
    It reads an Excel file containing the knowledge graph data and categorizes the sheets based on their names.
    """

    # get all sheet names from the xlsx file
    worksheets = excel_file.sheet_names

    # init node worksheet list and relationship worksheet list (initally empty)
    node_worksheets = []
    rel_worksheets = []

    # iterate over all sheets in the xlsx file
    for worksheet in worksheets:
        # check if the sheet name contains "REL" to determine if it is a relationship sheet
        if "REL" in worksheet:
            # append all worksheets that contain "REL" to the relationship worksheet list
            if len(pd.read_excel(excel_file, worksheet)) > 0:
                rel_worksheets.append(worksheet)
        else:
            # append all other worksheets to the node worksheet list
            if len(pd.read_excel(excel_file, worksheet)) > 0:
                node_worksheets.append(worksheet)
            

    # print node and relationship worksheets to the console
    print("Node worksheets: ", node_worksheets)
    print("Relationship worksheets: ", rel_worksheets, "\n")

    # return the two lists
    return node_worksheets, rel_worksheets


def create_nodes(worksheets: list[str], excel_file: pd.ExcelFile, graph) -> None:
    """
    This function creates nodes in the Neo4j database based on the data from the node worksheets.
    It reads each worksheet, formats the properties of each node, and executes a Cypher query to create the nodes.
    """

    # iterate over all node worksheets
    for worksheet in worksheets:
        # define dataframe from the worksheet
        df = pd.read_excel(excel_file, worksheet)
        
        # iterate over all rows in the dataframe
        for _, row in df.iterrows():
            # format the properties of the node because only the value should be in quotes
            formatted_props = "{" + ", ".join(f"{key}: \"{value}\"" for key, value in row.to_dict().items()) + "}"

            # add a backslash before any single quotes to avoid errors
            formatted_props = formatted_props.replace("'", "\\'")

            # define query to create a node
            query = f"CREATE (:{worksheet} {formatted_props})"

            # run the query
            graph.run(query)
        
        # print the number of nodes created for the current worksheet
        print(f"Created {len(df)} nodes with the label '{worksheet}'")

    # print the total number of node types created
    print(colored(f"All nodes have been created successfully. In total: {len(worksheets)} node types.\n", "green"))


def create_relationships(worksheets: list[str], excel_file: pd.ExcelFile, graph: Graph) -> None:
    """
    This function creates relationships in the Neo4j database based on the data from the relationship worksheets.
    It reads each worksheet, extracts the necessary information, and executes a Cypher query to create the relationships.
    """

    # iterate over all relationship worksheets
    for worksheet in worksheets:
        # define dataframe from the worksheet
        df = pd.read_excel(excel_file, worksheet)

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
    print(colored("All relationships have been created successfully.\n", "green"))


def excel_import(excel_file: pd.ExcelFile, graph: Graph) -> None:
    """
    This function imports data from an Excel file into the Neo4j database.
    """

    # create node and relationship worksheet lists
    node_worksheets, rel_worksheets = create_worksheet_lists(excel_file=excel_file)

    # create nodes and relationships in the Neo4j database by calling the specified functions
    create_nodes(worksheets=node_worksheets, excel_file=excel_file, graph=graph)
    create_relationships(worksheets=rel_worksheets, excel_file=excel_file, graph=graph)


def export_to_excel(current_time: str, graph: Graph, export_path: str) -> None:
    """
    This function exports data from the Neo4j database to an Excel file.
    """

    # define the file path where the Excel file will be saved
    file_path = f"{export_path}/export_{current_time}.xlsx"
    # create a Pandas Excel writer using Openpyxl as the engine
    writer = pd.ExcelWriter(file_path, engine='openpyxl')
    # get all labels from the graph
    labels = get_all_labels(graph=graph)

    # iterate over all labels 
    for label in labels:
        # retrieve all nodes with the current label
        nodes_result = graph.run(f"MATCH (n:{label}) RETURN properties(n) AS props")
        
        rows = [record["props"] for record in nodes_result]
        if rows:  # only write if rows exists
            # create a DataFrame from the nodes result
            nodes_df = pd.DataFrame(rows)
            # write the DataFrame to the Excel file
            nodes_df.to_excel(writer, sheet_name=label[:31], index=False)  # Excel Sheet-Namen dürfen max 31 Zeichen haben

        # retrieve all relationships for the current label
        rels_result = graph.run(f"MATCH (n:{label})-[r]->(m) RETURN n.name as start_node_name, LABELS(m)[0] as end_node_label, m.name as end_node_name, TYPE(r) as rel_type")

        # create a DataFrame from the relationships result
        rels_df = pd.DataFrame(rels_result.data())

        if not rels_df.empty:  # only create a worksheet if rels_df is not empty
            rels_df.to_excel(writer, sheet_name=f"REL_{label[:31]}", index=False)
    
    # close the Pandas Excel writer and save the file
    writer.close()

    # print the status that the export was completed successfully
    print(colored(f"Export completed. File saved at: {file_path}", "green"))


def test_query(query: str, graph: Graph) -> pd.DataFrame:
    """
    This function executes a performance test on a given Cypher query.
    """

    # measure the time of running the query 100-times with the globals variables
    execution_time = timeit.timeit("graph.run(query).data()", number=100, globals={"graph": graph, "query": query})

    # print the average execution time of all 100 runs by dividing by 100
    print(f"Average execution time: {execution_time / 100} seconds")
    
    # run the query and extract to data out of the response
    result = graph.run(query).data()

    # return the result as a dataframe
    return pd.DataFrame(result)


def reset_db(graph: Graph) -> None:
    """
    This function resets the Neo4j database by dropping all nodes and relationships.
    """

    # define the query to delete all nodes and relationships
    query = "MATCH (n) DETACH DELETE n"

    # run the query to delete all nodes and relationships
    graph.run(query)


    print(colored("!!! Database reset completed !!!", "green"))