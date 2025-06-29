# Resume Parser Service

A microservice focused on parsing resume/CV documents using LLMs and returning structured data.

## Responsibilities

- Parse resume documents and return structured data.

**What this service does:**
- Might be change later...
- Downloads resume files from signed URLs
- Extracts text from PDF/DOCX files  
- Uses LLM APIs to parse and structure resume data
- Returns parsed data in a standardized JSON format

**What this service does NOT do:**
- Might be change later...
- Database operations (handled by applicant management service)
- User authentication (handled by auth service)
- Document storage (handled by document management service)

## API Endpoints

### Parse Resume

**Request:**
```json
{
  "documentId": "d74b203e-907e-4b4a-8a07-16240ea34e5f",
  "downloadUrl": "https://signed-s3-url..."
}
```

**Response:**
```json
{
  "success": true,
  "message": "Resume parsed successfully",
  "document_id": "d74b203e-907e-4b4a-8a07-16240ea34e5f",
  "data": {
    "personal_info": { ... },
    "skills": [ ... ],
    "experience": [ ... ],
    "education": [ ... ],
    "languages": [ ... ],
    "projects": [ ... ],
    "certifications": [ ... ]
  }
}
```


## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```


2. Run the service:
   ```bash
   python run.py
   ```

## Integration

This service integrates with:
- **Document Management Service**: Receives document URLs
- **LLM APIs**: Gemini

## directory
resume-service/
├── app/
│   ├── __init__.py          # App factory (minimal)
│   ├── config.py            # Configuration
│   ├── routes/              # API routes (only parsing)
│   │   └── resume_routes.py
│   ├── services/            # Parsing logic only
│   │   └── parser_service.py
│   ├── utils/               # File utilities
│   │   └── file_utils.py
│   └── extensions.py        # Minimal extensions
│
├── .env                     # Environment variables
├── .gitignore
├── requirements.txt         # Reduced dependencies
├── run.py                   # Entry point
└── README.md