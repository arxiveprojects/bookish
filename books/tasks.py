from celery import shared_task
from .agentic_rag import process_file
import logging

logger = logging.getLogger(__name__)

@shared_task(bind=True, max_retries=3)
def process_pdf_task(self, file_path, book_id):
    try:
        process_file(file_path, book_id)
    except Exception as e:
        logger.error(f"Error processing PDF {book_id}: {str(e)}")
        self.retry(countdown=30 * self.request.retries)