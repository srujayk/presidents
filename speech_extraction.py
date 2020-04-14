from lxml import html
import requests
import re
from dateutil.parser import parse

speeches = [ ('Jan 22, 2020','https://www.presidency.ucsb.edu/documents/the-presidents-news-conference-davos-switzerland'),
('Nov 13, 2019','https://www.presidency.ucsb.edu/documents/the-presidents-news-conference-with-president-recep-tayyip-erdogan-turkey'),
('Oct 16, 2019','https://www.presidency.ucsb.edu/documents/the-presidents-news-conference-with-president-sergio-mattarella-italy'),
('Oct 02, 2019','https://www.presidency.ucsb.edu/documents/the-presidents-news-conference-with-president-sauli-niinisto-finland-0'),
('Sep 25, 2019','https://www.presidency.ucsb.edu/documents/the-presidents-news-conference-new-york-city-1'),
('Sep 20, 2019','https://www.presidency.ucsb.edu/documents/the-presidents-news-conference-with-prime-minister-scott-morrison-australia'),
('Aug 26, 2019','https://www.presidency.ucsb.edu/documents/the-presidents-news-conference-with-president-emmanuel-macron-france-biarritz-france'),
('Jun 30, 2019','https://www.presidency.ucsb.edu/documents/the-presidents-news-conference-with-president-moon-jae-south-korea-seoul-south-korea-0'),
('Jun 29, 2019','https://www.presidency.ucsb.edu/documents/the-presidents-news-conference-osaka-japan'),
('Jun 12, 2019','https://www.presidency.ucsb.edu/documents/the-presidents-news-conference-with-president-andrzej-duda-poland-0'),
('Jun 04, 2019','https://www.presidency.ucsb.edu/documents/the-presidents-news-conference-with-prime-minister-theresa-may-the-united-kingdom-london'),
('May 27, 2019','https://www.presidency.ucsb.edu/documents/the-presidents-news-conference-with-prime-minister-shinzo-abe-japan-tokyo-japan-1'),
('Mar 19, 2019','https://www.presidency.ucsb.edu/documents/the-presidents-news-conference-with-president-jair-messias-bolsonaro-brazil'),
('Feb 28, 2019','https://www.presidency.ucsb.edu/documents/the-presidents-news-conference-hanoi-vietnam'),
('Nov 07, 2018','https://www.presidency.ucsb.edu/documents/the-presidents-news-conference-washington-dc'),
('Sep 26, 2018','https://www.presidency.ucsb.edu/documents/the-presidents-news-conference-new-york-city-0'),
('Sep 18, 2018','https://www.presidency.ucsb.edu/documents/the-presidents-news-conference-with-president-andrzej-duda-poland'),
('Jul 30, 2018','https://www.presidency.ucsb.edu/documents/the-presidents-news-conference-with-prime-minister-giuseppe-conte-italy'),
('Jul 16, 2018','https://www.presidency.ucsb.edu/documents/the-presidents-news-conference-with-president-vladimir-vladimirovich-putin-russia-helsinki'),
('Jul 13, 2018','https://www.presidency.ucsb.edu/documents/the-presidents-news-conference-with-prime-minister-theresa-may-the-united-kingdom-0'),
('Jul 12, 2018','https://www.presidency.ucsb.edu/documents/the-presidents-news-conference-brussels-belgium'),
('Jun 12, 2018','https://www.presidency.ucsb.edu/documents/the-presidents-news-conference-sentosa-island-singapore'),
('Jun 09, 2018','https://www.presidency.ucsb.edu/documents/the-presidents-news-conference-charlevoix-canada'),
('Jun 07, 2018','https://www.presidency.ucsb.edu/documents/the-presidents-news-conference-with-prime-minister-shinzo-abe-japan-1'),
('Apr 30, 2018','https://www.presidency.ucsb.edu/documents/the-presidents-news-conference-with-president-muhammadu-buhari-nigeria'),
('Apr 27, 2018','https://www.presidency.ucsb.edu/documents/the-presidents-news-conference-with-chancellor-angela-merkel-germany-6'),
('Apr 24, 2018','https://www.presidency.ucsb.edu/documents/the-presidents-news-conference-with-president-emmanuel-macron-france'),
('Apr 18, 2018','https://www.presidency.ucsb.edu/documents/the-presidents-news-conference-with-prime-minister-shinzo-abe-japan-palm-beach-florida'),
('Apr 03, 2018','https://www.presidency.ucsb.edu/documents/the-presidents-news-conference-with-president-kersti-kaljulaid-estonia-president-raimonds'),
('Mar 06, 2018','https://www.presidency.ucsb.edu/documents/the-presidents-news-conference-with-prime-minister-stefan-lofven-sweden'),
('Feb 23, 2018','https://www.presidency.ucsb.edu/documents/the-presidents-news-conference-with-prime-minister-malcolm-b-turnbull-australia'),
('Jan 10, 2018','https://www.presidency.ucsb.edu/documents/the-presidents-news-conference-with-prime-minister-erna-solberg-norway'),
('Nov 12, 2017','https://www.presidency.ucsb.edu/documents/the-presidents-news-conference-with-president-tran-dai-quang-vietnam-hanoi-vietnam-0'),
('Nov 07, 2017','https://www.presidency.ucsb.edu/documents/the-presidents-news-conference-with-president-moon-jae-south-korea-seoul-south-korea'),
('Nov 06, 2017','https://www.presidency.ucsb.edu/documents/the-presidents-news-conference-with-prime-minister-shinzo-abe-japan-tokyo-japan-0'),
('Oct 17, 2017','https://www.presidency.ucsb.edu/documents/the-presidents-news-conference-with-prime-minister-alexios-tsipras-greece'),
('Oct 16, 2017','https://www.presidency.ucsb.edu/documents/the-presidents-news-conference-with-senate-majority-leader-mitchell-mcconnell'),
('Sep 26, 2017','https://www.presidency.ucsb.edu/documents/the-presidents-news-conference-with-prime-minister-mariano-rajoy-brey-spain'),
('Sep 07, 2017','https://www.presidency.ucsb.edu/documents/the-presidents-news-conference-with-amir-sabah-al-ahmad-al-jabir-al-sabah-kuwait'),
('Aug 28, 2017','https://www.presidency.ucsb.edu/documents/the-presidents-news-conference-with-president-sauli-niinisto-finland'),
('Jul 25, 2017','https://www.presidency.ucsb.edu/documents/the-presidents-news-conference-with-prime-minister-saad-al-hariri-lebanon'),
('Jul 13, 2017','https://www.presidency.ucsb.edu/documents/the-presidents-news-conference-with-president-emmanuel-macron-france-paris-france'),
('Jun 09, 2017','https://www.presidency.ucsb.edu/documents/the-presidents-news-conference-with-president-klaus-iohannis-romania'),
('May 18, 2017','https://www.presidency.ucsb.edu/documents/the-presidents-news-conference-with-president-juan-manuel-santos-calderon-colombia-0'),
('Apr 20, 2017','https://www.presidency.ucsb.edu/documents/the-presidents-news-conference-with-prime-minister-paolo-gentiloni-italy'),
('Apr 12, 2017','https://www.presidency.ucsb.edu/documents/the-presidents-news-conference-with-secretary-general-jens-stoltenberg-the-north-atlantic'),
('Apr 05, 2017','https://www.presidency.ucsb.edu/documents/the-presidents-news-conference-with-king-abdullah-ii-jordan-0'),
('Mar 17, 2017','https://www.presidency.ucsb.edu/documents/the-presidents-news-conference-with-chancellor-angela-merkel-germany-5'),
('Feb 16, 2017','https://www.presidency.ucsb.edu/documents/the-presidents-news-conference-1138'),
('Feb 15, 2017','https://www.presidency.ucsb.edu/documents/the-presidents-news-conference-with-prime-minister-benjamin-netanyahu-israel'), ('Feb 13, 2017','https://www.presidency.ucsb.edu/documents/the-presidents-news-conference-with-prime-minister-justin-pj-trudeau-canada'), ('Feb 10, 2017','https://www.presidency.ucsb.edu/documents/the-presidents-news-conference-with-prime-minister-shinzo-abe-japan'), ('Jan 27, 2017','https://www.presidency.ucsb.edu/documents/the-presidents-news-conference-with-prime-minister-theresa-may-the-united-kingdom')]

