import csv
import re
from re import search

def find_something(pat, _str):
    m = re.match(pat, _str)
    if m is not None:
        #print "found this: "+ m.group(0)
        return m.group(0)
    else:
        return None

category = "USER REGION" #initial category
region = "ITALY" #initial country
_type = ""
help_text = ""
data_source = ""
data_source_link = ""
license_link = ""
fixed = True
zoom_list = None
rnd_list = None
with open("questions_to_parse3.txt", "Ur") as q:
    with open("mb_countries.csv", "wb") as done:
        writer = csv.writer(done, delimiter=";", quotechar="\"", quoting=csv.QUOTE_MINIMAL)
        #writer.writerow(["category", "region", "type", "question", "answer", "help_text", "data_source", "data_source_link", "license_link", "fixed"])
        writer.writerow(["question", "category", "region", "_type", "answer", "cou_list"])
        line = q.readline()
        while (line != ''):
            write = False
            if line.find("QUESTIONS ON THE") != -1:
                category_start = line.find("QUESTIONS ON THE ") + len("QUESTIONS ON THE ") #saves category mediterranean area and general overview
                category = line[category_start:-1]
                region = ""
            if line.find("COUNTRY") != -1:
                #save the country!
                start_region = line.find("COUNTRY: ") + len("COUNTRY: ")
                region = line[start_region:-1]

            #is a question?
            else:
                q_start = find_something('[0-9]+\.\s+', line)
                if q_start and (line.endswith('MC\n') or line.endswith('TB\n') or
                                line.endswith('TF\n') or line.endswith('MB\n')):
                    #it's a question!!!
                    question = line[len(q_start):-4]
                    _type = line[-3:-1]
                #answer?
                elif line.find("(correct answer)") != -1:
                    end_ans = line.find("(correct answer)")
                    answer = line[3:end_ans-1]
                elif line.find("CORRECT ANSWER: ") != -1 and _type == "TF":
                    start_ans = line.find("CORRECT ANSWER: ") + len("CORRECT ANSWER: ")
                    answer = line[start_ans:-1]
                elif line.find("extracted randomly ") != -1:
                    fixed = False
                #check for answersss!
                elif line.find("b) ") != -1:
                    answer2 = line[3:-1]
                elif line.find("c) ") != -1:
                    answer3 = line[3:-1]
                elif line.find("d) ") != -1:
                    answer4 = line[3:-1]
                elif search("CHECK: the correct answer is ", line) != None and _type == "TB":
                    start = search("CHECK: the correct answer is ", line).end()
                    end = search("CHECK: the correct answer is (\d|\.|\%)+ ", line).end()
                    answer = line[start:end-1]
                    if answer[-1] == ".":
                        answer = answer[:-1]
                elif line.find("MESSAGE TO SHOW THE CORRECT ANSWER") != -1:
                    start_help = line.find("MESSAGE TO SHOW THE CORRECT ANSWER")
                    line = q.readline()
                    help_text = line[:-1]
                elif line.find("Map:") != -1 :
                    start = line.find("Map: ") + len("Map: ")
                    zoom_list = line[start:-1].split(", ")
                    write = True #got it all!
                if line.find("""randomly among [""") != -1 and \
                line.find("""randomly among [Jan""") == -1 and \
                line.find("""randomly among [Feb""") == -1 and \
                line.find("""randomly among [10""") == -1:
                    start = line.find("""randomly among [""") + len("""randomly among [""")
                    rnd_list = line[start:line.find("]")].split(", ")
                    answer = rnd_list[0]
                    #print "help text"+help_text
                elif line.find("Data Source:") != -1:
                    data_source = line[line.find("Data Source:")+13:-1]
                    #print "data source: "+data_source
                elif line.find("Data Source Link") != -1:
                    data_source_link = line[line.find("Data Source Link:")+18:-1]
                elif line.find("License Link") != -1:
                    license_link = line[line.find("License Link:")+14:-1]

                if write:
                        #(category, region, _type, question, answer, help_text, data_source, data_source_link, license_link)
                    #writer.writerow([category, region, _type, question, answer, help_text, data_source, data_source_link, license_link, fixed])
                    #if fixed == True and (_type == 'MB' or _type == 'MC'):
                    if region=='':
                        region = '\N'
                        
                        #if _type == 'MB':
                        #    writer.writerow

                            #for fixed questions only!
                    #print "writing: %s|%s|%s|%s|%s" % (question, region, answer, cou_list, _type)
                    if (zoom_list or rnd_list):
                        if rnd_list:
                            l = rnd_list
                        else:
                            l = zoom_list
                        writer.writerow([question, category, region, _type, answer, l])
                    _type = question = answer = help_text = data_source = rnd_list = zoom_list = data_source_link = license_link = None
                    fixed = True
            line = q.readline()
print "done!!"
