#encoding:gb18030
import random,pygame
from PathManager import cellObject
from pygame import locals
class Imap:
    
    GL_ROWS = [8, 8, 9, 10]
    GL_COLS = [14, 15, 16, 18]
    BGSTYLES = 'data/button.png'
    SPRITESTYLES = ['data/st1.png','data/st2.png','data/st3.png']
    BGREC = pygame.Rect(0,65, 54, 59)
    CELLWD = 50
    CELLHT = 55
    SPSIZE = 48
    def __init__(self,dc,lv,st,wd,ht):
        self.glevel = lv   #游戏级别 难易
        self.glpics = [int(self.GL_ROWS[i]*self.GL_COLS[i]/4) for i in range(4)]
        print(self.glpics)
        self.offsetX = (wd - self.CELLWD*self.GL_COLS[lv])/2
        self.offsetY = (ht - self.CELLHT*self.GL_ROWS[lv])/2
        self.spcount=0
        self.graph = dc
        self.cellinfo = []
        self.spstyle = st    #精灵样式默认为第一个
        self.selcell=[]
        #self.selidy=None
        self.load_img()
        self.init_map()
        self.hintcell=[]
        self.dela=0

    def init_map(self):
        srows = self.GL_ROWS[self.glevel]
        scols = self.GL_COLS[self.glevel]
        self.arrs=[i+1 for i in range(self.glpics[self.glevel])]*4
        #print arrs
        random.shuffle(self.arrs)        #  随机打乱列表
        multilist = [[((col-1)*self.CELLWD+self.offsetX, (row-1)*self.CELLHT+self.offsetY) for col in range(scols+2)] for row in range(srows+2)]
        
        #print multilist
        for i in range(srows+2):
            cellsp=[]
            for j in range(scols+2):
                pos = multilist[i][j]
                #print pos
                if i==0 or j==0 or i==srows+1 or j==scols+1:
                    cellsp.append(cellObject(pos, i, j, 0))
                    #self.cellinfo.append(cellObject(pos, i, j, 0))
                else:
                    cellsp.append(cellObject(pos, i, j, self.arrs[(i-1)*scols+j-1]))
                    #self.cellinfo.append(cellObject(pos, i, j, self.arrs[(i-1)*scols+j-1]))
            self.cellinfo.append(cellsp)
            #print cellsp
        
        #print random.randint(0,4)
        radof= random.choice([0,1,2,3])
        print (radof)
        #self.BGREC = self.BGREC.move(radof*54, 0)
        self.BGREC.left=radof*54
        print (self.BGREC)
    def set_spstyle(self,st):
        """设置精灵样式"""
        self.spstyle=st
        self.load_img()
    def load_img(self):
        self.bgsprite = pygame.image.load(self.BGSTYLES).convert_alpha()   #背景精灵
        self.spimg = pygame.image.load(self.SPRITESTYLES[self.spstyle]).convert_alpha()    # 所有精灵的图
            
    def get_spcount(self):
          cout=0
          temp=[]
          for r in self.cellinfo:
              for c in r:
                  if c.picid>0:
                      temp.append(c.picid)
                      cout +=1
          return cout,temp
    
    def refresh_map(self):
        """ 洗牌 """
        spcout,sptemp=self.get_spcount()
        if spcout<=0 : return 
        random.shuffle(sptemp)
        cc=0
        for r in self.cellinfo:
              for c in r:
                 if c.picid>0: 
                     c.picid=sptemp[cc]
                     cc +=1
                     
    def remove_cell(self,cell):
        self.cellinfo[cell[0]][cell[1]].picid=0
        if cell in self.hintcell:self.hintcell=[]
    def transPoint(self,mp):
       """ 鼠标坐标转换为矩阵的索引：鼠标处于哪个单元格内        """
       xx, yy = mp[0]-self.offsetX, mp[1]-self.offsetY
       srows = self.GL_ROWS[self.glevel]
       scols = self.GL_COLS[self.glevel]
       rr = (xx % self.CELLWD!=0 and xx > 0) and (xx/self.CELLWD+1) or (xx/self.CELLWD)
       cc = (yy % self.CELLHT!=0 and yy > 0) and (yy/self.CELLHT+1) or (yy/self.CELLHT)
