# create review

```bash
curl --location --request POST '127.0.0.1:5000/review/create' \
--header 'Content-Type: application/json' \
--data-raw '{"bid":1,"uid":1,"content":"the book tell me, the book tell me the book tell me the book tell me the book tell me the book tell me the book tell me the book tell me the book tell me the book tell me the book tell me the book tell me the book tell me the book tell me the book tell me the book tell me the book tell me the book tell me the book tell me the book tell me the book tell me the book tell me the book tell me the book tell me the book tell me the book tell me the book tell me the book tell me the book tell me the book tell me the book tell me the book tell me the book tell me the book tell me the book tell me the book tell me the book tell me the book tell me the book tell me the book tell me the book tell me the book tell me the book tell me the book tell me the book tell me the book tell me the book tell me the book tell me the book tell me the book tell me the book tell me the book tell me the book tell me the book tell me the book tell me the book tell me the book tell me the book tell me the book tell me the book tell me"}'
```


# review list
```bash
curl --location --request POST '127.0.0.1:5000/review/review_list' \
--header 'Content-Type: application/json' \
--data-raw '{"bid":1,"page":1,"page_size":10}'
```