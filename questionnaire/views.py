import ast
import json
#from ipware.ip import get_trusted_ip
from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from players.models import Player, Country
from questionnaire.models import Question, Game, AnsweredQuestion

@login_required
def map(request, json_req=None):
    user = request.user
    player = Player.objects.get(user=user)
    country = player.country
    #ip = get_trusted_ip(request)
    #print "country was %s but ip is %s" % (country, ip)
    ct = dict()
    #ct['alpha3'] = ["gmb", "afg", "cub", "hun", "mng", "swe", "alb", "cyp", "ind", "mrt", "syr", "arg", "cze", "irn", "ner", "tcd", "aut", "deu", "irq", "nga", "tha", "bdi", "dnk", "isr", "nic", "tun", "bel", "dza", "ita", "nld", "tur", "bgr", "egy", "jor", "nor", "tza", "bih", "eri", "kaz", "pak", "uga", "bra", "esp", "ken", "pol", "ukr", "caf", "eth", "lbn", "rou", "usa", "can", "fin", "lby", "rus", "ven", "che", "fra", "mar", "sdn", "vnm", "chn", "gbr", "mex", "sen", "xxk", "civ", "gib", "mkd", "som", "yem", "cmr", "grc", "mli", "srb", "zaf", "cod", "gtm", "mlt", "ssd", "col", "hrv", "mmr", "svn"]
    ct['alpha3'] = ["aaaaaa", "cpv", "ind", "moz", "ssd", "afg", "cri", "iot", "mrt", "sssss", "ago", "cub", "irl", "msr", "stp", "aia", "cym", "irn", "mus", "sur", "alb", "cyp", "irq", "mwi", "svk", "and", "cze", "isl", "mys", "svn", "are", "deu", "isr", "nam", "swe", "arg", "dji", "ita", "ner", "swz", "arm", "dma", "jam", "nga", "syc", "atg", "dnk", "jey", "nic", "syr", "aus", "dom", "jjjjj", "niu", "tca", "aut", "dza", "jor", "nld", "tcd", "aze", "ecu", "jpn", "nor", "tgo", "bbbbb", "egy", "kaz", "npl", "tha", "bdi", "eri", "ken", "nru", "tjk", "bel", "esp", "kgz", "nzl", "tkl", "ben", "est", "khm", "omn", "tkm", "bfa", "eth", "kir", "ooooo", "tls", "bgd", "fin", "kna", "pak", "ton", "bgr", "fji", "kor", "pan", "tto", "bhr", "flk", "kwt", "pcn", "ttttt", "bhs", "fra", "lao", "per", "tun", "bih", "fro", "lbn", "phl", "tur", "blr", "fsm", "lbr", "plw", "tuv", "blz", "gab", "lby", "png", "twn", "bmu", "gbr", "lca", "pol", "tza", "bol", "ggy", "lie", "prk", "uga", "bra", "gha", "lka", "prt", "ukr", "brb", "gib", "lso", "pry", "ury", "brn", "gin", "ltu", "qat", "usa", "btn", "gmb", "lux", "rou", "bwa", "gnb", "lva", "rus", "uzb", "caf", "gnq", "mar", "rwa", "vat", "can", "grc", "mco", "sau", "vct", "che", "grd", "mdg", "sdn", "ven", "chl", "grl", "mdv", "sen", "vgb", "chn", "gtm", "mex", "sgp", "vnm", "civ", "guy", "mhl", "shn", "vut", "cmr", "hnd", "mkd", "slb", "wsm", "cod", "hrv", "mli", "sle", "xxk", "cog", "hti", "mlt", "slv", "yem", "cok", "hun", "mmr", "smr", "zaf", "col", "idn", "mne", "som", "zmb", "com", "imn", "mng", "srb", "zwe"]

    if json_req == "restart":
        qs = Question.get_questions(country)
        q_list = list()
        game = Game(player=player)
        game.save()
        for q in qs:
            answers = q.get_mix_answers()
            aq = AnsweredQuestion(question=q, game=game)
            aq.option1 = answers[0]
            aq.option2 = answers[1]
            aq.option3 = answers[2]
            aq.option4 = answers[3]
            aq.save()
            qd = q.to_dict()
            qd['answers'] = answers
            qd['cnt_list'] = ast.literal_eval(q.cnt_list)

            qd['ans_cnt_names'] = []
            if q._type == 'MB':
                for c in qd['answers']:
                    qd['ans_cnt_names'].append(Country.get_country(c))

            qd['game_id'] = game.id
            if q._type == 'MB':
                qd['answer_code'] = q.answer_code
            q_list.append(qd)
        ct['questions'] = q_list
        return JsonResponse(ct)
    return render(request, 'map.html', context=ct)

def finish_game(request):
    if request.is_ajax() and request.method == 'POST':
        data = json.loads(request.body)
        game = Game.objects.get(id=data['game_id'])
        game.score = data['score']
        answers = game.answeredquestion_set
        for q in data['questions']:
            a = answers.get(question_id = q['question_id'])
            a.user_answer = q['answer']
            a.save()
        game.save()
        game.player.profile.update_avg_score()
        return JsonResponse({'ok': True})
    return JsonResponse({'ok': False})


def team(request):
    return render(request, 'team.html')

def data(request):
    return render(request, 'data.html')

def about(request):
    return render(request, 'about.html')
