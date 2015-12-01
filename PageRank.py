# unicoding:utf-8

#url='http://baike.baidu.com/subview/203868/11094487.htm'5
#url='http://baike.baidu.com/subview/2211222/9371450.htm'
#url='http://baike.baidu.com/subview/9329/5277596.htm'50
#url='http://baike.baidu.com/subview/8755770/11103476.htm'20
#url='http://baike.baidu.com/subview/90660/11206729.htm'200
#url='http://baike.baidu.com/view/61891.htm'500
    
import urllib
import re
import networkx as nx
import time
import math
import matplotlib.pyplot as plt
import matplotlib
import xmlrpclib
from pylab import *

G=nx.DiGraph()

local_webpages_dir = "html/"
#local_webpages_dir = "html_xns/"
#local_webpages_dir = "html_jobs/"

server_url = 'http://127.0.0.1:20738/RPC2'
server = xmlrpclib.Server(server_url)
G1 = server.ubigraph;
G1.clear()


def mainfuction(url):
    list1=[]
    prepare_list=[]
    
    temp=str(url).split('com')
    father_short_url=temp[1]
    
    base_name=findname(father_short_url)
    print 'Your Search Word: ' + base_name
    
    father_dict=childurl(getinfor(getHtml(url)))
    father_dict[0]=father_short_url
    #print father_dict
    print 'Total link:' + str(len(father_dict))
    
    G1.new_vertex_w_id(0)
    G1.set_vertex_attribute(0,"shape","sphere")
    G1.set_vertex_attribute(0,"size","2")
    G1.set_vertex_attribute(0,"color","#DC143C")
 
    #Save the First Page
    getHtml_save(father_short_url,father_dict)
    
    #Algorithm Mode
    #PageRank
    Activity = search(father_dict)  
    a = pagerank(G)
    list1 = drawRelation(a, father_dict, base_name, 8)
    drawGraph(list1,'PageRank')
    list2 = drawRelationFor3D(a, father_dict, base_name, 8)
    Draw3D_ball(list2)
    G1.clear()
    G.clear()
    
    #Linked PR
    G1.new_vertex_w_id(0)
    G1.set_vertex_attribute(0,"shape","sphere")
    G1.set_vertex_attribute(0,"size","2")
    G1.set_vertex_attribute(0,"color","#DC143C")
    
    Activity = search_link(father_dict)
    a = pagerank(G)
    list1 = drawRelation(a, father_dict, base_name, 8)
    
    drawGraph(list1,'PageRank_Link')
    list2 = drawRelationFor3D(a, father_dict, base_name, 8)
    Draw3D_ball(list2)
    G1.clear()
    G.clear()
    
    #Date PR
    
    G1.new_vertex_w_id(0)
    G1.set_vertex_attribute(0,"shape","sphere")
    G1.set_vertex_attribute(0,"size","2")
    G1.set_vertex_attribute(0,"color","#DC143C")
    
    Activity = search_link(father_dict)
    a = pagerank_Date(G, Activity)
    list1 = drawRelation(a, father_dict, base_name, 8)
    
    drawGraph(list1,'PageRank_Date')
    list2 = drawRelationFor3D(a, father_dict, base_name, 8)
    Draw3D_ball(list2)
    G1.clear()
    G.clear()
    
    #PageRank + TFIDF
    G1.new_vertex_w_id(0)
    G1.set_vertex_attribute(0,"shape","sphere")
    G1.set_vertex_attribute(0,"size","2")
    G1.set_vertex_attribute(0,"color","#DC143C")

    info=search_TF(father_dict,father_short_url)
    pagerank_part = pagerank(G)
    a = TFIDF(pagerank_part, info)
    #Draw picture
    list1 = drawRelation(a, father_dict, base_name, 8)
    drawGraph(list1,'PR+TFIDF')
    list2 = drawRelationFor3D(a, father_dict, base_name, 8)
    Draw3D_ball(list2)
    G1.clear()
    G.clear()
  
    #PageRank+Hits+TFIDF
    G1.new_vertex_w_id(0)
    G1.set_vertex_attribute(0,"shape","sphere")
    G1.set_vertex_attribute(0,"size","2")
    G1.set_vertex_attribute(0,"color","#DC143C")

    info=search_TF(father_dict,father_short_url)
    pagerank_part = pagerank(G)
    
    a = TFIDF(pagerank_part, info)    
    prepare_list = drawRelationForHits(a, father_dict, base_name, 8)
    a = hyberlink_induced_topic_search(a, prepare_list,G)
    #Draw picture
    list1 = drawRelation(a, father_dict, base_name, 8)
    drawGraph(list1,'PR+HITS+TFIDF')
    list2 = drawRelationFor3D(a, father_dict, base_name, 8)
    Draw3D_ball(list2)
    G.clear()
    
    print 'Finished'

