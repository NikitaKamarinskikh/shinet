# SHINET API


## Websocket 

### Common response structure
```
{
    "key": {
        "inner_key": ["example_value"],
    },
    "other_key": 0,
    "errors": {
        "message": "message text",
        "key_name": "key name error" 
    }
}
```

### Slots response example
#### Bookings types: `registered_client`, `unregistered_client`
````
{
  "schedule": [
    {
      "id": 79,
      "bookings_list": [
        {
          "slot_id": 79,
          "service_id": 1,
          "client_id": 10,
          "start_datetime": "2023-07-01T16:20:47",
          "end_datetime": "2023-07-01T16:20:48",
          "type": "registered_client"
        },
        {
          "slot_id": 79,
          "service_id": 1,
          "client_id": 1,
          "start_datetime": "2023-07-05T06:44:09",
          "end_datetime": "2023-07-05T06:44:10",
          "type": "unregistered_client"
        },
      ],
      "start_datetime": "2023-07-01T12:00:00",
      "end_datetime": "2023-07-01T18:00:00",
      "master": 15
    }
  ],
}
````
