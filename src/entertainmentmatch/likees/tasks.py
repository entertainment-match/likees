from entertainmentmatch.likees.services import CatalogService, UserService, VoteService, SoulmatesService
from celery.decorators import task

@task
def calculate_soulmates(user_id):
    userservice = UserService.UserService()
    soulmateservice = SoulmatesService.SoulmatesService()

    user = userservice.get(user_id)
    soulmateservice.get_soulmates_by_user(user)


