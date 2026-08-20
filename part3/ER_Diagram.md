## Database Schema Diagram

```mermaid
erDiagram
    USERS {
        string id PK
        string first_name
        string last_name
        string email UK
        string password
        boolean is_admin
    }

    PLACES {
        string id PK
        string title
        string description
        float price
        float latitude
        float longitude
        string owner_id FK
    }

    REVIEWS {
        string id PK
        string text
        int rating
        string user_id FK
        string place_id FK
    }

    AMENITIES {
        string id PK
        string name
    }

    PLACE_AMENITY {
        string place_id PK, FK
        string amenity_id PK, FK
    }

    USERS ||--o{ PLACES : "owns"
    USERS ||--o{ REVIEWS : "writes"
    PLACES ||--o{ REVIEWS : "receives"
    PLACES ||--o{ PLACE_AMENITY : "has"
    AMENITIES ||--o{ PLACE_AMENITY : "belongs to"
