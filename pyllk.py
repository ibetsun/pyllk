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
clearsp=False       #有清除精灵
gamelevel=0         #级别
gmissing=0          #关
#_quit=None         #退出标志
mainmenu=None       #主菜单
meswin=None         #游戏结束信息窗口
misswin=None        #过关信息窗口
psubft=None         #信息字体
psubfts=None
clicksnd=None       #选择的声音
lasersnd=None       #消除的声音
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
        self.td(gui.Label(u"主 菜 单",color=fg,font=fonts),align=0)
        
        self.tr()
        bv=gui.Label(u"开始游戏",color=fga,font=psubfts)
        bt1=gui.Button(bv,width=150,height=30)
        bt1.connect(gui.CLICK,self.EnterMenu,0)
        self.td(bt1,align=0,height=50)
        self.optiond=OptionDialog()
        self.optiond.connect(gui.CHANGE,self.onchange,self.optiond.value)
            
        self.tr()
        bv=gui.Label(u"游戏设置",color=fga,font=psubfts)
        bt2=gui.Button(bv,width=150,height=30)
        bt2.connect(gui.CLICK,self.EnterMenu,1)
        self.td(bt2, align=0,height=50)
        
        self.tr()
        bv=gui.Label(u"退出游戏",color=fga,font=psubfts)
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
        title = gui.Label(u"游戏设置",font=psubfts)
        self.dfstr=[u'普  通',u'高  级',u'专  家',u'大  师']
        self.value=gui.Form()
        tab=gui.Table()
        tab.tr()
        tab.td(gui.Spacer(width=8,height=16))
        tab.tr()
        tab.td(gui.Label(u"难  度:",font=psubfts), align=1,valign=1)
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
        tab.td(gui.Label(u"样  式:",font=psubfts),align=1)
        
        tt=gui.Table(width=200)
        tt.tr()
        tt.td(gui.Radio(g,value="style 1"),align=1)
        tt.td(gui.Image('data/s1.gif',width=36,height=36),align=-1)
        #tt.td(gui.Label(u"一",font=psubfts),align=-1)
        tt.td(gui.Radio(g,value="style 2"),align=1)
        tt.td(gui.Image('data/s2.gif',width=36,height=36),align=-1)
        tt.td(gui.Radio(g,value="style 3"),align=1)
        tt.td(gui.Image('data/s3.png',width=36,height=36),align=-1)
        tab.td(tt)
        
        tab.tr()
        tab.td(gui.Spacer(width=8,height=16))
        tab.tr()
        bv=gui.Label(u"确定",font=psubfts,color=fga)
        bt=gui.Button(bv)
        bt.connect(gui.CLICK, self.send, gui.CHANGE)
        tab.td(bt,width=120,align=1)
        bv=gui.Label(u"取消",font=psubfts,color=fga)
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
         title=gui.Label(u"暂停游戏",font=psubft,color=(255,255,0))
         
         space=title.style.font.size(" ")
         self.tr()
         self.td(title,width=width,align=0)
         self.tr()
         self.td(gui.Spacer(width=8,height=36))
         doc=gui.Document(width=width)
         doc.block(align=-1)
         for word in u"""按 F8 返回游戏!""".split(" "):
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
          for word in u"""按 ESC 取消或 空格 确定!""".split(" "):
             doc.add(gui.Label(word,font=psubfts,color=(255,255,0)))
             doc.space(space)
          self.tr()
          self.td(doc,align=0)   
            
