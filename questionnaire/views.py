import ast
import json
import base64
import math
from Crypto.Cipher import AES
from Crypto import Random
from cStringIO import StringIO
#from ipware.ip import get_trusted_ip
from django.core import management
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.utils.encoding import smart_str
from django.contrib.auth.decorators import login_required
from players.models import Player, Country
from questionnaire.models import Question, Game, AnsweredQuestion

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

BLOCK_SIZE = 16

def pad(data):
    length = 16 - (len(data) % 16)
    return (data + chr(length)*length)

def unpad(data):
    return data[:-ord(data[-1])]

def encrypt(message, passphrase):
    IV = Random.new().read(BLOCK_SIZE)
    aes = AES.new(passphrase, AES.MODE_CFB, IV, segment_size=128)
    return base64.b64encode(IV + aes.encrypt(pad(message)))

def decrypt(encrypted, passphrase):
    encrypted = base64.b64decode(encrypted)
    IV = encrypted[:BLOCK_SIZE]
    aes = AES.new(passphrase, AES.MODE_CFB, IV, segment_size=128)
    return unpad(aes.decrypt(encrypted[BLOCK_SIZE:]))

@login_required
def map(request, json_req=None):
    #ip = get_trusted_ip(request)
    #print "country was %s but ip is %s" % (country, ip)

    if json_req == "restart":
        ct_rs = dict()

        user = request.user
        player = Player.objects.get(user=user)
        country = player.country

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

            #encrypt the answer
            qd_answer_encypted = encrypt(qd['answer'], "1234567890123456")
            qd['answer'] = qd_answer_encypted

            qd['answers'] = answers
            qd['cnt_list'] = ast.literal_eval(q.cnt_list)

            qd['ans_cnt_names'] = []
            if q._type == 'MB':
                for c in qd['answers']:
                    qd['ans_cnt_names'].append(Country.get_country(c))

            qd['game_id'] = game.id
            if q._type == 'MB':
                qd['answer_code'] = encrypt(q.answer_code, "1234567890123456")
            q_list.append(qd)
        ct_rs['questions'] = q_list
        return JsonResponse(ct_rs)

    ct = dict()
    #ct['alpha3'] = ["gmb", "afg", "cub", "hun", "mng", "swe", "alb", "cyp", "ind", "mrt", "syr", "arg", "cze", "irn", "ner", "tcd", "aut", "deu", "irq", "nga", "tha", "bdi", "dnk", "isr", "nic", "tun", "bel", "dza", "ita", "nld", "tur", "bgr", "egy", "jor", "nor", "tza", "bih", "eri", "kaz", "pak", "uga", "bra", "esp", "ken", "pol", "ukr", "caf", "eth", "lbn", "rou", "usa", "can", "fin", "lby", "rus", "ven", "che", "fra", "mar", "sdn", "vnm", "chn", "gbr", "mex", "sen", "xxk", "civ", "gib", "mkd", "som", "yem", "cmr", "grc", "mli", "srb", "zaf", "cod", "gtm", "mlt", "ssd", "col", "hrv", "mmr", "svn"]
    ct['alpha3'] = ["aaaaaa", "cpv", "ind", "moz", "ssd", "afg", "cri", "iot", "mrt", "sssss", "ago", "cub", "irl", "msr", "stp", "aia", "cym", "irn", "mus", "sur", "alb", "cyp", "irq", "mwi", "svk", "and", "cze", "isl", "mys", "svn", "are", "deu", "isr", "nam", "swe", "arg", "dji", "ita", "ner", "swz", "arm", "dma", "jam", "nga", "syc", "atg", "dnk", "jey", "nic", "syr", "aus", "dom", "jjjjj", "niu", "tca", "aut", "dza", "jor", "nld", "tcd", "aze", "ecu", "jpn", "nor", "tgo", "bbbbb", "egy", "kaz", "npl", "tha", "bdi", "eri", "ken", "nru", "tjk", "bel", "esp", "kgz", "nzl", "tkl", "ben", "est", "khm", "omn", "tkm", "bfa", "eth", "kir", "ooooo", "tls", "bgd", "fin", "kna", "pak", "ton", "bgr", "fji", "kor", "pan", "tto", "bhr", "flk", "kwt", "pcn", "ttttt", "bhs", "fra", "lao", "per", "tun", "bih", "fro", "lbn", "phl", "tur", "blr", "fsm", "lbr", "plw", "tuv", "blz", "gab", "lby", "png", "twn", "bmu", "gbr", "lca", "pol", "tza", "bol", "ggy", "lie", "prk", "uga", "bra", "gha", "lka", "prt", "ukr", "brb", "gib", "lso", "pry", "ury", "brn", "gin", "ltu", "qat", "usa", "btn", "gmb", "lux", "rou", "bwa", "gnb", "lva", "rus", "uzb", "caf", "gnq", "mar", "rwa", "vat", "can", "grc", "mco", "sau", "vct", "che", "grd", "mdg", "sdn", "ven", "chl", "grl", "mdv", "sen", "vgb", "chn", "gtm", "mex", "sgp", "vnm", "civ", "guy", "mhl", "shn", "vut", "cmr", "hnd", "mkd", "slb", "wsm", "cod", "hrv", "mli", "sle", "xxk", "cog", "hti", "mlt", "slv", "yem", "cok", "hun", "mmr", "smr", "zaf", "col", "idn", "mne", "som", "zmb", "com", "imn", "mng", "srb", "zwe"]
    return render(request, 'map.html', context=ct)

