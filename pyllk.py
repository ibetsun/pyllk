#encoding:gb18030
import pgu
import pygame
from Imap import *
from PathManager import *
from pygame.locals import * 
from pgu import gui
import sys
from encodings import gbk
SW,SH=880,660
gamemap=None
gamecm=None
gamepm=None
dc=None
clearsp=False       #���������
gamelevel=0         #����
gmissing=0          #��
#_quit=None         #�˳���־
mainmenu=None       #���˵�
meswin=None         #��Ϸ������Ϣ����
misswin=None        #������Ϣ����
psubft=None         #��Ϣ����
psubfts=None
clicksnd=None       #ѡ�������
lasersnd=None       #����������
backmisc=['102','103','101','104','105','106','107','108','109','110','111']
gamepath=os.path.split(os.path.abspath(sys.argv[0]))[0]
print(gamepath)
class MenuControl(gui.Table):
    def __init__(self,**params):
        gui.Table.__init__(self,**params)
        fg = (255,0,255)
        fga = (255,25,0)
        self.diflevel=0
        self.styleset=0
        self.selectedm=gameState.gameBegin
        fonts=pygame.font.Font('data/shaonv.ttf', 30)
        fonts.set_bold(True)
        self.tr()
        self.td(gui.Label(u"�� �� ��",color=fg,font=fonts),align=0)
        
        self.tr()
        bv=gui.Label(u"��ʼ��Ϸ",color=fga,font=psubfts)
        bt1=gui.Button(bv,width=150,height=30)
        bt1.connect(gui.CLICK,self.EnterMenu,0)
        self.td(bt1,align=0,height=50)
        self.optiond=OptionDialog()
        self.optiond.connect(gui.CHANGE,self.onchange,self.optiond.value)
            
        self.tr()
        bv=gui.Label(u"��Ϸ����",color=fga,font=psubfts)
        bt2=gui.Button(bv,width=150,height=30)
        bt2.connect(gui.CLICK,self.EnterMenu,1)
        self.td(bt2, align=0,height=50)
        
        self.tr()
        bv=gui.Label(u"�˳���Ϸ",color=fga,font=psubfts)
        bt3=gui.Button(bv,width=150,height=30)
        bt3.connect(gui.CLICK,self.EnterMenu,2)
        self.td(bt3, align=0,height=50)
        
    def onchange(self,value):
            _res=value.results()
            self.diflevel = int(_res['dif'])
            sttmp= _res['gstyle']
            self.styleset = int(sttmp[-1])-1
            self.optiond.close()
            self.selectedm=gameState.gameBegin
            #print self.diflevel,self.styleset

    def EnterMenu(self,i):
        if i==0: 
            self.selectedm=gameState.gameRun
            pygame.mixer.music.fadeout(500)
        elif i==1: 
            self.selectedm=gameState.gameOption
            gui.action_open({'container':self,'window':self.optiond})
        elif i==2: 
            self.selectedm=gameState.gameEnd
           
class OptionDialog(gui.Dialog): 
    def __init__(self,**params):
        fga = (255,25,0)
        title = gui.Label(u"��Ϸ����",font=psubfts)
        self.dfstr=[u'��  ͨ',u'��  ��',u'ר  ��',u'��  ʦ']
        self.value=gui.Form()
        tab=gui.Table()
        tab.tr()
        tab.td(gui.Spacer(width=8,height=16))
        tab.tr()
        tab.td(gui.Label(u"��  ��:",font=psubfts), align=1,valign=1)
        tt=gui.Table(width=200)
        sld=gui.HSlider(0,0,3,size=32,width=180,height=25,name='dif')
        dflb=gui.Label(self.dfstr[sld.value],width=180,font=psubfts,color=fga)
        sld.connect(gui.CHANGE, self.ajust,(sld,dflb))
        tt.tr()
        tt.td(dflb)
        tt.tr()
        tt.td(sld,align=0,width=240)
        tab.td(tt)
        
        tab.tr()
        tab.td(gui.Spacer(width=8,height=16))
       
        g = gui.Group(name='gstyle',value='style 1')
        tab.tr()
        tab.td(gui.Label(u"��  ʽ:",font=psubfts),align=1)
        
        tt=gui.Table(width=200)
        tt.tr()
        tt.td(gui.Radio(g,value="style 1"),align=1)
        tt.td(gui.Image('data/s1.gif',width=36,height=36),align=-1)
        #tt.td(gui.Label(u"һ",font=psubfts),align=-1)
        tt.td(gui.Radio(g,value="style 2"),align=1)
        tt.td(gui.Image('data/s2.gif',width=36,height=36),align=-1)
        tt.td(gui.Radio(g,value="style 3"),align=1)
        tt.td(gui.Image('data/s3.png',width=36,height=36),align=-1)
        tab.td(tt)
        
        tab.tr()
        tab.td(gui.Spacer(width=8,height=16))
        tab.tr()
        bv=gui.Label(u"ȷ��",font=psubfts,color=fga)
        bt=gui.Button(bv)
        bt.connect(gui.CLICK, self.send, gui.CHANGE)
        tab.td(bt,width=120,align=1)
        bv=gui.Label(u"ȡ��",font=psubfts,color=fga)
        bt=gui.Button(bv)
        bt.connect(gui.CLICK, self.close,None)
        tab.td(bt)
        tab.tr()
        tab.td(gui.Spacer(width=8,height=16))
        gui.Dialog.__init__(self, title, tab)
        
    def ajust(self,value):
        n,e=value
        e.value=self.dfstr[n.value]
        e.repaint()
        

