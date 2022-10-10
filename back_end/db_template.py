import boto3

"""
the template to update remote database
"""
def create_book_table(dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb')
    table = dynamodb.create_table(
        TableName='Book',
        KeySchema=[
            {
                'AttributeName': 'title',
                'KeyType': 'HASH'
            },
            {
                'AttributeName': 'year',
                'KeyType': 'RANGE'
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'title',
                'AttributeType': 'S'
            },
            {
                'AttributeName': 'year',
                'AttributeType': 'N'
            },
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 5,
            'WriteCapacityUnits': 5
        }
    )
    return table


if __name__ == '__main__':
    book_table = create_book_table()
    # print("Tablestatus:", book_table.table_status)
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table("Book")
    table.put_item(
        Item={
            'title': '02',
            'year': 2022,
            "value": '12345'
        }
    )
    print(table.get_item(
        Key = {
        'title': '02',
        'year': 2022
    }
    ))