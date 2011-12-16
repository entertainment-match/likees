from entertainmentmatch.likees.services import CatalogService, UserService, VoteService, SoulmatesService
from entertainmentmatch.likees import tasks
from django.conf import settings
from multiprocessing import Process

class SoulmatesMiddleware(object):
    def process_request(self,request):

        if request.path.startswith('/dynjs'):
            return

        if request.user.id is None:
            return

        voteservice = VoteService.VoteService()
      
        recalculate = False
        current_votes = None
        last_update = 0
        if 'last_soulmates_update' in request.session:
            last_update = request.session['last_soulmates_update']
        if request.session is not None:
            if not 'total_voted' in request.session:
                current_votes = voteservice.get_user_votes_num(request.user.id)
                request.session['total_voted'] = current_votes
                recalculate = True
            else:
                num = request.session['total_voted']
                recalculate =  num - last_update >= 10
                current_votes = num
        if recalculate:
            request.session['last_soulmates_update'] = current_votes
            result = tasks.calculate_soulmates.apply_async(args=[request.user.id])
            #result.ready()
            #p = Process(target=self._bulk_action, args=([request.user.id]))
            #p.start()

       
