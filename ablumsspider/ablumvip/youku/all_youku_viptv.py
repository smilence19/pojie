#!/usr/bin/env python
#encoding=UTF-8
import re
import sys
import json
import os
import time
import copy
from spiderTool import spiderTool
from vipmediaContent import BASE_CONTENT
from vipmediaContent import PROGRAM_SUB
from bs4 import BeautifulSoup



class all_youku_viptv():
    def __init__(self):
        print "Do spider all_youku_viptv."
        self.program = copy.deepcopy(BASE_CONTENT["program"])
        self.program_sub = PROGRAM_SUB
        self.seedBase = [ "http://list.youku.com/category/show/c_97_pt_2_s_6_d_1_p_1.html"
                          , "http://list.youku.com/category/show/c_97_pt_2_s_6_d_1_p_1.html"
                          , "http://list.youku.com/category/show/c_97_pt_2_s_6_d_1_p_2.html"
                          , "http://list.youku.com/category/show/c_97_pt_2_s_6_d_1_p_3.html"
                          , "http://list.youku.com/category/show/c_97_pt_2_s_6_d_1_p_4.html"
                          , "http://list.youku.com/category/show/c_97_pt_2_s_6_d_1_p_5.html"
                       ]
        self.seedList = []
        self.dataDir = '.' + os.path.sep + 'data'
        self.today = time.strftime('%Y%m%d', time.localtime())
        self.seqNocnt = 1
        self.dataFile = spiderTool.openFile(self.dataDir + os.path.sep + "all_youku_viptv_" + self.today + ".txt")

    def __del__(self):
        if self.dataFile is not None:
            self.dataFile.close()

    def doProcess(self):
        for seed in self.seedBase:
            self.seedList = []
            seedList = []
            doc = spiderTool.getHtmlBody(seed)
            soup = BeautifulSoup(doc)
            seed_P = soup.find("div", attrs={"class": "box-series"})
            if seed_P is not None:
                seedList = seed_P.find_all("div", attrs={"class": "p-thumb"})
            for each in seedList:
                a_tag = each.find("a")
                if a_tag is not None:
                    subSeed = a_tag.get("href")
                    if subSeed is not None:
                        subSeed = "http:%s" % subSeed
                        self.seedList.append(subSeed)

            self.seedSpider()


    def seedSpider(self):
        for seed in self.seedList:
            self.program = copy.deepcopy(BASE_CONTENT["program"])
            self.program['pcUrl'] = seed
            self.program["ptype"] = "电视剧".decode("utf8")
            self.program['website'] = '优酷'.decode("utf8")
            self.program['getTime'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
            self.firstSpider(seed)
            self.program['totalSets'] = len(self.program['programSub'])
            # print self.program["name"],self.program['totalSets']

            if self.program['name'] == '' or self.program['name'] is None \
                    or self.program['mainId'] == ''or self.program['mainId'] is None \
                    or self.program['totalSets'] < 1:
                continue
            #add seqnum
            self.program['seqNo'] = self.seqNocnt
            self.seqNocnt = self.seqNocnt + 1

            json.dumps(PROGRAM_SUB)
            content = {'program': self.program}
            str = json.dumps(content)
            self.dataFile.write(str + '\n')



    def firstSpider(self, seed):
        point = 0.0
        poster = ""
        name = ""
        shootYear = ""
        alias = ""
        area = ""
        star = ""
        director = ""
        ctype = ""
        playTimes = 0
        intro = ""
        mainId = ""
        youkushootYear = ""

        doc = spiderTool.getHtmlBody(seed)
        soup = BeautifulSoup(doc)
        seed_v = re.search(r'http://v\.youku\.com/v_show/id_',seed)
        seed_Re = re.search(r'http://www\.youku\.com/show_page/id', seed)

        if seed_v:
            seed_P = soup.find('a', attrs={'class': 'desc-link'})
            if seed_P is not None:
                    seed = seed_P.get('href')
                    seed = "http:%s" % seed
                    doc = spiderTool.getHtmlBody(seed)
                    soup = BeautifulSoup(doc)
        elif not seed_Re:
            seed_P = soup.find('h1', attrs={'class': 'title'})
            if seed_P is not None:
                seed_aTag = seed_P.find('a')
                if seed_aTag is not None:
                    seed = seed_aTag.get('href')
                    seed = "http:%s" % seed
                    doc = spiderTool.getHtmlBody(seed)
                    soup = BeautifulSoup(doc)

        poster_p = soup.find("div", attrs={'class': 'p-thumb'})
        if poster_p is not None:
            poster = poster_p.find('img').get("src")

        p_base_content = soup.find('div',attrs={'class': 'p-base'})
        if p_base_content is not None:
            for li in p_base_content.find_all('li'):
                li_p = str(li)
                if li.find('span', attrs={'class': 'star-num'}) is not None:
                    point = li.find('span', attrs={'class': 'star-num'}).get_text()
                elif li.get('class') == ['p-row', 'p-title']:
                    name_p = re.findall(r'/a>：(.*)<span'.decode('utf8'), li_p.decode('utf8'))
                    if name_p:
                        name = name_p[0]
                    if re.search(r'<'.decode('utf8'), name):
                        name_p = re.findall(r'(.*)<span'.decode('utf8'), name)
                        if name_p:
                            name = name_p[0]
                elif li.get('class') == ['p-alias']:
                    alias_p = li.get('title')
                elif li.find('span', attrs={'class': 'pub'}) is not None :
                    shootYear_P = li.find('span', attrs={'class': 'pub'})
                    if re.search(r'优酷'.decode('utf8'), li_p.decode('utf8')):
                        youkushootYear_text = re.findall(r'/label>(.*)</span', str(shootYear_P))
                        if youkushootYear_text:
                            youkushootYear_text = youkushootYear_text[0]
                            youkushootYear = ''.join(youkushootYear_text.split('-')[0])
                    else:
                        shootYear_text = re.findall(r'/label>(.*)</span', str(shootYear_P))
                        if shootYear_text:
                            shootYear_text = shootYear_text[0]
                            shootYear = ''.join(shootYear_text.split('-')[0])
                elif re.search(r'<li>地区'.decode('utf8'), li_p.decode('utf8')):
                    area_p = li.get_text()
                    area_p = re.findall(r'地区：(.*)'.decode('utf8'), area_p)
                    if area_p:
                        area = area_p[0]
                        area = area.replace('/', ',')
                elif re.search(r'<li>类型'.decode('utf8'), li_p.decode('utf8')):
                    ctype_p = li.get_text()
                    ctype_p = re.findall(r'类型：(.*)'.decode('utf8'), ctype_p)
                    if ctype_p:
                        ctype = ctype_p[0]
                        ctype = ctype.replace('/', ',')
                elif re.search(r'<li>导演'.decode('utf8'), li_p.decode('utf8')):
                    director_p = li.get_text()
                    director_p = re.findall(r'导演：(.*)'.decode('utf8'), director_p)
                    if director_p:
                        director = director_p[0]
                elif li.get('class') == ['p-performer']:
                    star_list = []
                    for each in li.find_all('a'):
                        star_list.append(each.get_text())
                        star = ','.join(star_list)
                elif re.search(r'<li>总播放数'.decode('utf8'), li_p.decode('utf8')):
                    playTimesStr = li.get_text()
                    playTimesStr = re.findall(r'总播放数：(.*)'.decode('utf8'), playTimesStr)
                    if playTimesStr:
                        playTimesStr = playTimesStr[0]
                        playTimes_list = re.findall(r'(\d+)', playTimesStr)
                        playTimes = long(''.join(playTimes_list))
                elif li.get('class') == ['p-row', 'p-intro']:
                    intro = li.find('span').get_text().strip()
                else:
                    continue

            if shootYear == "":
                shootYear = youkushootYear

        if re.match(r'http://list\.youku\.com/show/id_(.+)\.html', seed):
            mainId = re.match(r'http://list\.youku\.com/show/id_(.+)\.html', seed).group(1)
        if re.match(r'http://v\.youku\.com/v_show/id_(.+)\.html', seed):
            mainId = re.match(r'http://v\.youku\.com/v_show/id_(.+)\.html', seed).group(1)

        self.program["name"] = spiderTool.changeName(name)
        self.program["alias"] = spiderTool.changeName(alias)
        self.program["point"] = float(point)
        self.program['poster'] = spiderTool.listStringToJson('url',poster)
        self.program['star'] = spiderTool.listStringToJson('name',star)
        self.program['director'] = spiderTool.listStringToJson('name',director)
        self.program['ctype'] = spiderTool.listStringToJson('name',ctype)
        self.program['shootYear'] = shootYear
        self.program['area'] = spiderTool.listStringToJson('name', area)
        self.program['playTimes'] = long(playTimes)
        self.program['intro'] = intro
        self.program['mainId'] = mainId

        showid = ""
        showid_url = ""
        p_list_p = soup.find_all('script', attrs={'type': 'text/javascript'})
        if p_list_p is not None:
            for each in p_list_p:
                if re.search(r'PageConfig', str(each)):
                    showid_p = re.findall(r'showid:"(.*)", videoId', str(each))
                    if showid_p:
                        showid = showid_p[0]
                        showid_url = "http://list.youku.com/show/module?id=%s&tab=showInfo&callback=jQuery111208239648697137207" % showid

        if showid_url != "":
            sub_doc = spiderTool.getHtmlBody(showid_url)
            if re.search(r'window\.jQuery', sub_doc):
                sub_doc_p = re.search(r'\((.*)\);', sub_doc)
                if sub_doc_p is not None:
                    sub_doc = sub_doc_p.group(1)
            try:
                data = json.loads(sub_doc)
            except:
                #print("load json error1111!")
                return
            if data.get('html') is None:
                #print("get html error1111")
                return

            sub_soup = BeautifulSoup(data['html'])
            reload_list_p = re.findall(r'id="reload_(\d+)"', data['html'])
            if reload_list_p:
                reload_list = list(set(reload_list_p))
                for reload in reload_list:
                    sub_seed = "http://list.youku.com/show/point?id=%s&stage=reload_%s&callback=jQuery111208239648697137207" % (mainId, reload)
                    #print(sub_seed)
                    self.secondSpider(sub_seed)

    def secondSpider(self, seed_sub):
        playseeduse = 0
        doc = spiderTool.getHtmlBody(seed_sub)
        if re.search(r'window\.jQuery', doc):
            sub_doc_p = re.search(r'\((.*)\);', doc)
            doc = sub_doc_p.group(1)
        try:
            data = json.loads(doc)
        except:
            #print("load json error22222!")
            return
        if data.get('html') is None:
            #print("get html error22222")
            return

        sub_soup = BeautifulSoup(data['html'])
        for div in sub_soup.find_all('div', attrs={'class': 'p-item'}):
            self.program_sub = copy.deepcopy(PROGRAM_SUB)
            setNumber = ""
            setName = ""
            webUrl = ""
            poster = ""
            playLength = ""
            setIntro = ""
            plot = []

            webUrl_p = div.find('a')
            if webUrl_p is not None:
                webUrl = "http:%s" % webUrl_p.get('href')
            setName_p = div.find('a')
            if setName_p is not None:
                setName = setName_p.get('title')
            setNumber_p = div.find('a')
            if setNumber_p is not None:
                setNumber = setNumber_p.get('title')
            setIntro_p = div.find('div', attrs={'class': 'item-intro c999'})
            if setIntro_p is not None:
                setIntro = setIntro_p.get_text()
            poster_p = div.find('img')
            if poster_p is not None:
                poster = poster_p.get('src')
            playLength_p = div.find('span', attrs={'class': 'p-time'})
            if playLength_p is not None:
                playLength = playLength_p.get_text()


            if re.search(r'\d+$'.decode('utf8'), setNumber):
                setNumber = re.search(r'\d+$'.decode('utf8'), setNumber).group(0)
            else:
                setNumber = ""

            if setNumber == "" and setName != "" and setName is not None:
                if re.search(r'\d+'.decode('utf8'), setName):
                    setNumber = re.search(r'\d+'.decode('utf8'), setName).group(0)
            if setNumber == "" or setName == "" or setNumber is None or setName is None or webUrl is None or webUrl == "" or \
                    re.search(r'预告'.decode('utf8'), setName):
                continue
            self.program_sub['setNumber'] = setNumber
            self.program_sub['setName'] = setName
            self.program_sub['webUrl'] = webUrl
            self.program_sub['poster'] = poster
            self.program_sub['playLength'] = playLength
            self.program_sub['setIntro'] = setIntro
            self.program_sub['plot'] = plot
            self.program['programSub'].append(self.program_sub)



if __name__ == '__main__':
    app = all_youku_viptv()
    if len(sys.argv) > 1:
        app.seedList = spiderTool.readSeedList(sys.argv[1])
        app.seedSpider()
    else:
        app.doProcess()