def getHtml(url):
    page=urllib.urlopen(url)
    html=page.read()
    page.close()
    return html

def getHtml_save(short_url,father_dict):
    url = 'http://baike.baidu.com' + short_url
    for i in father_dict:
        if father_dict[i] == short_url:
            index = i
            break
    name = local_webpages_dir + str(index) +'.html'
   
    try:
        f = open(name, 'r')
    except IOError, e:
        urllib.urlretrieve(url, name)
        f = open(name, 'r')
    
    html = f.read()
    f.close()
    return html

def getinfor(html):
    reg='<a target=_blank href="(.*?)">.*?</a>'
    inforList=re.compile(reg).findall(html)
    return inforList

def childurl(inforList):
    domain=[]
    t=1
    for information in inforList:
        domain.append(information)
    domain2=[]
    this_dict={}
    for i in domain:
        if not i in domain2:
            domain2.append(i)
            this_dict[t]=i
            t=t+1
    return this_dict

def findname(url):
    name=""
    realurl='http://baike.baidu.com'+url
    reg='<title>(.*?)_.*?</title>'
    nameList=re.compile(reg).findall(getHtml(realurl))
    for namelist in nameList:
        name=namelist
    return name

def findname_dict(url, dict):
    name=""
    reg='<title>(.*?)_.*?</title>'
    nameList=re.compile(reg).findall(getHtml_save(url, dict))
    for namelist in nameList:
        name=namelist
    return name

def search(dict2):
    list=[]    
    link=[]
    dict={}
    length=len(dict2)
        
    for i in range(0,length):
        list.append(str(i))
        G1.new_vertex_w_id(i+1)
        G1.set_vertex_attribute(i+1,"shape","sphere")
        G1.new_edge(0,i+1)
    print list
    G.add_nodes_from(list)
    #print G.nodes()
    
    hasrelation=[0 for j in range(1,length)]
    for i in range(1, length):
        link.append(dict2[i])
        
    i=0
    j=0
    for k in range(1, length):
        i=1
        j_html = getHtml_save(dict2[k], dict2)
        dict = childurl(getinfor(j_html))
        print len(dict)
        for klink in link:
            for kchild in dict.keys():
                if (str(klink) in str(dict[kchild]) or str(dict[kchild]) in str(klink)):
                    hasrelation[j] = getRankValue(j_html)
                    G.add_edge(str(j+1),str(i))
                    G1.new_edge(j+1,i+1)
                    break;
            #print i
            i=i+1
        print "j: "+str(j)
        j=j+1
        dict.clear()      
    return hasrelation

