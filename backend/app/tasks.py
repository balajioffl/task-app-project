from celery import shared_task
import time
import logging

logger = logging.getLogger(__name__)

@shared_task
def task_activity_log(task_id, action, username):

    logger.info("Celery task started . . .")
    logger.info(
        f"Task ID {task_id} - Action: {action} - By: {username}"
    )

    return "Background task completed"
