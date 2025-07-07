import json
from datetime import datetime
from google import genai
from google.genai import types
from flask import current_app
import os
import mimetypes
import httpx


class ResumeParserService:
    """Service for parsing resume documents using Google Gemini"""

    def __init__(self):

        self.client = genai.Client()

    def parse_resume_from_url(self, document_id, download_url):
        """
        Downloads a resume from a URL, parses it using Gemini, and returns structured data.
        """
        try:
            current_app.logger.info(f"Starting resume parsing for document {document_id}")

            # Step 1: Fetch file content from URL
            try:
                response = httpx.get(download_url, follow_redirects=True, timeout=30)
                response.raise_for_status()
                file_bytes = response.content
                mime_type = self._get_mime_type(response)
            except httpx.RequestError as e:
                current_app.logger.error(f"Failed to download file for document {document_id} from {download_url}: {e}")
                return {'success': False, 'error': 'Failed to download file from URL'}

            # Step 2: Extract structured data with Gemini
            mime_type = self._get_mime_type(response)
            parsed_data = self._extract_structured_data_with_gemini(file_bytes, mime_type)
            if not parsed_data:
                return {'success': False, 'error': 'Failed to parse resume with Gemini'}

            # Step 3: Validate and clean the parsed data
            validated_data = self._validate_and_clean_data(parsed_data)

            current_app.logger.info(f"Successfully parsed resume for document {document_id}")
            return {
                'success': True,
                'document_id': document_id,
                'parsed_data': validated_data
            }

        except Exception as e:
            current_app.logger.error(f"Error parsing resume for document {document_id}: {str(e)}")
            return {'success': False, 'error': f'Internal parsing error: {str(e)}'}

    def _extract_structured_data_with_gemini(self, file_bytes, mime_type):
        """Use Gemini to extract structured data from file bytes"""
        try:
            prompt = self._create_llm_prompt()
            file_part = types.Part.from_bytes(data=file_bytes, mime_type=mime_type)

            response = self.client.models.generate_content(
                model="gemini-2.5-flash",
                contents=[prompt, file_part]
            )
            response_text = response.text.strip() if response.text else ""
            current_app.logger.debug(f"LLM response for: {response_text[:200]}...")

            if response_text.startswith("```json"):
                response_text = response_text[7:-3].strip()
            return json.loads(response_text)

        except json.JSONDecodeError:
            current_app.logger.error(f"Could not extract JSON from LLM response: {response_text}")
            raise Exception("Failed to parse JSON response from LLM")
        except Exception as e:
            current_app.logger.error(f"Gemini API error: {str(e)}")
            return None

    def _get_mime_type(self, response: httpx.Response) -> str:
        """Determines the MIME type from the HTTP response headers or URL."""
        content_type = response.headers.get('Content-Type')
        if content_type and '/' in content_type:
            return content_type.split(';')[0].strip()
        
        mime_type, _ = mimetypes.guess_type(str(response.url))
        if mime_type:
            return mime_type
        
        current_app.logger.warning(f"Could not determine MIME type for {response.url}. Defaulting to application/pdf.")
        return 'application/pdf'

    def _create_llm_prompt(self):
        """Loads the LLM prompt from a file."""
        prompt_path = os.path.join(current_app.root_path, 'prompts', 'resume_parser_prompt.txt')
        try:
            with open(prompt_path, 'r', encoding='utf-8') as f:
                return f.read()
        except FileNotFoundError:
            current_app.logger.error(f"Prompt file not found at {prompt_path}")
            raise

    def _validate_and_clean_data(self, parsed_data):
        """Validate and clean the parsed data"""
        validated_data = {
            'applicant': parsed_data.get('applicant', {}),
            'skills': parsed_data.get('skills', []),
            'experience': parsed_data.get('experience', []),
            'education': parsed_data.get('education', []),
            'languages': parsed_data.get('languages', []),
            'projects': parsed_data.get('projects', []),
            'certifications': parsed_data.get('certifications', [])
        }

        # Validate and clean dates
        for item in validated_data['experience']:
            item['start_date'] = self._validate_date_format(item.get('start_date'))
            item['end_date'] = self._validate_date_format(item.get('end_date'))
        
        for item in validated_data['education']:
            item['start_date'] = self._validate_date_format(item.get('start_date'))
            item['end_date'] = self._validate_date_format(item.get('end_date'))
            
        for item in validated_data['projects']:
            item['start_date'] = self._validate_date_format(item.get('start_date'))
            item['end_date'] = self._validate_date_format(item.get('end_date'))
            
        for item in validated_data['certifications']:
            item['issue_date'] = self._validate_date_format(item.get('issue_date'))
            item['expiration_date'] = self._validate_date_format(item.get('expiration_date'))

        return validated_data

    def _validate_date_format(self, date_string):
        """Validate date format and return standardized format or None"""
        if not date_string:
            return None
        
        # Supported input formats
        formats_to_try = ['%Y-%m-%d', '%Y-%m', '%Y']
        
        for fmt in formats_to_try:
            try:
                parsed_date = datetime.strptime(date_string, fmt)
                return parsed_date.strftime('%Y-%m-%d')
            except ValueError:
                continue
        
        current_app.logger.warning(f"Could not parse date: {date_string}")
        return None
