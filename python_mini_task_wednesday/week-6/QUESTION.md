# Job Board Application - Django REST Framework API

## Core Idea
Companies post jobs, users apply with resumes, companies review applications.

## Week 1: Setup + Core Models + REST API

### Concepts
Setup, migrations, model relationships, validations, CRUD operations, Django REST Framework, API design.

### Task

#### 1. Project Setup
Create a new Django REST API project with PostgreSQL and proper API configuration.

**Requirements:**
- Use Django 5.x (latest stable version)
- Configure PostgreSQL as the database
- Use UUID fields as primary keys for all models
- Set up Django REST Framework for API endpoints
- Configure CORS for frontend integration
- Configure proper project structure with separate apps
- API-first architecture design

#### 2. Models

Create the following models with appropriate fields:

**User Model (extend AbstractUser):**
- `first_name` - CharField
- `last_name` - CharField  
- `email` - EmailField (unique)
- `user_type` - CharField with choices (JOB_SEEKER, EMPLOYER)
- `id` - UUIDField (primary key)

**Company Model:**
- `id` - UUIDField (primary key)
- `name` - CharField
- `description` - TextField
- `created_at` - DateTimeField (auto_now_add)
- `updated_at` - DateTimeField (auto_now)

**Job Model:**
- `id` - UUIDField (primary key)
- `title` - CharField
- `description` - TextField
- `location` - CharField
- `salary` - DecimalField
- `status` - CharField with choices (ACTIVE, INACTIVE, CLOSED)
- `company` - ForeignKey to Company
- `created_at` - DateTimeField (auto_now_add)
- `updated_at` - DateTimeField (auto_now)

#### 3. Model Relationships
- User has OneToOne relationship with Company (for employer users)
- Company has many Jobs (ForeignKey relationship)
- Implement proper `related_name` attributes

#### 4. Django Model Validations
Implement the following validations using Django's validation system:

**Job Model:**
- `title`, `description`, `location`, `salary` are required
- `salary` must be greater than 0
- Custom validator for salary range (minimum wage compliance)

**Company Model:**
- `name` and `description` are required
- `name` must be unique
- `description` minimum length validation

**User Model:**
- `first_name`, `last_name`, `email`, `user_type` are required
- `email` must be unique and valid format
- Custom validator for name fields (no special characters)

#### 5. CRUD Operations
Implement Django REST Framework ViewSets for complete API functionality:

**API ViewSets:**
- **CompanyViewSet** - Full CRUD operations
- **UserViewSet** - Full CRUD operations  
- **JobViewSet** - Full CRUD operations
- Proper HTTP method handling (GET, POST, PUT, PATCH, DELETE)
- Custom actions and permissions

#### 6. API Endpoints
Create RESTful API endpoints following Django REST Framework conventions:

**API URLs:**
```python
GET/POST /api/companies/
GET/PUT/PATCH/DELETE /api/companies/{id}/
GET/POST /api/users/
GET/PUT/PATCH/DELETE /api/users/{id}/
GET/POST /api/jobs/
GET/PUT/PATCH/DELETE /api/jobs/{id}/

# Additional endpoints
GET /api/companies/{id}/jobs/ - Jobs for a specific company
GET /api/jobs/?company={id} - Filter jobs by company
```

#### 7. Serializers
Create Django REST Framework serializers with comprehensive validation:

**DRF Serializers:**
- `CompanySerializer` - Full model serialization with validation
- `UserSerializer` - User model serialization with validation  
- `JobSerializer` - Job model serialization with nested company data
- Proper field validation and custom validation methods
- Nested serialization for relationships
- Structured error responses

#### 8. Testing
Write comprehensive API tests using Django REST Framework test tools:
- Model validation tests
- API endpoint tests (CRUD operations)
- Serializer validation tests
- Relationship tests
- Authentication and permission tests
- Edge case testing

## Deliverables

1. Django REST API project with proper app structure
2. Models with validations and relationships
3. **Django REST Framework ViewSets** with full CRUD operations
4. **Serializers** with comprehensive validation logic
5. **API endpoints** following RESTful conventions
6. Comprehensive API test suite
7. Database migrations
8. uv for package management and environment management
9. API documentation (using DRF's browsable API or additional tools)
10. README.md with setup instructions and API usage guide

## Technical Constraints

1. **Django Version:** Use Django 5.x (latest stable version)
2. **Database:** PostgreSQL with proper configuration
3. **API-Only Architecture:** No Django templates or static files
4. **UUID Primary Keys:** All models must use UUID as primary key
5. **Django REST Framework:** Must use DRF for all API endpoints
6. **Validation:** Must use Django's built-in validation system
7. **RESTful Design:** Follow REST conventions for URL patterns
8. **Strong Parameters:** Implement proper serializer validation
9. **Migration Management:** Use Django migrations for database changes
10. **Environment Configuration:** Use environment variables for sensitive settings
11. **API Documentation:** Include proper API documentation
