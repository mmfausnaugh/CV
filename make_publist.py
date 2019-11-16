import scipy as sp
from bs4 import BeautifulSoup
import re

def make_pub_string_aas(xml_record):
    title = xml_record.journal.text
    title = title.replace('#','\\#')
    author = xml_record.author.text
    last,first = author.split(',')
    num = xml_record.volume.text
    id_string = last + '_aas'+num
    date = xml_record.pubdate.text
    
    return id_string, ('\publication{{{},'
                       ' {}}}\\\\\n').format(title,date)


def make_pub_string_atel(xml_record):
    title = xml_record.journal.text
    author = xml_record.author.text
    last,first = author.split(',')
    num = xml_record.volume.text
    id_string = last + '_atel'+num
    date = xml_record.pubdate.text
    if '#' in title:
        title,_ = title.split('#')
        #remove the comma
        title = title[0:-2]        
    
    return id_string, ('\publication{{{},'
                       ' {}}}\\\\\n').format(title,date)
    
def make_pub_string(xml_record):
    """Has a few parts:

    ---Title
    ---First Author
    ---N authors
    ---journal: in the ref-xml format, this has the journal, volume,
       issue,article, page, and year.

    fill in the string template, and return

    """

    title = xml_record.title.text
    year = xml_record.pubdate.text.split()[-1]
    #split first and last name for reformating
    last_name, first_list = xml_record.author.text.split(',')
    id_string = last_name+year
    #adds the unbreakable space, and removes the comma at the end of the last_name
    author = '~'.join(first_list.split()) + "~" + last_name
    author = author.replace('ü','\\"u')
    N_author = len(xml_record.find_all('author'))

    journal_list = xml_record.journal.text.split(',')
    if len(journal_list) == 5:
        #this is ApJ/AAS journals
        journal, volume, issue, article_id, page = journal_list
    elif len(journal_list) == 4:
        #MNRAS
        journal, volume, issue,page = journal_list
        article_id = page
        
    elif len(journal_list) == 2 and 'Nature' in journal_list[0]:
        #Nature astronomy
        return id_string,'\publication{{"{}", {} et al. ({} authors, including M.~M.~Fausnaugh),'\
            '\\textit{{{}}}, page {} {}. }}\\\\\n'.format(title,
                                                          author,
                                                          N_author,
                                                          journal_list[0],
                                                          xml_record.page.text,
                                                          xml_record.pubdate.text)
    elif len(journal_list) == 3 and 'Nature' in journal_list[0]:
        #another version of nature astronomy with volume numbers
        if N_author >1:
            return id_string,'\publication{{"{}", {} et al. ({} authors, including M.~M.~Fausnaugh),'\
                ' \\textit{{{}}}, page {} {}. }}\\\\\n'.format(title,
                                                               author,
                                                               N_author,
                                                               journal_list[0],
                                                               xml_record.page.text,
                                                               xml_record.pubdate.text)
        else:
            return id_string,'\publication{{"{}", {},'\
                ' \\textit{{{}}}, page {} {}. }}\\\\\n'.format(title,
                                                               author,
                                                               journal_list[0],
                                                               xml_record.page.text,
                                                               xml_record.pubdate.text)


    elif len(journal_list) == 3:
        #frontiers, for now ?
        journal, volume, article_id = journal_list
    else:
        print(journal_list)

    journal = journal.replace('&amp;','\\&')
    search = re.search("(\d+)", volume)
    volume = search.group(1)
    search = re.search("(\w*\d+)", article_id)
    article_id = search.group(1)

    if int(N_author) == 1:
        return author + year,'\\noindent\publication{{"{}", {},'\
            ' \\textit{{{}}}, {}:{} ({}).  }}\\\\\n'.format(title,
                                                            author,
                                                            journal,
                                                            volume,
                                                            article_id,
                                                            year)
    elif 'Fausnaugh' in author:
        return id_string,'\\noindent\publication{{"{}", {} et al. ({} authors),'\
            ' \\textit{{{}}}, {}:{} ({}).  }}\\\\\n'.format(title,
                                                            author,
                                                            N_author,
                                                            journal,
                                                            volume,
                                                            article_id,
                                                            year)

    else:
        return id_string,'\\noindent\publication{{"{}", {} et al. ({} authors, including M.~M.~Fausnaugh),'\
            ' \\textit{{{}}}, {}:{} ({}).  }}\\\\\n'.format(title,
                                                            author,
                                                            N_author,
                                                            journal,
                                                            volume,
                                                            article_id,
                                                            year)
    

