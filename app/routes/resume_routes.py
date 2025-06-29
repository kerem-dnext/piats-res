# Creating app/routes/resume_routes.py - API routes
from flask import Blueprint, request, jsonify
from app.services.parser_service import ResumeParserService
import uuid

resume_bp = Blueprint('resume', __name__)

@resume_bp.route('/resume/parse', methods=['POST'])
def parse_resume():
    """
    Parse resume from a document URL.
    This endpoint downloads a resume file from the provided URL, parses it to extract structured data, and returns the extracted information.
    ---
    tags:
      - Resume Parsing
    parameters:
      - in: body
        name: body
        required: true
        schema:
          id: ResumeParseRequest
          required:
            - documentId
            - downloadUrl
          properties:
            documentId:
              type: string
              format: uuid
              description: The unique identifier for the document.
              example: "123e4567-e89b-12d3-a456-426614174000"
            downloadUrl:
              type: string
              format: uri
              description: The public URL to download the resume file.
              example: "https://example.com/path/to/resume.pdf"
    responses:
      200:
        description: Resume parsed successfully.
        schema:
          id: ResumeParseSuccess
          properties:
            success:
              type: boolean
              example: true
            message:
              type: string
              example: "Resume parsed successfully"
            document_id:
              type: string
              format: uuid
              example: "123e4567-e89b-12d3-a456-426614174000"
            data:
              type: object
              description: The structured data extracted from the resume.
      400:
        description: Bad request, such as missing fields or invalid UUID.
      500:
        description: Internal server error during parsing.
    """
    try:
        # Get request data
        data = request.get_json()
        
        # Validate required fields
        if not data or 'documentId' not in data or 'downloadUrl' not in data:
            return jsonify({
                'success': False,
                'error': 'Missing required fields: documentId and downloadUrl'
            }), 400
        
        document_id = data['documentId']
        download_url = data['downloadUrl']
        
        # Validate document_id is a valid UUID
        try:
            uuid.UUID(document_id)
        except ValueError:
            return jsonify({
                'success': False,
                'error': 'Invalid documentId format'
            }), 400
        
        # Initialize parser service
        parser_service = ResumeParserService()
        
        # Parse the resume
        result = parser_service.parse_resume_from_url(document_id, download_url)
        
        if result.get('success'):
            return jsonify({
                'success': True,
                'message': 'Resume parsed successfully',
                'document_id': result['document_id'],
                'data': result['parsed_data']
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': result.get('error', 'Unknown error occurred')
            }), 500
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Internal server error: {str(e)}'
        }), 500

@resume_bp.route('/resume/health', methods=['GET'])
def health_check():
    """
    Health check endpoint for the service.
    Returns the current health status of the resume parser service.
    ---
    tags:
      - Health Check
    responses:
      200:
        description: Service is healthy.
        schema:
          id: HealthStatus
          properties:
            status:
              type: string
              example: "healthy"
            service:
              type: string
              example: "resume-parser"
            version:
              type: string
              example: "1.0.0"
    """
    return jsonify({
        'status': 'healthy',
        'service': 'resume-parser',
        'version': '1.0.0'
    }), 200