def search_link(dict2):
    list=[]
    name=[]
    htmlList=[]
    length=len(dict2)

    for i in range(0,length):
        list.append(str(i))
        G1.new_vertex_w_id(i+1)
        G1.set_vertex_attribute(i+1,"shape","sphere")
        G1.new_edge(0,i+1)
    print list
    G.add_nodes_from(list)
    
    hasrelation=[0 for j in range(1,length)]
    
    for i in range(1, length):
        name.append(findname_dict(dict2[i], dict2))

    for k in range(1, length):
        html=getHtml_save(dict2[k], dict2)
        hasrelation[k-1]=getRankValue(html)
        htmlList.append(html)
        
    i=1
    print "HTML list:" + str(len(htmlList))
    for nam in name:
        j=1
        for htm in htmlList:
            if nam in htm:
                G.add_edge(str(i),str(j))
                G1.new_edge(i,j)
            j=j+1
        print "Name i Finished: "+str(i)
        i=i+1
    return hasrelation

def search_TF(dict2,url):
    list=[]
    name=[]
    htmlList=[]
    length=len(dict2)
    
    for i in range(0,length):
        list.append(str(i))
        G1.new_vertex_w_id(i+1)
        G1.set_vertex_attribute(i+1,"shape","sphere")
        G1.new_edge(0,i+1)
    print list
    G.add_nodes_from(list)
    
    finalrelation=[[0 for i in range(2)] for j in range(1,length)]
    hasrelation=[[0 for j in range(1,length)] for i in range(1,length)]   

    for k in range(1, length):
        html=getHtml_save(dict2[k], dict2)
        htmlList.append(html)
        
        name1=""
        reg='<title>(.*?)_.*?</title>'
        nameList=re.compile(reg).findall(html)
        for namelist in nameList:
            name1=namelist
        name.append(name1)

    #print "HTML list :"+ str(len(htmlList))
    i=0
    for nam in name:
        j=0
        temp=0
        for htm in htmlList:
            if nam in htm:
                hasrelation[i][j]=htm.count(nam)
                G.add_edge(str(i+1),str(j+1))  
                G1.new_edge(i+1,j+1)          
            if i is j:
                hasrelation[i][j]=0
            temp=temp+hasrelation[i][j]
            j=j+1
        finalrelation[i][1]=temp
        print "i: "+str(i+1)
        i=i+1
    
    parenthtml=getHtml_save(url,dict2)
    t=0
    for na in name:
        if na in parenthtml:
            finalrelation[t][0]=parenthtml.count(na)
        t=t+1
    return finalrelation

def pagerank(graph):
    print "Begin PageRank_Original"
    
    factor=0.85 
    max_iter=100
    min_delta=0.00001
    
    nodes = graph.nodes()  
    for i in range(len(nodes)):
        if nodes[i] == str(0):
            del nodes[i]
            break
    print nodes
    
    graph_size = len(nodes)
    if graph_size == 0:
        return {}

    min_value = (1.0-factor)/graph_size 
    pagerank = dict.fromkeys(nodes, 1.0)
    
    for i in range(max_iter):
        diff = 0
        for node in nodes:
            rank = min_value
            for referring_page in nodes:
                if (graph.has_edge(referring_page, node)) and (referring_page is not node):
                    rank += factor * pagerank[referring_page]/len(graph.neighbors(referring_page))
                
            diff += abs(pagerank[node] - rank)
            pagerank[node] = rank
            
        print 'NO.%s ' % (i+1)
        print pagerank
        print ''

        if diff < min_delta:
            break
            
    return pagerank

def pagerank_Date(graph, activity):
    print "Begin PageRank_Factor Modified"

    max_iter=100
    min_delta=0.00001

    nodes = graph.nodes()
    del nodes[0]
    graph_size = len(nodes)
    for i in range(len(nodes)):
        if nodes[i] == str(0):
            del nodes[i]
            break
    print nodes
    
    pagerank = dict.fromkeys(nodes, 1.0)
    
    for i in range(max_iter):
        diff=0 
        for node in nodes:
            factor = activity[int(node)-1]
            rank = (1.0-factor)/graph_size
            for referring_page in nodes:
                if (graph.has_edge(referring_page, node)) and (referring_page is not node):
                    rank += factor * pagerank[referring_page]/len(graph.neighbors(referring_page))

            diff += abs(pagerank[node] - rank)
            pagerank[node] = rank

        print 'NO.%s ' % (i+1)
        print pagerank
        print ''

        if diff < min_delta:
            break
    return pagerank

