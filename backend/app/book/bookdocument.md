# book api document
## create book
> requenst
```bash
curl --location --request POST '127.0.0.1:5000/book/create_book' \
--header 'Content-Type: application/json' \
--data-raw '{"name":"xiao","author":"bai","edition":"ouudwaooh","isbn":"dwafawefwaihdfi","categories":"[dsid,dwah,dwa]","introduce":"dwahfawh fwaiofho fhaiwofh fawhi"}'
```   
> response
```josn
{
    "message": "create book successful!",
    "success": true
}
```

## modify book
>requests
```bash
curl --location --request PUT '127.0.0.1:5000/book/modify_book' \
--header 'Content-Type: application/json' \
--data-raw '{"id":1,"name":"xiaoxiaoxiao","author":"bai","edition":"ouudwaoohouudwaooh","isbn":"ouudwaooh","categories":"[dsid,dwa]","introduce":"dwahfawh fwaiofh fawhi wwwwwwwwwwwwwwwww"}'
```
>response
```json
{
    "message": "update xiaoxiaoxiao2 successful",
    "success": true
}
```

## book list
> request
```bash
curl --location --request GET '127.0.0.1:5000/book/book_list/1'
```
>response
```json
{
    "message": [
        {
            "author": "bai",
            "categories": "[dsid,dwah,dwa]",
            "edition": "ouudwaooh",
            "id": 1,
            "introduce": "dwahfawh fwaiofho fhaiwofh fawhi",
            "isbn": "dwafawefwaihdfi",
            "name": "xiao"
        }
    ],
    "success": false
}
```

## delete book
>requests
```bash
curl --location --request DELETE '127.0.0.1:5000/book/delete/2'
```
>response
```json
{
    "message": "delete xiao sussessful",
    "success": true
}
```

## book info
>requests
```bash
curl --location --request GET '127.0.0.1:5000/book/book_info/1'
```
>response
```json
{
    "message": {
        "author": "bai",
        "categories": "[dsid,dwa]",
        "edition": "ouudwaoohouudwaooh",
        "id": 1,
        "introduce": "dwahfawh fwaiofh fawhi wwwwwwwwwwwwwwwww",
        "isbn": "ouudwaooh",
        "name": "xiaoxiaoxiao2"
    },
    "success": false
}
```

## book rank
>requests
```bash
curl --location --request POST '127.0.0.1:5000/book/rank' \
--header 'Content-Type: application/json' \
--data-raw '{}'
```
>response
```json
{
    "message": "find book ranking ok",
    "result": [
        {
            "author": "bai",
            "book_id": 1,
            "book_name": "xiao",
            "categories": "[tes,dwah,dwa]",
            "cover": "https://dwdwfwa.com/dw/iwafhi.img",
            "edition": "ouudwaooh",
            "introduce": "dwahfawh fwaiofho fhaiwofh fawhi",
            "isbn": "dwafawefwaihdfi",
            "rate": 3.67
        },
        {
            "author": "bai",
            "book_id": 2,
            "book_name": "lalala",
            "categories": "[dsid,dwah,dwa]",
            "cover": "https://dwdwfwa.com/dw/iwafhi.img",
            "edition": "ouudwaooh",
            "introduce": "dwahfawh fwaiofho fhaiwofh fawhi",
            "isbn": "dwafawefwaihdfi",
            "rate": 2.0
        }
    ],
    "success": true
}
``'