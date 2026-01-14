from celery import shared_task
import time
from django.core.mail import send_mail
from django.conf import settings

import logging

logger = logging.getLogger(__name__)

@shared_task
def task_activity_log(task_id, action, username):

    logger.info("Celery task started . . .")
    logger.info(
        f"Task ID {task_id} - Action: {action} - By: {username}"
    )

    return "Background task completed"


@shared_task
def send_task_assigned_email(email, task_title, assigned_by):
    send_mail(
        subject="New Task Assigned",
        message=f"You have been assigned a task: {task_title}\nAssigned by: {assigned_by}",
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[email],
    )