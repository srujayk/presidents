from lxml import html
import requests
import re
from dateutil.parser import parse

def build_regex_string(speakers):

    fin_string = '('

    for speaker in speakers:
        speaker_temp = speaker.replace("(", "").replace(")", "").replace("|", "").replace(" ", "").replace("[", "").replace("?", "").replace("*", "")
        fin_string += speaker_temp
        fin_string += '|'

    fin_string = fin_string[:-1]
    fin_string += ')'

    return fin_string

page = requests.get('https://www.presidency.ucsb.edu/documents/presidential-documents-archive-guidebook/presidential-candidates-debates-1960-2016')
tree = html.fromstring(page.content)

debate_dates = tree.xpath('//table/tbody/tr/td[@class="xl70"]/span/span/span/span/span/span/text()')
debate_links = tree.xpath('//table/tbody/tr/td[@class="xl77"]/span/span/span/span/span/span/a/@href')
debate_names = tree.xpath('//table/tbody/tr/td[@class="xl77"]/span/span/span/span/span/span/a/text()')

for i in range(len(debate_links)):
    page = requests.get(debate_links[i])
    tree = html.fromstring(page.content)

    debate_speakers = list(set(tree.xpath('//*[@id="block-system-main"]/div/div/div[1]/div[3]/p/strong/text()')))

    if len(debate_speakers) == 0:
        debate_speakers = list(set(tree.xpath('//*[@id="block-system-main"]/div/div/div[1]/div[3]/p/b/text()')))

    if len(debate_speakers) == 0:
        debate_speakers = list(set(tree.xpath('//*[@id="block-system-main"]/div/div/div[1]/div[3]/p/i/text()')))

    if len(debate_speakers) == 0:
        debate_speakers = list(set(tree.xpath('//*[@id="block-system-main"]/div/div/div[1]/div[3]/p/em/text()')))

    if len(debate_speakers) == 0:
        temp_speakers = list(set(tree.xpath('//*[@id="block-system-main"]/div/div/div[1]/div[3]/p/text()')))
        #print(temp_speakers)
        debate_speakers = []

        for speaker in temp_speakers:
            comma = speaker.find(':')
            if comma < 20 and comma > -1:
                debate_speakers.append(speaker[:comma])

        debate_speakers = list(set(debate_speakers))

    if len(debate_speakers) < 3:
        temp_speakers = list(set(tree.xpath('//*[@id="block-system-main"]/div/div/div[1]/div[3]/p/text()')))
        #print(temp_speakers)
        debate_speakers = []

        for speaker in temp_speakers:
            comma = speaker.find('.')
            if comma < 15 and comma > -1:
                debate_speakers.append(speaker[:comma])

        debate_speakers = list(set(debate_speakers))

    debate_paragraphs = [" ".join(string.text_content().split()) for string in tree.xpath('//*[@id="block-system-main"]/div/div/div[1]/div[3]')][0]

    #print(list(set(debate_speakers)))
    # print(debate_paragraphs[:1000])
    #print(debate_dates[i], debate_speakers)
    regex_string = build_regex_string(debate_speakers)
    print(regex_string)
    splitter = re.compile(regex_string)

    speakers_text = {}

    for speaker in debate_speakers:
        speakers_text[speaker] = ""

    speakers_text['NOBODY:'] = ""

    debate_paragraphs_split = splitter.split(debate_paragraphs)

    curr_speaker = 'NOBODY:'

    for paragraph in debate_paragraphs_split:
        if paragraph == '' or paragraph == ' ' or paragraph == ' ':
            continue
        elif paragraph in debate_speakers:
            curr_speaker = paragraph
        else:
            speakers_text[curr_speaker] += " "
            speakers_text[curr_speaker] += paragraph

    speech_date = parse(debate_dates[i]).strftime("%m%d%y")

    for speaker in debate_speakers:
        speaker_name = speaker
        if speaker_name not in ['PARTICIPANTS:', 'MODERATOR:', 'MODERATORS:', 'QUESTION:', 'PANELISTS:', 'PANELIST:', 'AUDIENCE MEMBER:', '', ' ']:
            file_string = "data/" + speaker_name.replace("/", "").replace("'", "").replace('"', "").replace(":", "") + "_" + speech_date + ".txt"

            with open(file_string, "w") as text_file:
                text_file.write(speakers_text[speaker_name])

    print("finished ", speech_date, i)

    # print(len(split_paragraphs))
    # print(split_paragraphs[:30])