# page = requests.get('https://www.presidency.ucsb.edu/documents/presidential-documents-archive-guidebook/presidential-candidates-debates-1960-2016')
# tree = html.fromstring(page.content)
#
# debate_dates = tree.xpath('//table/tbody/tr/td[@class="xl70"]/span/span/span/span/span/span/text()')
# debate_links = tree.xpath('//table/tbody/tr/td[@class="xl77"]/span/span/span/span/span/span/a/@href')
# debate_names = tree.xpath('//table/tbody/tr/td[@class="xl77"]/span/span/span/span/span/span/a/text()')

for i in range(len(speeches)):
    page = requests.get(speeches[i][1])
    tree = html.fromstring(page.content)

    debate_paragraphs = [" ".join(string.text_content().split()) for string in tree.xpath('//*[@id="block-system-main"]/div/div/div[1]/div[3]')][0]

    speech_date = parse(speeches[i][0]).strftime("%m%d%y")

    speech_num = ""
    if i < 10:
        speech_num = "00" + str(i)
    else:
        speech_num = "0" + str(i)

    file_string = "speeches/" + "trump_speeches_" + speech_num + ".txt"

    with open(file_string, "w") as text_file:
        text_file.write(debate_paragraphs)

    print("finished ", speech_date, i)

    # print(len(split_paragraphs))
    # print(split_paragraphs[:30])