class PauseDialog(gui.Table):
      def __init__(self,**params):
         gui.Table.__init__(self,**params)
         width=500
         fg=(25,255,200)
         #pft=pygame.font.Font('data/shaonv.ttf', 30)
         #psubft=pygame.font.Font('data/shaonv.ttf', 25)
         title=gui.Label(u"��ͣ��Ϸ",font=psubft,color=(255,255,0))
         
         space=title.style.font.size(" ")
         self.tr()
         self.td(title,width=width,align=0)
         self.tr()
         self.td(gui.Spacer(width=8,height=36))
         doc=gui.Document(width=width)
         doc.block(align=-1)
         for word in u"""�� F8 ������Ϸ!""".split(" "):
             doc.add(gui.Label(word,font=psubfts,color=fg))
             doc.space(space)
         #doc.br(space[1])
         self.tr()
         self.td(doc,align=0)
         

class MessageDialog(gui.Table): 
      def __init__(self,mess,ft,**params):
          gui.Table.__init__(self,**params)
          width=500
          fg=(25,255,200)
          #self.tr()
          #self.td(gui.Label(" Message ",font=ft,color=(255,255,0)),width=width,align=0)
          
          self.tr()
          self.td(gui.Label(mess,font=ft,color=fg),width=width,align=0)
          self.tr()
          self.td(gui.Spacer(width=8,height=36))
          space=ft.size(" ")
          doc=gui.Document(width=width)
          doc.block(align=-1)
          for word in u"""�� ESC ȡ���� �ո� ȷ��!""".split(" "):
             doc.add(gui.Label(word,font=psubfts,color=(255,255,0)))
             doc.space(space)
          self.tr()
          self.td(doc,align=0)   
            