#projects for my pubs
first_author = ['Fausnaugh2018','M.~M.~Fausnaugh2017','Fausnaugh2017b','Fausnaugh2017','Fausnaugh2016','Fausnaugh2015']
major_author = ['Jayasinghe2019','De Rosa2018','Pei2017','Edelson2017','Vazquez2015'] #Jenkins2018 is ete6 research note
agn_storm = ['Dehghanian2019','Kriss2019','Mathur2017','Starkey2017','Goad2016','Edelson2015','De Rosa2015']
agn_misc = ['Landt2019','Goad2019','Edelson2019','McHardy2018','Grier2017','Cackett2015','Denney2014']
spitzer_microlensing = ['Wang2017','Chung2017','Zhu2017','Han2017','Shvartzvald2016','Han2016','Poleski2016',
                        'Bozza2016','Shvartzvald2015','Calchi Novati2015',]
tess_planets = ['Dumusque2019','Newton2019','Günther2019','Bouma2019','Vanderspek2019','Huang2018']
tess_differencing = ['Holoien2019','Vallely2019']
misc_observing =['Kennedy2017','Milisavljevic2013']
minor_pub = ['Fausnaugh2019',
             'Fausnaugh_aas233',
             'Jenkins2018',
             'Glidden_aas231',
             'Fausnaugh_aas231',
             'Guerrero_aas231',
             'Fausnaugh_atel9146',
             'Prieto_atel8356',
             'Wagner_atel8352',
             'Fausnaugh_atel6158',
             'Shappee_atel6143',
             'Prieto_atel3549',
             'Prieto_atel5110',
             'Prieto_atel5102',
             'Fausnaugh_aas229',
             'Fausnaugh_aas225']

headers = {'\\noindent\\underline{\\textbf{First Author}}\\\\\n':first_author,
           ('\\\\\\\\\\noindent\\underline{'
            '\\textbf{Major Author}}\\\\\n'
            '\\textbf{Contributed major analysis or reduced data}\\\\\n'):major_author,
           '\\\\\\\\\\noindent\\underline{\\textbf{Contributing Author}}\\\\\n':[],
           ('\\noindent\\textbf{'
            'TESS Exoplanets}\\\\\n'
            '\\textbf{Authorship acknowledges direct support of the TESS mission}\\\\\n'):tess_planets,
           ('\\noindent\\textbf{TESS:'
            ' Difference Imaging Pipeline}\\\\\n'
            '\\textbf{Contributed analysis}\\\\\n'):tess_differencing,
           ('\\noindent\\textbf{AGN STORM}\\\\\n'
            '\\textbf{Co-I status}\\\\\n'):agn_storm,
           ('\\noindent\\textbf{AGN Misc}\\\\\n'
            '\\textbf{Co-I status}\\\\\n'):agn_misc,
           ('\\noindent\\textbf{'
            'Spitzer Microlensing Campaign}\\\\\n'
            '\\textbf{Contributed observations}\\\\\n'):spitzer_microlensing,
           ('\\noindent\\textbf{Miscellaneous}\\\\\n'
            '\\textbf{Contributed observations}\\\\\n'):misc_observing,
           '\\\\\\\\\\noindent\\underline{\\textbf{Unrefereed Publications}}\\\\\n':minor_pub
           }
           
           


xml_string = open('export-refxml.xml','r').read()
soup = BeautifulSoup(xml_string)

pub_dict = {}
test_list = []
outstring = '\\begin{center}\\huge\\textbf{Publications}\\end{center}\n\n'
skips = 0
for pub in soup.find_all('record'):
    if 'arXiv' in pub.journal.text:
        skips +=1 
        continue
    if 'Quasars at all Cosmic Epochs' in pub.journal.text:
        skips +=1
        #a weird one off that resulted in the frontiers publication, anyway
        continue
    if 'Dissertations' in pub.journal.text:
        skips += 1
        continue
    if 'Telegram' in pub.journal.text:
        id_string,pub_string = make_pub_string_atel(pub)
    elif 'AAS Meeting' in pub.journal.text:
        id_string,pub_string = make_pub_string_aas(pub)
    else:
        id_string,pub_string = make_pub_string(pub)
    if id_string in pub_dict.keys():
        id_string = id_string + 'b'
    if id_string in pub_dict.keys():
        id_string = id_string[0:-1] + 'c'
    if id_string in pub_dict.keys():
        id_string = id_string[0:-1] + 'd'

        
    pub_dict[id_string] = pub_string
    test_list.append(pub_string)
    #outstring += pub_string


all_proj_keys = sp.r_[first_author,
                      major_author,
                      agn_storm,
                      agn_misc,
                      spitzer_microlensing,
                      tess_differencing,
                      tess_planets,
                      misc_observing,
                      minor_pub]
print('length of keys                           ',len(pub_dict))
print('length of list (check for clobbered pubs)',len(test_list))
print('length of projects                       ',len(all_proj_keys))
print('number skipped:                          ',skips)

print(pub_dict.keys())

for key in pub_dict.keys():
    if key not in all_proj_keys:
        print(key)

    
for key in headers.keys():
    outstring += key
    for pubkey in headers[key]:
        outstring += pub_dict[pubkey]
    


with open('publist_input2.tex','w') as fout:
    fout.write(outstring)