def h_yberlink_induced_topic_search(pagerank, nodes, graph):
    print "Begin Hyberlink_induced_topic_search"
    max_iter=100
    min_delta=0.00001
    
    graph_size = len(nodes)
    if graph_size == 0:
        return {}
    
    hub={}
    auth={}
    tempauth={}
    temphub={}
    
    for node in nodes:
        hub[str(node)]=1
        auth[str(node)]=1
        tempauth[str(node)]=1
        temphub[str(node)]=1
            
    for i in range(max_iter):
        diffauth=0.0
        diffhub=0.0
        norm = 0.0

        for node in nodes:
            auth[str(node)]=0
            tempauth[str(node)]=0
            for referring_page in nodes:
                if graph.has_edge(referring_page, node):
                    tempauth[str(node)] += hub[str(referring_page)]
            #if tempauth[str(node)] < min_delta:
                #tempauth[str(node)]=2.0
            norm += tempauth[str(node)]**2
        if norm < min_delta:
            norm=2.0
        norm=sqrt(norm)
        
        for node in nodes:                
            tempauth[str(node)]=tempauth[str(node)]/norm
            diffauth=abs(tempauth[str(node)]-auth[str(node)])
            auth[str(node)]=tempauth[str(node)]
    
        norm = 0.0
        for node in nodes:
            hub[str(node)]=0
            temphub[str(node)]=0
            for referring_page in graph.neighbors(str(node)):
                if referring_page in nodes:
                    temphub[str(node)]+=auth[str(referring_page)]
            
            #if temphub[str(node)] < min_delta:
                #temphub[str(node)]=2.0
            norm+=temphub[str(node)]**2
        if norm < min_delta:
            norm=2.0
        norm=sqrt(norm)
        
        for node in nodes:    
            temphub[str(node)]=temphub[str(node)]/norm
            diffhub=abs(temphub[str(node)]-hub[str(node)])
            hub[str(node)]=temphub[str(node)]
            
        print 'NO.%s iteration' % (i+1)
        print auth
        print ''
        print 'Diff' + str(diffhub+diffauth)
        
        if (diffhub + diffauth) < min_delta:
            break    
        
    for node in auth :
        auth[str(node)] += pagerank[str(node)]
        
    return auth

def hyberlink_induced_topic_search(pagerank, nodes, graph):
    print "Begin Hyberlink Induced Topic Search(HITS)"
    max_iter=100
    min_delta=0.00001
    
    graph_size = len(nodes)
    if graph_size == 0:
        return {}
    
    hub={}
    auth={}
    
    for node in nodes:
        hub[str(node)]=1
        auth[str(node)]=1
            
    for i in range(max_iter):
        norm = 0.0

        for node in nodes:
            auth[str(node)]=0
            for referring_page in nodes:
                if graph.has_edge(referring_page, node):
                    auth[str(node)] += hub[str(referring_page)]
            
            norm += auth[str(node)]**2
        #if norm < min_delta:
            #norm=2.0
        norm=sqrt(norm)
        
        for node in nodes:                
            auth[str(node)]=auth[str(node)]/norm
    
        norm = 0.0
        for node in nodes:
            hub[str(node)]=0
            for referring_page in graph.neighbors(str(node)):
                if referring_page in nodes:
                    hub[str(node)]+=auth[str(referring_page)]

            norm+=hub[str(node)]**2
        #if norm < min_delta:
            #norm=2.0
        norm=sqrt(norm)
        
        for node in nodes:    
            hub[str(node)]=hub[str(node)]/norm
            
        print 'NO.%s ' % (i+1)
        print auth
        print ''    
        
    for node in auth :
        if node in pagerank:
            auth[str(node)] += pagerank[str(node)]
            
    print "Hyberlink Induced Topic Search(HITS) Finished"   
    print auth
    return auth