def main():
   os.environ['SDL_VIDEO_CENTERED'] = '1'
   pygame.mixer.init()
   pygame.init()
   pygame.display.set_caption("������ powered by Python")
   global dc,psubft,psubfts
   dc = pygame.display.set_mode((SW, SH),pygame.DOUBLEBUF)
   appico=pygame.image.load('data/app.png').convert_alpha()
   pygame.display.set_icon(appico)
   psubft=pygame.font.Font('data/shaonv.ttf', 35)
   psubfts=pygame.font.Font('data/shaonv.ttf', 18)
   global gamecm,gamemap,gamepm
   gamecm = gameComm()
   #gamemap = Imap(dc,0,SW,SH)
   #mymap = gamemap.cellinfo
   #gamepm= PathManager(mymap)
   gamecm.set_background(color=(25,50,24))
   
   app=gui.App()
   c=gui.Container(width=SW,align=0,valign=-1)
   #print c.style.x
   global mainmenu,meswin,misswin
   mainmenu=MenuControl()
   #print mainmenu.rect
   c.add(mainmenu, (SW-166)/2, 200)
   app.init(c)
   #print mainmenu.rect
   global clearsp
   _quit = 0
   clock = pygame.time.Clock()
   pausewin=PauseDialog()
   
   #meswin.connect(gui.K_ESCAPE, quitGame,None)
   #meswin.connect(gui.K_SPACE, show_mainmenu,c)
   qmeswin=MessageDialog(u"��Ҫ��������Ϸ�������˵���?", psubft)
   misswin=MessageDialog(u"ͨ���˹�,������һ��!",psubft)
   misswina=MessageDialog(u"��ϲ��ͨ����!",psubft)
   global clicksnd,lasersnd
   clicksnd=load_sound('click.wav')
   clicksnd.set_volume(0.2)
   lasersnd=load_sound('laser.wav')
   lasersnd.set_volume(0.2)
   if pygame.mixer:
        menumusic = os.path.join('data', 'menu.wav')
        pygame.mixer.music.load(menumusic)
        pygame.mixer.music.set_volume(0.2)
        
   gameTime=0    #����������ʱ��
   playTime=0    #��Ϸ�����ʱ��
   tmpTime=0     #�������ʱ��
   playTime1=0
   sprizeTime=0
  
   miscid=0
   #pausewin.connect(gui.K_F7, pausewin.close())
   while not _quit:
       delta=clock.tick(30)
       
       gameTime=pygame.time.get_ticks()
       dc.blit(gamecm.backgd,(0,0))
       #pygame.draw.line(dc, (255,0,2), (SW/2,0), (SW/2,SH))       
       for evt in pygame.event.get():
            if evt.type == pygame.QUIT: _quit = 1
            if evt.type == pygame.KEYDOWN:
               if evt.key == pygame.K_ESCAPE: 
                   if mainmenu.selectedm==gameState.gameRun:          #������Ϣ����
                         mainmenu.selectedm=gameState.gameMess
                         qmeswin.open()
                         pygame.mixer.music.pause()
                   elif mainmenu.selectedm==gameState.gameMess:     #�˳���Ϣ���ڻ��˳���Ϸ
                       if qmeswin in app.windows:
                            mainmenu.selectedm=gameState.gameRun
                            pygame.mixer.music.unpause()
                            qmeswin.close()
                       elif meswin in app.windows:
                            _quit=1
                       #elif misswin in app.windows:
                           
               elif evt.key == pygame.K_SPACE or evt.key == pygame.K_RETURN:   ##��ʱ������û���˻������Ϸ��Ϣ���ڷ������˵�
                   if mainmenu.selectedm==gameState.gameMess:
                         mainmenu.selectedm=gameState.gameBegin
                         if qmeswin in app.windows:
                              qmeswin.close()
                         elif meswin in app.windows:
                              meswin.close()
                         c.add(mainmenu,(SW-166)/2, 200)               
                         gamecm.reinit()
                         pygame.mixer.music.load(menumusic)
                   elif mainmenu.selectedm==gameState.gameNextmiss:   #��һ��
                         mainmenu.selectedm=gameState.gameRun
                         gamecm.update_heart(1)
                         #gamecm.update_misslv(1)
                         gamecm.update_score(2000)
                         gamemap.reset_map()
                         gamepm.set_map(gamemap.cellinfo)
                         playTime=0
                         pygame.mixer.music.unpause()
                         misswin.close() 
                   elif mainmenu.selectedm==gameState.gameWin:        #ͨ��-�������˵�
                         mainmenu.selectedm=gameState.gameBegin
                         misswina.close()
                         c.add(mainmenu,(SW-166)/2, 200)               
                         gamecm.reinit()
                         pygame.mixer.music.load(menumusic) 
               elif evt.key == pygame.K_F8:                        #������ͣ����
                   if mainmenu.selectedm==gameState.gameRun:
                       mainmenu.selectedm=gameState.gamePause
                       pygame.mixer.music.pause()
                       pausewin.open()
                       #c.add(pausewin,(SW-500)/2, 200)
                   elif mainmenu.selectedm==gameState.gamePause:
                       mainmenu.selectedm=gameState.gameRun
                       pygame.mixer.music.unpause()
                       pausewin.close()
               elif evt.key == pygame.K_F4:                       #��ʾ����
                   if gamecm.hintcount>0:
                       if gamepm.search_path():
                          if gamepm.pot1!=gamepm.pot2 and gamepm.pot1!=(0,0):
                              gamecm.update_hint(-1)
                              gamemap.add_hint(gamepm.pot1)
                              gamemap.add_hint(gamepm.pot2)
                              
            if evt.type == pygame.MOUSEBUTTONDOWN and evt.button == 1:
                 if mainmenu.selectedm==gameState.gameRun:
                     update_Game()
            elif evt.type == pygame.MOUSEBUTTONUP:
                   pygame.event.set_grab(0)
                                           
            if mainmenu.selectedm!=gameState.gameRun: app.event(evt)
            
       
       if mainmenu.selectedm!=gameState.gameRun:           #����Ϸ������
           app.paint(dc)
           tmpTime=gameTime
           playTime1=(gamecm.sptime-0)
           if mainmenu.selectedm==gameState.gameBegin:
               gamemap=None
               gamepm=None
               if not pygame.mixer.music.get_busy(): pygame.mixer.music.play(-1)
           elif mainmenu.selectedm==gameState.gameEnd:  
               _quit=1
           elif mainmenu.selectedm==gameState.gameOver:          #ʱ�䳬ʱ/�������㵯����Ϣ����
               mainmenu.selectedm=gameState.gameMess
               meswin.open()
           

       elif mainmenu.selectedm==gameState.gameRun:        #��Ϸ������
           if mainmenu in c.widgets: c.remove(mainmenu)
           
           if not pygame.mixer.music.get_busy():
               pygame.mixer.music.load('data/'+backmisc[miscid]+'.mid')
               pygame.mixer.music.play()
               print (miscid)
               miscid=miscid+1 
           
           if gamemap is None:
               gamemap=Imap(dc, mainmenu.diflevel,mainmenu.styleset, SW, SH)
               gamecm.reinit()
               playTime=0
           if gamepm is None:
               gamepm=PathManager(gamemap.cellinfo)
           mx,my=pygame.mouse.get_pos()
           px, py = gamemap.transPoint((mx,my))
           if gameTime>tmpTime:
                #playTime=playTime1 + gameTime - tmpTime - sprizeTime
                playTime=playTime+clock.get_time()
                #print gtt,playTime
                if clearsp==True:
                    #sprizeTime=playTime<3000 and playTime or 3000
                    if playTime<3000: 
                        sprizeTime=playTime
                    else:
                        sprizeTime=3000
                    playTime = playTime-sprizeTime
                    #print sprizeTime
                    #playTime1=(playTime-3000)>0 and (playTime1-3000) or playTime1
           if not gamecm.set_spendTime(playTime): 
               mainmenu.selectedm=gameState.gameOver
               meswin=MessageDialog(u"ʱ�䵽!�������˵����˳�����?",psubft)
               pygame.mixer.music.stop()
           gamecm.show_gameinfo(dc)
           gamemap.draw_sprites()
           #if clearsp==True: 
           gamemap.draw_rect(px, py)
           gamemap.draw_hint(clock.get_time(), 300)   
           if clearsp==True: gamepm.draw_line(dc)    

       
       pygame.display.flip()     
       if clearsp==True:
            
            gamemap.remove_cell(gamepm.selected_cell[1])
            gamemap.remove_cell(gamepm.selected_cell[0])
            gamepm.clear_selected_cell()
            gamemap.clear_select()
            lasersnd.play()
            clearsp=False
            pygame.time.delay(150)
            gamemap.map_change(gamecm.misslv)
            spcount,sptemp=gamemap.get_spcount()
            #print spcount
            if spcount==0:  #������
                 gamecm.update_misslv(1)
                 if gamecm.misslv>9:      #ͨ��
                     mainmenu.selectedm=gameState.gameWin
                     misswina.open()
                     pygame.mixer.music.stop()
                 else:                        #��һ��
                     mainmenu.selectedm=gameState.gameNextmiss
                     misswin.open()
                     pygame.mixer.music.pause()
            else:
                 if not gamepm.search_path():   #û�п�������
                     if gamecm.heart>0:
                         gamecm.update_heart(-1)
                         gamemap.refresh_map()
                     else:
                         mainmenu.selectedm=gameState.gameOver
                         meswin=MessageDialog(u"�����������û����!",psubft)
                         pygame.mixer.music.stop()
       
