# API Endpoints Specification - Phase 2

## Base URL
`http://localhost:8000/api/` (development)
`https://your-domain.com/api/` (production)

## Authentication
All endpoints require authentication using JWT tokens provided by Better Auth.

## Common Response Format

### Success Response
```json
{
  "success": true,
  "data": {},
  "message": "Optional success message"
}
```

### Error Response
```json
{
  "success": false,
  "error": "Error message",
  "details": {}
}
```

## Endpoints

### 1. Get All Tasks
- **Method**: GET
- **Endpoint**: `/tasks`
- **Authentication**: Required
- **Parameters**:
  - `filter` (optional): "all", "active", "completed"
  - `search` (optional): Search query string
  - `limit` (optional): Number of tasks to return
  - `offset` (optional): Offset for pagination

- **Response**:
```json
{
  "success": true,
  "data": {
    "tasks": [
      {
        "id": 1,
        "title": "Design new landing page",
        "completed": false,
        "priority": "high",
        "tags": ["work"],
        "dueDate": "2024-02-15",
        "createdAt": "2024-01-29T10:30:00Z",
        "updatedAt": "2024-01-29T10:30:00Z"
      }
    ],
    "total": 1,
    "page": 1,
    "limit": 10
  }
}
```

### 2. Create Task
- **Method**: POST
- **Endpoint**: `/tasks`
- **Authentication**: Required
- **Request Body**:
```json
{
  "title": "New task title",
  "priority": "medium",
  "tags": ["tag1", "tag2"],
  "dueDate": "2024-02-15"
}
```

- **Validation**:
  - title: Required, 1-200 characters
  - priority: Required, one of "high", "medium", "low"
  - tags: Optional, array of strings
  - dueDate: Optional, ISO date format

- **Response**:
```json
{
  "success": true,
  "data": {
    "id": 1,
    "title": "New task title",
    "completed": false,
    "priority": "medium",
    "tags": ["tag1", "tag2"],
    "dueDate": "2024-02-15",
    "createdAt": "2024-01-29T10:30:00Z",
    "updatedAt": "2024-01-29T10:30:00Z"
  },
  "message": "Task created successfully"
}
```

### 3. Get Single Task
- **Method**: GET
- **Endpoint**: `/tasks/{id}`
- **Authentication**: Required
- **Parameters**:
  - `id` (path): Task ID

- **Response**:
```json
{
  "success": true,
  "data": {
    "id": 1,
    "title": "Task title",
    "completed": false,
    "priority": "medium",
    "tags": ["tag1"],
    "dueDate": "2024-02-15",
    "createdAt": "2024-01-29T10:30:00Z",
    "updatedAt": "2024-01-29T10:30:00Z"
  }
}
```

### 4. Update Task
- **Method**: PUT
- **Endpoint**: `/tasks/{id}`
- **Authentication**: Required
- **Parameters**:
  - `id` (path): Task ID

- **Request Body** (all optional):
```json
{
  "title": "Updated task title",
  "priority": "high",
  "tags": ["work", "important"],
  "dueDate": "2024-02-20",
  "completed": true
}
```

- **Response**:
```json
{
  "success": true,
  "data": {
    "id": 1,
    "title": "Updated task title",
    "completed": true,
    "priority": "high",
    "tags": ["work", "important"],
    "dueDate": "2024-02-20",
    "createdAt": "2024-01-29T10:30:00Z",
    "updatedAt": "2024-01-29T11:00:00Z"
  },
  "message": "Task updated successfully"
}
```

### 5. Delete Task
- **Method**: DELETE
- **Endpoint**: `/tasks/{id}`
- **Authentication**: Required
- **Parameters**:
  - `id` (path): Task ID

- **Response**:
```json
{
  "success": true,
  "data": {
    "id": 1,
    "title": "Task title",
    "completed": false,
    "priority": "medium",
    "tags": ["tag1"],
    "dueDate": "2024-02-15"
  },
  "message": "Task deleted successfully"
}
```

### 6. Toggle Task Completion
- **Method**: PATCH
- **Endpoint**: `/tasks/{id}/toggle-complete`
- **Authentication**: Required
- **Parameters**:
  - `id` (path): Task ID

- **Response**:
```json
{
  "success": true,
  "data": {
    "id": 1,
    "title": "Task title",
    "completed": true,
    "priority": "medium",
    "tags": ["tag1"],
    "dueDate": "2024-02-15",
    "updatedAt": "2024-01-29T11:00:00Z"
  },
  "message": "Task completion status updated"
}
```

### 7. Get Task Statistics
- **Method**: GET
- **Endpoint**: `/tasks/stats`
- **Authentication**: Required

- **Response**:
```json
{
  "success": true,
  "data": {
    "total": 10,
    "completed": 3,
    "active": 7,
    "byPriority": {
      "high": 2,
      "medium": 4,
      "low": 4
    }
  }
}
```

## Error Codes

| Status Code | Error Code | Message | Description |
|-------------|------------|---------|-------------|
| 400 | VALIDATION_ERROR | Validation failed | Request body validation failed |
| 401 | UNAUTHORIZED | Unauthorized | Missing or invalid authentication |
| 404 | NOT_FOUND | Task not found | Task with given ID does not exist |
| 409 | CONFLICT | Resource conflict | Attempt to create duplicate resource |
| 500 | INTERNAL_ERROR | Internal server error | Unexpected server error |

## Rate Limiting
- API requests limited to 100 requests per minute per user
- Exceeding limit returns 429 status code with retry-after header