def weighted_score(weight, trem):
    if trem>15 and trem<=30:
        q_score = weight*1
    elif trem>7 and trem<=15:
        q_score = weight*0.9
    else:
        q_score = weight*0.8
    return q_score

def isInt(str):
    try:
        str2int = int(str)
        return True
    except ValueError:
        return False

def isFloat(str):
    try:
        str2float = float(str)
        return True
    except ValueError:
        return False

def evaluate_answer(type, right_answer, given_answer):
    if type == "MC":
        if right_answer.capitalize() == given_answer:
            result = True
        else:
            result = False
    elif type == "MB" or type == "TF":
        if right_answer == given_answer:
            result = True
        else:
            result = False
    else:
        if (isInt(given_answer) or isFloat(given_answer)):
            if "%" in right_answer:
                lowerBound = float(right_answer[:-1])*9/10
                upperBound = float(right_answer[:-1])*11/10
                if upperBound > 100:
                    upperBound = 100
            else:
                lowerBound = float(right_answer)*8/10
                upperBound = float(right_answer)*12/10

            if float(given_answer) >= lowerBound and given_answer <= upperBound:
                result = True
            else:
                result = False
        else:
            print "given answer is not a float or a number!"
            result = False

    return result

def finish_game(request):
    if request.is_ajax() and request.method == 'POST':
        data = json.loads(request.body)
        game = Game.objects.get(id=data['game_id'])

        g_score = 0.0
        for q in data['questions']:
            question = Question.objects.get(id=q['question_id'])
            type = question._type

            if type == "MB":
                right_answer = question.answer_code
            else:
                right_answer = question.answer

            given_answer = q['answer']

            tf = evaluate_answer(type, right_answer, given_answer)

            print given_answer + " " + right_answer + " %r" % tf

            if tf == True:
                if type == "TF":
                    q_score = weighted_score(0.5, q['trem'])
                    g_score += q_score
                    print q_score, g_score
                elif type == "TB":
                    q_score = weighted_score(1.5, q['trem'])
                    g_score += q_score
                    print q_score, g_score
                else:
                    q_score = weighted_score(1.0, q['trem'])
                    g_score += q_score
                    print q_score, g_score

        print "g_score: %f" % g_score
        game.score = g_score

        answers = game.answeredquestion_set
        for q in data['questions']:
            a = answers.get(question_id = q['question_id'])
            a.user_answer = q['answer']
            a.save()
        game.save()
        game.player.profile.update_avg_score()
        return JsonResponse({'ok': True, 'score': g_score})
    return JsonResponse({'ok': False})


def team(request):
    return render(request, 'team.html')

def data(request):
    return render(request, 'data.html')

def challenge(request):
    return render(request, 'challenge.html')

def about(request):
    return render(request, 'about.html')

def free_data(request):
    buf = StringIO()
    management.call_command('dumpdata', 'questionnaire.game', stdout=buf)
    management.call_command('dumpdata', 'questionnaire.answeredquestion', stdout=buf)
    #management.call_command('dumpdata', 'players', stdout=buf)
    buf.seek(0)
    fname = 'migrate.json'
    with open(fname, 'w') as f:
        f.write(buf.read())
    response = HttpResponse(open(fname), content_type='application/force-download')
    response['Content-Disposition'] = 'attachment; filename=%s' % smart_str(fname)
    response['X-Sendfile'] = smart_str(fname)
    return response
