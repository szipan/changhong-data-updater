import json
import mysql.connector
import os

# import requests


def lambda_handler(event, context):
    """Sample pure Lambda function

    Parameters
    ----------
    event: dict, required
        API Gateway Lambda Proxy Input Format

        Event doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html#api-gateway-simple-proxy-for-lambda-input-format

    context: object, required
        Lambda Context runtime methods and attributes

        Context doc: https://docs.aws.amazon.com/lambda/latest/dg/python-context-object.html

    Returns
    ------
    API Gateway Lambda Proxy Output Format: dict

        Return doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html
    """

    # try:
    #     ip = requests.get("http://checkip.amazonaws.com/")
    # except requests.RequestException as e:
    #     # Send some context about this error to Lambda Logs
    #     print(e)

    #     raise e

    # Retrieve MySQL database connection details from Lambda environment variables
    db_host = os.environ['DB_HOST']
    db_user = os.environ['DB_USER']
    db_password = os.environ['DB_PASSWORD']
    db_name = os.environ['DB_NAME']
    sql_statement = event['sql']
    
    try:
        # Connect to the MySQL database
        connection = mysql.connector.connect(
            host=db_host,
            user=db_user,
            password=db_password,
            database=db_name
        )
        
        print("SQL statement to be executed: " + sql_statement)
        if connection.is_connected():
            print("Connected to MySQL database")

            # Create a cursor object to execute SQL queries
            cursor = connection.cursor()

            # Execute the SQL statement
            cursor.execute(sql_statement)
            connection.commit()
    except mysql.connector.Error as err:
        print("Error: {}".format(err))


    finally:
        # Close cursor and connection
        if 'cursor' in locals() and cursor is not None:
            cursor.close()
        if 'connection' in locals() and connection.is_connected():
            connection.close()
            print("MySQL connection is closed")

    return {
        'statusCode': 200,
        'body': 'SQL query executed successfully'
    }