def main():
   os.environ['SDL_VIDEO_CENTERED'] = '1'
   pygame.mixer.init()
   pygame.init()
   pygame.display.set_caption("连连看 powered by Python")
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
   qmeswin=MessageDialog(u"你要放弃此游戏返回主菜单吗?", psubft)
   misswin=MessageDialog(u"通过此关,进入下一关!",psubft)
   misswina=MessageDialog(u"恭喜你通关了!",psubft)
   global clicksnd,lasersnd
   clicksnd=load_sound('click.wav')
   clicksnd.set_volume(0.2)
   lasersnd=load_sound('laser.wav')
   lasersnd.set_volume(0.2)
   if pygame.mixer:
        menumusic = os.path.join('data', 'menu.wav')
        pygame.mixer.music.load(menumusic)
        pygame.mixer.music.set_volume(0.2)
        
   gameTime=0    #程序运行总时间
   playTime=0    #游戏中玩的时间
   tmpTime=0     #不在玩的时间
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
                   if mainmenu.selectedm==gameState.gameRun:          #弹出信息窗口
                         mainmenu.selectedm=gameState.gameMess
                         qmeswin.open()
                         pygame.mixer.music.pause()
                   elif mainmenu.selectedm==gameState.gameMess:     #退出信息窗口或退出游戏
                       if qmeswin in app.windows:
                            mainmenu.selectedm=gameState.gameRun
                            pygame.mixer.music.unpause()
                            qmeswin.close()
                       elif meswin in app.windows:
                            _quit=1
                       #elif misswin in app.windows:
                           
               elif evt.key == pygame.K_SPACE or evt.key == pygame.K_RETURN:   ##超时或生命没有了或放弃游戏信息窗口返回主菜单
                   if mainmenu.selectedm==gameState.gameMess:
                         mainmenu.selectedm=gameState.gameBegin
                         if qmeswin in app.windows:
                              qmeswin.close()
                         elif meswin in app.windows:
                              meswin.close()
                         c.add(mainmenu,(SW-166)/2, 200)               
                         gamecm.reinit()
                         pygame.mixer.music.load(menumusic)
                   elif mainmenu.selectedm==gameState.gameNextmiss:   #下一关
                         mainmenu.selectedm=gameState.gameRun
                         gamecm.update_heart(1)
                         #gamecm.update_misslv(1)
                         gamecm.update_score(2000)
                         gamemap.reset_map()
                         gamepm.set_map(gamemap.cellinfo)
                         playTime=0
                         pygame.mixer.music.unpause()
                         misswin.close() 
                   elif mainmenu.selectedm==gameState.gameWin:        #通关-返回主菜单
                         mainmenu.selectedm=gameState.gameBegin
                         misswina.close()
                         c.add(mainmenu,(SW-166)/2, 200)               
                         gamecm.reinit()
                         pygame.mixer.music.load(menumusic) 
               elif evt.key == pygame.K_F8:                        #弹出暂停窗口
                   if mainmenu.selectedm==gameState.gameRun:
                       mainmenu.selectedm=gameState.gamePause
                       pygame.mixer.music.pause()
                       pausewin.open()
                       #c.add(pausewin,(SW-500)/2, 200)
                   elif mainmenu.selectedm==gameState.gamePause:
                       mainmenu.selectedm=gameState.gameRun
                       pygame.mixer.music.unpause()
                       pausewin.close()
               elif evt.key == pygame.K_F4:                       #提示功能
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
            
       
       if mainmenu.selectedm!=gameState.gameRun:           #非游戏进行中
           app.paint(dc)
           tmpTime=gameTime
           playTime1=(gamecm.sptime-0)
           if mainmenu.selectedm==gameState.gameBegin:
               gamemap=None
               gamepm=None
               if not pygame.mixer.music.get_busy(): pygame.mixer.music.play(-1)
           elif mainmenu.selectedm==gameState.gameEnd:  
               _quit=1
           elif mainmenu.selectedm==gameState.gameOver:          #时间超时/无生命点弹出信息窗口
               mainmenu.selectedm=gameState.gameMess
               meswin.open()
           

       elif mainmenu.selectedm==gameState.gameRun:        #游戏进行中
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
               meswin=MessageDialog(u"时间到!返回主菜单或退出程序?",psubft)
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
            if spcount==0:  #消除完
                 gamecm.update_misslv(1)
                 if gamecm.misslv>9:      #通关
                     mainmenu.selectedm=gameState.gameWin
                     misswina.open()
                     pygame.mixer.music.stop()
                 else:                        #下一关
                     mainmenu.selectedm=gameState.gameNextmiss
                     misswin.open()
                     pygame.mixer.music.pause()
            else:
                 if not gamepm.search_path():   #没有可消除的
                     if gamecm.heart>0:
                         gamecm.update_heart(-1)
                         gamemap.refresh_map()
                     else:
                         mainmenu.selectedm=gameState.gameOver
                         meswin=MessageDialog(u"你的生命点数没有了!",psubft)
                         pygame.mixer.music.stop()
       
def update_Game():
        global clearsp
        clearsp=False
        mx,my=pygame.mouse.get_pos()
        px, py = gamemap.transPoint((mx,my))       #矩阵的行列
        if px>0:
                    gamemap.add_select(px, py)
                    pygame.event.set_grab(1)
                    gamepm.add_selected_cell((px,py))
                    clicksnd.play()
                    if gamepm.can_startlink():
                          tl,coor=gamepm.test_link()
                          if tl == True:
                                 clearsp=True
                                 gamecm.update_score(coor*100)        #得分=拐点*100
                                  
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
    gameBegin=1     #开始主菜单
    gameRun=2       #进行游戏
    gamePause=3     #暂停游戏
    gameEnd=4       #退出游戏
    gameNextmiss=5  #下一关
    gameOver=6      #结束游戏时间到
    gameWin=7       #通过游戏
    gameOption=8    #选项设置
    gameMess=9      #信息窗口
    
if __name__=="__main__": main()