def update_Game():
        global clearsp
        clearsp=False
        mx,my=pygame.mouse.get_pos()
        px, py = gamemap.transPoint((mx,my))       #���������
        if px>0:
                    gamemap.add_select(px, py)
                    pygame.event.set_grab(1)
                    gamepm.add_selected_cell((px,py))
                    clicksnd.play()
                    if gamepm.can_startlink():
                          tl,coor=gamepm.test_link()
                          if tl == True:
                                 clearsp=True
                                 gamecm.update_score(coor*100)        #�÷�=�յ�*100
                                  
                          else:
                                 if not gamepm.samelink:gamemap.remove_preselect()
                                 gamemap.remove_preselect()
       
def quitGame():
    _quit=1       
       
def show_mainmenu(contain):
    mainmenu.selectedm=gameState.gameBegin
    contain.add(mainmenu,(SW-200)/2, 200)

def load_sound(file):
    file = os.path.join('data', file)
    try:
        sound = pygame.mixer.Sound(file)
        return sound
    except pygame.error:
        print ('Warning, unable to load,', file)
       
class gameState:
    gameBegin=1     #��ʼ���˵�
    gameRun=2       #������Ϸ
    gamePause=3     #��ͣ��Ϸ
    gameEnd=4       #�˳���Ϸ
    gameNextmiss=5  #��һ��
    gameOver=6      #������Ϸʱ�䵽
    gameWin=7       #ͨ����Ϸ
    gameOption=8    #ѡ������
    gameMess=9      #��Ϣ����
    
if __name__=="__main__": main()