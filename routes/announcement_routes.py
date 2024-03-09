from fastapi import APIRouter
import services.announcement_services as announcement_services
from DTOs.announcementDTO import AnnouncementDTO

router = APIRouter()


@router.get('/getAllAnnouncements')
async def get_announcements():
    return announcement_services.get_announcement_list()


@router.get('/getAnnouncementById/{announcement_id}')
async def create_announcements(announcement_id: int):
    return announcement_services.get_announcement_by_id(announcement_id=announcement_id)


@router.post('/createAnnouncement')
async def create_announcements(announcement: AnnouncementDTO):
    return announcement_services.create_announcement(announcement_dto=announcement)


@router.patch('/updateAnnouncement/{announcement_id}')
async def create_announcements(announcement: AnnouncementDTO, announcement_id: int):
    return announcement_services.update_announcement(announcement_dto=announcement, announcement_id=announcement_id)


@router.delete('/deleteAnnouncement/{announcement_id}')
async def create_announcements(announcement_id: int):
    return announcement_services.delete_announcement(announcement_id=announcement_id)