#        print (cc,rr,xx,yy)
       if (rr>0 and rr<scols+1) and (cc>0 and cc<srows+1):
             return int(cc), int(rr)
       else:
             return -10,-10
         
    def get_cellinfo(self,idx,idy):
        return self.cellinfo[idx][idy].pos
    
    def draw_selecte(self,pos):
        """ 画出点击选择的精灵，背景不一样 """   
        
        #self.bgsprite.set_colorkey((240,20,150))
        #print pos
        bgre = (54*4,65, 54, 59)
        self.graph.blit(self.bgsprite,pos,bgre)
    
    def add_select(self,idx,idy):
        self.selcell.append((idx,idy))
        if len(self.selcell)>2: self.selcell.pop(0)
        #posst=self.cellinfo[idx][idy].pos
        #self.draw_selecte(posst)
        #self.selidx=idx-1
        #self.selidy=idy
     
    def remove_preselect(self):
        self.selcell.pop(0)
    
    def clear_select(self):
        self.selcell=[]
               
    def draw_sprites(self):
        """ 画出所有的精灵 """
        
        srows = self.GL_ROWS[self.glevel]
        scols = self.GL_COLS[self.glevel]
        for rr in self.cellinfo:
            for cc in rr:
                if cc.picid>0:
                    reca = (int(cc.picid/23)*self.SPSIZE, (cc.picid%23)*self.SPSIZE, self.SPSIZE, self.SPSIZE)
                    if len(self.selcell)>0 and (cc.ind_x,cc.ind_y) in self.selcell:
                        self.draw_selecte(cc.pos)
                    else:
                        self.graph.blit(self.bgsprite,cc.pos,self.BGREC)
                    self.graph.blit(self.spimg,cc.pos,reca)
                     
                    
    def draw_rect(self,px,py):
        
        if px>0 and py>0 and self.cellinfo[px][py].picid>0:
            pygame.draw.rect(self.graph, (255, 0, 0), ((self.cellinfo[px][py].pos), (self.CELLWD, self.CELLHT)), 1)
           
    def add_hint(self,pot):
        """添加提示的精灵"""
        self.hintcell.append(pot)
        if len(self.hintcell)>2:self.hintcell=self.hintcell[-1:]
        #self.hintstp=stp
    def flash_hide(self,gametime,stp):
        """提示框闪烁时判断隐藏"""    
        self.dela=self.dela+gametime
        if self.dela<stp:return True
        if self.dela>=stp*2: self.dela=0
        return False     
    def draw_hint(self,gt,stp):
        """绘制提示框"""
        if len(self.hintcell)>0:
            if self.flash_hide(gt, stp)==False:
                for pot in self.hintcell:
                      px,py=pot
                      pygame.draw.rect(self.graph, (255,128,0), ((self.cellinfo[px][py].pos), (self.CELLWD, self.CELLHT)), 3)

            
    def reset_map(self):
        """ 过关到下一个关口   """
        self.arrs=[]
        self.cellinfo=[]
        self.selcell=[]
        self.init_map()
        
    def map_change(self,ml):
        dr=self.GL_ROWS[self.glevel]
        lc=self.GL_COLS[self.glevel]
        ofy=lc/2+dr/2-dr
        if ml==1:
            self._move_down(1, dr, 1, lc)
        elif ml==2:       #上左下右
            self._move_left(1, dr/2, 1, lc)
            self._move_right(dr/2+1, dr,1, lc) 
        elif ml==3:       #左分离右集中
            self._move_down(dr/2+1, dr, 1, lc/2)
            self._move_up(1,dr/2,1,lc/2)
            self._move_down(1,dr/2,lc/2+1,lc)        
            self._move_up(dr/2+1,dr,lc/2+1,lc)
        elif ml==4:       #上分离下集中
            self._move_left(1, dr/2, 1, lc/2)
            self._move_right(1, dr/2, lc/2+1, lc)
            self._move_left(dr/2+1, dr, lc/2+1, lc)
            self._move_right(dr/2+1, dr, 1, lc/2)  
        elif ml==5:       #东南-西北
            self._move_Rdown(2, 1, ofy, lc)
            self._move_Lup(2, 1, 1, lc-ofy-1)
        elif ml==6:       #西南-东北
            self._move_Ldown(2,1, 1, lc-ofy)
            self._move_Rup(2, 1, ofy+2, lc)
        elif ml==7:       #向左
            self._move_left(1, dr, 1, lc)
        elif ml==8:       #向外
            self._move_left(1, dr, 1, lc/2)     
            self._move_right(1, dr, lc/2+1, lc)
            self._move_up(1, dr/2, 1, lc)
            self._move_down(dr/2+1, dr, 1, lc)
        elif ml==9:       #向内
            self._move_left(1, dr, lc/2+1, lc)     
            self._move_right(1, dr, 1, lc/2)
            self._move_up(dr/2+1, dr, 1, lc)
            self._move_down(1, dr, 1, lc)
            
       
    def _move_down(self,stx,enx,sty,eny):
        
        while sty<=eny:
            movepic=[]
            for k in range(stx,enx+1):     #从上向下收集
                if self.cellinfo[k][sty].picid>0:
                    movepic.append(self.cellinfo[k][sty].picid)
            
            if len(movepic)==enx-stx+1:
                sty=sty+1
                continue
            k=enx             #从底部向上放
            while len(movepic) !=0:
                self.cellinfo[k][sty].picid=movepic.pop()
                k=k-1
            while k>=stx:
                self.cellinfo[k][sty].picid=0
                k=k-1
            sty=sty+1 
      
    def _move_up(self,stx,enx,sty,eny): 
        
        while sty<=eny:
            movepic=[]
            for k in range(stx,enx+1):                      #从上向下收集
               if self.cellinfo[k][sty].picid>0:
                    movepic.append(self.cellinfo[k][sty].picid)
            if len(movepic)==enx-stx+1:
                sty=sty+1
                continue
            k=stx
            while len(movepic) !=0:
                self.cellinfo[k][sty].picid=movepic.pop(0)     #弹出第一个
                k=k+1
                
            while k<=enx:
                self.cellinfo[k][sty].picid=0
                k=k+1 
            
            sty=sty+1
        
    def _move_left(self,stx,enx,sty,eny):    
        k=0
        while stx<=enx:
             movepic=[]
             for k in range(sty,eny+1):
                 if self.cellinfo[stx][k].picid>0:
                    movepic.append(self.cellinfo[stx][k].picid)
             if len(movepic)==eny-sty+1:
                stx=stx+1
                continue
             k=sty
             while len(movepic) !=0:
                self.cellinfo[stx][k].picid=movepic.pop(0)     #弹出第一个
                k=k+1
             while k<=eny:
                self.cellinfo[stx][k].picid=0 
                k=k+1 
             
             stx=stx+1
             
    def _move_right(self,stx,enx,sty,eny):
        k=0
        while stx<=enx:
             movepic=[]
             for k in range(sty,eny+1):
                 if self.cellinfo[stx][k].picid>0:
                    movepic.append(self.cellinfo[stx][k].picid)
             if len(movepic)==eny-sty+1:
                stx=stx+1
                continue
             k=eny
             while len(movepic) !=0:
                self.cellinfo[stx][k].picid=movepic.pop()     #弹出最后
                k=k-1
             while k>=sty:
                self.cellinfo[stx][k].picid=0 
                k=k-1 
             
             stx=stx+1
        
    def _move_Rdown(self,stx,enx,sty,eny):  
        while stx<=enx:
            movepic=[]
            k,m=stx,1;
            while k<=enx and m<=self.GL_COLS[self.glevel]:
                if self.cellinfo[k][m].picid>0:
                    movepic.append(self.cellinfo[k][m].picid)   
                k,m=k+1,m+1
                
            k,m=k-1,m-1
            while len(movepic) >0:
                self.cellinfo[k][m].picid=movepic.pop()
                k,m=k-1,m-1
            while k>=stx and m>=1:
                self.cellinfo[k][m].picid=0
                k,m=k-1,m-1
            stx=stx+1
            
        while sty<=eny:
            movepic=[]
            k,m=sty,1
            while k<=eny and m<=self.GL_ROWS[self.glevel]:
                if self.cellinfo[m][k].picid>0:
                    movepic.append(self.cellinfo[m][k].picid)
                m,k=m+1,k+1
            k,m=k-1,m-1
            while len(movepic) >0:
                self.cellinfo[m][k].picid=movepic.pop()
                k,m=k-1,m-1
            while k>=sty and m>=1:     
                self.cellinfo[m][k].picid=0
                k,m=k-1,m-1
            sty=sty+1  
            
    def _move_Ldown(self,stx,enx,sty,eny):           
         while stx<=enx:
            movepic=[]
            k,m=stx,self.GL_COLS[self.glevel]
            while k<=enx and m>=1:
                if self.cellinfo[k][m].picid>0:
                    movepic.append(self.cellinfo[k][m].picid)   
                k,m=k+1,m-1
                
            k,m=k-1,m+1
            while len(movepic) >0:
                self.cellinfo[k][m].picid=movepic.pop()
                k,m=k-1,m+1
            while k>=stx and m<=self.GL_COLS[self.glevel]:
                self.cellinfo[k][m].picid=0
                k,m=k-1,m+1
            stx=stx+1
            
         while eny>=sty:
            movepic=[]
            k,m=eny,1
            while k>=sty and m<=self.GL_ROWS[self.glevel]:
                if self.cellinfo[m][k].picid>0:
                    movepic.append(self.cellinfo[m][k].picid)
                m,k=m+1,k-1
            k,m=k+1,m-1
            while len(movepic) >0:
                self.cellinfo[m][k].picid=movepic.pop(0)
                k,m=k+1,m-1
            while k<=eny and m>=1:     
                self.cellinfo[m][k].picid=0
                k,m=k+1,m-1
            eny=eny-1 
            
    def _move_Rup(self,stx,enx,sty,eny):        
          while enx>=stx:
              movepic=[]      
              k,m=enx,1
              while k>=stx and m<=self.GL_COLS[self.glevel]:
                  if self.cellinfo[k][m].picid>0:
                      movepic.append(self.cellinfo[k][m].picid)   
                  k,m=k-1,m+1
              k,m=k+1,m-1
              while len(movepic) >0:
                self.cellinfo[k][m].picid=movepic.pop(0)
                k,m=k+1,m-1
              while k<=enx and m>=1:
                self.cellinfo[k][m].picid=0
                k,m=k+1,m-1
              enx=enx-1
          while sty<=eny:   
              movepic=[]
              k,m=sty,self.GL_ROWS[self.glevel]
              while k<=eny and m>=1:
                  if self.cellinfo[m][k].picid>0:
                      movepic.append(self.cellinfo[m][k].picid)   
                  k,m=k+1,m-1
              k,m=k-1,m+1
              while len(movepic) >0:
                self.cellinfo[m][k].picid=movepic.pop(0)
                k,m=k-1,m+1
              while k>=sty and m<=self.GL_ROWS[self.glevel]:
                self.cellinfo[m][k].picid=0
                k,m=k-1,m+1
              sty=sty+1    
              
    def _move_Lup(self,stx,enx,sty,eny):
        while enx>=stx:
           movepic=[]
           k,m=enx,self.GL_COLS[self.glevel]
           while k>=stx and m>=1:
               if self.cellinfo[k][m].picid>0:
                      movepic.append(self.cellinfo[k][m].picid)   
               k,m=k-1,m-1
           k,m=k+1,m+1
           while len(movepic) >0:
                self.cellinfo[k][m].picid=movepic.pop(0)
                k,m=k+1,m+1
           while k<=enx and m<=self.GL_COLS[self.glevel]:
                self.cellinfo[k][m].picid=0
                k,m=k+1,m+1
           enx=enx-1 
        while eny>=sty:
           movepic=[]
           k,m=eny,self.GL_ROWS[self.glevel] 
           while k>=sty and m>=1: 
               if self.cellinfo[m][k].picid>0:
                      movepic.append(self.cellinfo[m][k].picid)   
               k,m=k-1,m-1
           k,m=k+1,m+1
           while len(movepic) >0:
                self.cellinfo[m][k].picid=movepic.pop(0)
                k,m=k+1,m+1
           while k<=eny and m<=self.GL_ROWS[self.glevel]:
                self.cellinfo[m][k].picid=0
                k,m=k+1,m+1
           eny=eny-1 
           
           
               