def prepareHits(baselist, graph):
    print 'Begin Add extended Nodes for Hits.'
    extend_list=baselist
    
    nodes = graph.nodes()
    for i in range(len(nodes)):
        if nodes[i] == str(0):
            del nodes[i]
            break
    
    for node in nodes:
        if (not node in extend_list):
            for basenode in baselist:
                if(graph.has_edge(basenode, node) or graph.has_edge(node, basenode)):
                    extend_list.append(node)
                    print 'Add one ' + str(node)
                    break
    
    print 'Extended Nodes for Hits finished.'
    print extend_list
    return extend_list

def getRankValue(html):
    temptime=time.strftime('%Y-%m-%d',time.localtime(time.time()))
    nowtime=temptime.split("-")
    
    reg='<span id="viewPV"></span>.*?</div><div class="side-list-item">(.*?)<a href=.*?>'
    timelist=re.compile(reg).findall(html)
    if(len(timelist) == 0):
        return 0.85
    tempcount=str(timelist[0])
    modifycount=int(filter(str.isdigit,tempcount))
    
    reg='<span id="lastModifyTime">(.*?)</span>'
    lastlist=re.compile(reg).findall(html)
    if(len(lastlist) == 0):
        return 0.85
    temptime=str(lastlist[0])
    lastmodify=temptime.split("-")
    modifynum=modifycount
    modifytime=lastmodify
    
    minusyear=int(nowtime[0])-int(modifytime[0])
    minusmonth=int(nowtime[1])-int(modifytime[1])
    minusday=int(nowtime[2])-int(modifytime[2])
    d=modifynum*0.005+100*minusyear+10*minusmonth+1*minusday
    
    if int(d) < 10:
        return 0.95
    return 0.85

def TFIDF(pagerank,info):
    print 'Begin TFIDF'
    FatherPageTotal = 0
    OtherPageTotal = 0
    for i in pagerank:
        FatherPageTotal += info[int(i)-1][0]
        OtherPageTotal += info[int(i)-1][1]

    #print FatherPageTotal
    #print OtherPageTotal
    
    for i in pagerank:
        tf = info[int(i)-1][0]/FatherPageTotal
        idf = math.log10(OtherPageTotal /(1+info[int(i)-1][1]))   
        pagerank[i] += tf*idf
    print 'Finish TFIDF'
    print pagerank    
    return pagerank
    
def drawRelation(d, dict, basename, basenum): 
    print "Begin Sort to Select the Top"
    list=[]
    items= d.items()
    backitems=[[v[1],v[0]] for v in items] 
    backitems.sort(reverse=True) 
    list = [value for key, value in backitems]
    print list

    #Add the nodes we want
    list1=[]
    list1.append(str(basename))
    
    #Choose the TOP
    i=0
    j=0
    while (i < basenum):        
            s = str(findname_dict(dict[int(list[j])],dict))
            j=j+1
            #s_code = s.encode('gb2312')
            if (not s in list1) and (s is not basename):
                list1.append(s)    
                i = i+1
                #print i
    print "Select Finished"
    for item in list1:
        print str(item)
    return list1

def drawRelationForHits(d, dict, basename, basenum): 
    print "Begin Sort for Hits to get Core Nodes."
    list=[]
    items= d.items()
    backitems=[[v[1],v[0]] for v in items] 
    backitems.sort(reverse=True) 
    list = [value for key, value in backitems]
    #print list
   
    #Add the nodes we want
    list1=[]
    
    #Choose the TOP
    i=0
    j=0
    while (i < basenum):        
            s = str(findname_dict(dict[int(list[j])],dict))
            #s_code = s.encode('gb2312')
            if not s in list1:
                if s != basename:
                    list1.append(list[j])    
                    i = i+1                 
            j=j+1
    print 'Sort for Hits Finished'
    print list1
    return prepareHits(list1,G)     

