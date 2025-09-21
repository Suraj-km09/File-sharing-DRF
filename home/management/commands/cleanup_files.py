
import os
import shutil
from django.core.management.base import BaseCommand
from django.utils import timezone
from home.models import Folder

class Command(BaseCommand):
    help = 'Deletes folders and files older than 24 hours or after download'

    def handle(self, *args, **options):
        # Delete folders older than 24 hours
        time_threshold = timezone.now() - timezone.timedelta(hours=24)
        old_folders = Folder.objects.filter(created_at__lt=time_threshold)
        
        # Also delete folders that were downloaded more than 1 hour ago
        download_threshold = timezone.now() - timezone.timedelta(hours=1)
        downloaded_folders = Folder.objects.filter(
            downloaded=True, 
            download_time__lt=download_threshold
        )
        
        # Combine both querysets
        folders_to_delete = old_folders | downloaded_folders
        
        count = folders_to_delete.count()
        for folder in folders_to_delete:
            # Delete associated files from filesystem
            folder_path = os.path.join('media', str(folder.uid))
            if os.path.exists(folder_path):
                shutil.rmtree(folder_path)
            
            # Delete from database
            folder.delete()
        
        self.stdout.write(
            self.style.SUCCESS(f'Successfully deleted {count} folders')
        )