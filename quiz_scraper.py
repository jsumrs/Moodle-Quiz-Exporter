import csv
import re
from bs4 import BeautifulSoup


def clean_string(content):
    if content:
        return re.sub(r"[\n\s\t\r]+", " ", content) 
    else:
        return ''

def get_mc_questions(filepath):
    with open(filepath) as fp:
        soup = BeautifulSoup(fp, 'html.parser')


    mc_questions = []
    soup = soup.select('div.que.multichoice.deferredfeedback')
    for q_block in soup:
        # Find the tag the question resides in
        q_text = q_block.find(class_='qtext')
        if not q_text:
            continue

        # Navigate down a child to the answer's tag
        q_div = q_text.div
        if not q_div:
            continue
        question = clean_string(q_div.string)


        # Find the tag that the possible answers are contained in
        a_block = q_block.find(class_='answer')
        if not a_block:
            continue

        # Grab a list of the possible answers within the answer tag
        options = a_block.find_all(class_='ml-1')
        if len(options) == 0:
            continue

        # For each answer, grab its contained text and clean the string of whitespace and other such characters
        options = list(filter(lambda o: o != None, options))
        options = [clean_string(answer.get_text()) for answer in options]
        options = list(filter(lambda a: a != '', options)) # sometimes there are empty divs, remove them.
        options_s = ""
        for k, v in enumerate(options):
            options_s += f"{k + 1}. {v}\n"




        # Find the right answer block's text, then splice that string to get rid of the repeated text 'The correct answer is: '
        key_answer = q_block.find(class_='rightanswer')
        key_answer = key_answer.get_text()
        key_answer = key_answer[key_answer.find(':')+1:]
        key_answer = clean_string(key_answer)

        # Dict used to glue the data together
        mc_question = {
            'question': question,
            'options': options,
            'key': key_answer
        }

        mc_questions.append(mc_question)
    
    fp.close()
    return mc_questions

    

with open('quiz.csv', 'w', newline='') as file:
    for i in range(9):
        filepath = f"./quiz {i+1}_ Attempt review _ OCmoodle.htm"
        mc_questions = get_mc_questions(filepath)
        keys = mc_questions[0].keys()
        writer = csv.DictWriter(file, fieldnames=keys)
        if i == 0:
            writer.writeheader()
        writer.writerows(mc_questions)