def drawRelationFor3D(d, dict, basename, basenum): 
    print "Begin Sort for 3D Graph"
    list=[]
    items= d.items()
    backitems=[[v[1],v[0]] for v in items] 
    backitems.sort(reverse=True) 
    list = [value for key, value in backitems]
    #print list

    #Add the nodes we want
    list1=[]
    list1.append(0)
    
    #Choose the TOP 8
    i=0
    j=0
    while (i < basenum):        
            s = str(findname_dict(dict[int(list[j])],dict))
            
            if not s in list1:
                if s != basename:
                    list1.append(int(list[j]))   
                    i = i+1
                    #print i
                    
            j=j+1
    print 'Sort for 3D Graph Finished'    
    print list1    
    return list1 

def drawGraph(list,name):
    G=nx.star_graph(len(list)-1) #graph model generator
    pos=nx.spring_layout(G) # positions for all nodes
    
    #set graph radius
    radius = 200
    #initial points
    pos[0][0] = 0
    pos[0][1] = 0
    pos[1][0] = radius
    pos[1][1] = 0
    pos[2][0] = radius/(math.sqrt(2))
    pos[2][1] = radius/(math.sqrt(2))
    pos[3][0] = 0
    pos[3][1] = radius
    pos[4][0] = -radius/(math.sqrt(2))
    pos[4][1] = radius/(math.sqrt(2))
    pos[5][0] = -radius
    pos[5][1] = 0
    pos[6][0] = -radius/(math.sqrt(2))
    pos[6][1] = -radius/(math.sqrt(2))
    pos[7][0] = 0
    pos[7][1] = -radius
    pos[8][0] = radius/(math.sqrt(2))
    pos[8][1] = -radius/(math.sqrt(2))
    
    #set the point by weight
    for j in range(1, len(pos)):
        temp_x = pos[j][0]
        temp_weight = 5*j*j    #weight algorithm
        if (temp_x > 0) and (pos[j][1] == 0):
            pos[j][0] = pos[j][0] + temp_weight                
        if (temp_x > 0) and (pos[j][1] > 0):
            pos[j][0] = pos[j][0] + temp_weight
            pos[j][1] = pos[j][1]*(1 + temp_weight/temp_x)    
        if (temp_x == 0) and (pos[j][1] > 0):
            pos[j][1] = pos[j][1] + temp_weight
        if (temp_x < 0) and (pos[j][1] > 0):
            pos[j][0] = pos[j][0] - temp_weight
            pos[j][1] = pos[j][1]*(1 - temp_weight/temp_x)    
        if (temp_x < 0) and (pos[j][1] == 0):
            pos[j][0] = pos[j][0] - temp_weight                
        if (temp_x < 0) and (pos[j][1] < 0):
            pos[j][0] = pos[j][0] - temp_weight
            pos[j][1] = pos[j][1]*(1 - temp_weight/temp_x)    
        if (temp_x == 0) and (pos[j][1] < 0):
            pos[j][1] = pos[j][1] - temp_weight
        if (temp_x > 0) and (pos[j][1] < 0):
            pos[j][0] = pos[j][0] + temp_weight
            pos[j][1] = pos[j][1]*(1 + temp_weight/temp_x)
    
    # set nodes
    size = 3000
    #red
    nx.draw_networkx_nodes(G,pos,
                           nodelist=[0],
                           node_color='#FF0000',
                           node_size=4500,
                             alpha=0.9
                             )
    #Crimson
    nx.draw_networkx_nodes(G,pos,
                           nodelist=[1],
                           node_color='#1E90FF',
                           node_size=size,
                              alpha=0.8
                              )
    #OrangeRed
    nx.draw_networkx_nodes(G,pos,
                           nodelist=[2],
                           node_color='#EEC900',
                           node_size=size,
                             alpha=0.8
                             )
    #DarkOrange
    nx.draw_networkx_nodes(G,pos,
                           nodelist=[3],
                           node_color='#48D1CC',
                           node_size=size,
                             alpha=0.8
                             )
    #Gold
    nx.draw_networkx_nodes(G,pos,
                           nodelist=[4],
                           node_color='#FFD700',
                           node_size=size,
                             alpha=0.8
                             )
    #GreenYellow
    nx.draw_networkx_nodes(G,pos,
                           nodelist=[5],
                           node_color='#ADFF2F',
                           node_size=size,
                             alpha=0.8
                             )
    #LightGreen
    nx.draw_networkx_nodes(G,pos,
                           nodelist=[6],
                           node_color='#90EE90',
                           node_size=size,
                             alpha=0.8
                             )
    #SkyBlue
    nx.draw_networkx_nodes(G,pos,
                           nodelist=[7],
                           node_color='#87CEEB',
                           node_size=size,
                              alpha=0.8
                              )
    #DarkOrchid
    nx.draw_networkx_nodes(G,pos,
                           nodelist=[8],
                           node_color='#9932CC',
                           node_size=size,
                              alpha=0.8
                              )
    
    
    # set name of labels 
    labels={}
    for k in range(0, len(list)):
        labels[k]= unicode(list[k])
        
    #set labels
    nx.draw_networkx_labels(G,pos,labels,font_size=14)
    
    #draw edges
    nx.draw_networkx_edges(G,pos,width=1.0,alpha=0.3)
    
    plt.axis('off')  #No coordinate axis
    plt.savefig(name + ".png") # save as png
    plt.close()
    #plt.show() # display


