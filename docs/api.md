## GET /api/v1/jokes/count

Returns the total number of jokes in the database.

### Request
- **Method:** GET
- **Authentication:** Not required
- **Query Parameters:** None
- **Request Body:** None

### Success Response (200 OK)
```json
{
  "data": { "count": 42 },
  "status": "ok"
}

```

### Error Responses
| Status | Code | When |
|--------|------|------|
| 405 | METHOD_NOT_ALLOWED | Non-GET method used |
| 500 | INTERNAL_ERROR | Database unreachable |

### Notes
- Count includes all jokes regardless of author or status.
- Returns 0 (not an error) when no jokes exist.
- This endpoint is the prerequisite for client-side pagination of GET /api/v1/jokes.