def Draw3D_ball(list):
    nodes = G.nodes()
    if(len(list)==9):
        G1.set_vertex_attribute(list[0],"color","#DC143C")
        G1.set_vertex_attribute(list[1],"color","#1E90FF")
        G1.set_vertex_attribute(list[2],"color","#EEC900")
        G1.set_vertex_attribute(list[3],"color","#48D1CC")
        G1.set_vertex_attribute(list[4],"color","#FFD700")
        G1.set_vertex_attribute(list[5],"color","#ADFF2F")
        G1.set_vertex_attribute(list[6],"color","#90EE90")
        G1.set_vertex_attribute(list[7],"color","#87CEEB")
        G1.set_vertex_attribute(list[8],"color","#9932CC")

    if(len(list)==8):
        G1.set_vertex_attribute(list[0],"color","#DC143C")
        G1.set_vertex_attribute(list[1],"color","#1E90FF")
        G1.set_vertex_attribute(list[2],"color","#EEC900")
        G1.set_vertex_attribute(list[3],"color","#48D1CC")
        G1.set_vertex_attribute(list[4],"color","#FFD700")
        G1.set_vertex_attribute(list[5],"color","#ADFF2F")
        G1.set_vertex_attribute(list[6],"color","#90EE90")
        G1.set_vertex_attribute(list[7],"color","#87CEEB")
        
    if(len(list)==7):
        G1.set_vertex_attribute(list[0],"color","#DC143C")
        G1.set_vertex_attribute(list[1],"color","#1E90FF")
        G1.set_vertex_attribute(list[2],"color","#EEC900")
        G1.set_vertex_attribute(list[3],"color","#48D1CC")
        G1.set_vertex_attribute(list[4],"color","#FFD700")
        G1.set_vertex_attribute(list[5],"color","#ADFF2F")
        G1.set_vertex_attribute(list[6],"color","#90EE90")    
        
    if(len(list)==6):
        G1.set_vertex_attribute(list[0],"color","#DC143C")
        G1.set_vertex_attribute(list[1],"color","#1E90FF")
        G1.set_vertex_attribute(list[2],"color","#EEC900")
        G1.set_vertex_attribute(list[3],"color","#48D1CC")
        G1.set_vertex_attribute(list[4],"color","#FFD700")
        G1.set_vertex_attribute(list[5],"color","#ADFF2F")    
    
    if(len(list)==5):
        G1.set_vertex_attribute(list[0],"color","#DC143C")
        G1.set_vertex_attribute(list[1],"color","#1E90FF")
        G1.set_vertex_attribute(list[2],"color","#EEC900")
        G1.set_vertex_attribute(list[3],"color","#48D1CC")
        G1.set_vertex_attribute(list[4],"color","#FFD700")
    
    if(len(list)==4):
        G1.set_vertex_attribute(list[0],"color","#DC143C")
        G1.set_vertex_attribute(list[1],"color","#1E90FF")
        G1.set_vertex_attribute(list[2],"color","#EEC900")
        G1.set_vertex_attribute(list[3],"color","#48D1CC")
        
    if(len(list)==3):
        G1.set_vertex_attribute(list[0],"color","#DC143C")
        G1.set_vertex_attribute(list[1],"color","#1E90FF")
        G1.set_vertex_attribute(list[2],"color","#EEC900")
        
    if(len(list)==2):
        G1.set_vertex_attribute(list[0],"color","#DC143C")
        G1.set_vertex_attribute(list[1],"color","#1E90FF")    
        
    if(len(list)==1):
        G1.set_vertex_attribute(list[0],"color","#DC143C")    
    
    
    delete = 1
    for flag in range(0,len(nodes)):
        for li in list:
            if (flag == li):
                delete = 0
        if(delete == 1):                
            G1.remove_vertex(flag)
        delete = 1

def find_url_byname(name):
    s_utf=name.decode(sys.stdin.encoding).encode("GBK")
    test=urllib.quote(s_utf)
    url='http://baike.baidu.com/list-php/dispose/searchword.php?word='+test+'&pic=1'
    webpage=urllib.urlopen(url)
    a=webpage.read().decode('utf-8')
    reg='meta http-equiv=.*? content=.*?><meta http-equiv=.*? content=\'0;URL=(.*?)\'>'
    namelist=re.compile(reg).findall(a)
    url='http://baike.baidu.com'+str(namelist[0])
    return url

def multymeaning(realname):
    #url=find_url_byname(realname)
    tempname=realname.split('_')
    if len(tempname) is 2:
        father=tempname[0]
        number=tempname[1]
        return multymeaning_2(str(father),int(number))
    else:
        return multymeaning_1(realname)

def multymeaning_1(realname):
    url=find_url_byname(realname)
    if 'notexist' in url:
        return u"您输入的词条不存在！"
    
    html=getHtml(url)
    if 'createpolysemyitem?' in html:
        reg='<a target=_blank href="(.*?)">(.*?)</a></p>'
        meaninglist=re.compile(reg).findall(html)
        meaningname={}
        meaningurl={}
        q=1
        for i in meaninglist:
            meaningname[q]=i[1]
            meaningurl[q]=i[0]
            q=q+1
        #inform user multymeaning error and show meaning in a blank
        returnstr=u'您输入的是个多义词，您可能想要找:\n'
        for i in meaningname.keys():
            returnstr=returnstr+str(i)+": "+meaningname[i]+"\n"
        returnstr=returnstr+u"您可以按照下面的方式搜索:\n"+realname+"_"+str(1)+" is "+meaningname[1]
        #show information in UI returnstr
        return returnstr
    else:    
        mainfuction(url)
        return 'Not the ambivalent word. Begin analyze the word.'        

def multymeaning_2(realname,number):
        #Get the ambivalent page.
        url=find_url_byname(realname)
        html=getHtml(url)
        
        #Choose one meaning of the word
        reg='<a target=_blank href="(.*?)">(.*?)</a></p>'
        meaninglist=re.compile(reg).findall(html)
        meaningname={}
        meaningurl={}
        q=1
        for i in meaninglist:
                meaningname[q]=i[1]
                meaningurl[q]=i[0]
                q=q+1
        realurl='http://baike.baidu.com'+str(meaningurl[number])
        mainfuction(realurl)
        return realurl