#encoding:gb18030
import math,os
import pygame
INFOSTYLE='data/number.png'
class PathManager:
    HALFWD,HALFHT = 24,24
    def __init__(self, cellinfo):
        self.managed_cellinfo=cellinfo
        self.finded_path=[]
        self.selected_cell=[]
        self.maprow=len(cellinfo)
        self.mapcol=len(cellinfo[0])
        self.pot1=(0, 0)
        self.pot2=(0, 0)
        self.samelink=True
    def set_map(self,cmap):
        self.managed_cellinfo=cmap
    def add_selected_cell(self, se):
        if se not in self.selected_cell:
           if self.managed_cellinfo[se[0]][se[1]].picid>0:
              self.selected_cell.append(se)
              #print "select cell:",se
    def remove_selected_cell(self):
        try:
            self.selected_cell.pop(0)   #删除第一个选择
            #self.selected_cell.remove(id)
            return True
        except IndexError:
            return False
    
    def clear_selected_cell(self):
        self.selected_cell=[]
        
    def passgo(self, idx, idy):
        """ 检查一个单元格是否空，精灵被消除   """
        if (idx>=0 and idx<self.maprow) and (idy>=0 and idy<self.mapcol):
            if self.managed_cellinfo[idx][idy].picid==0:
                return True
            
        return False
    
    def can_startlink(self):
        """检查是否可以开始连线，选择列表是双数个 """
        countc=len(self.selected_cell)
        if countc>0:
            return (countc%2==0)
        else:
            return False
    
    def scan_X(self, x, finx, finy, tinx, tiny):
        """ 扫描X坐标 """  
        fX, mY, tX =1, 1, 1
        
        if x!=finx:
             xDis = int((finx - x) / math.fabs(finx - x))
             
             for n in range(x, finx, xDis):
                if not self.passgo(n, finy):
                    fX=0
                    break
        if x!=tinx:
            xDis = int((tinx-x)/math.fabs(tinx-x))
            
            for n in range(x, tinx, xDis):
                if not self.passgo(n, tiny):
                    tX=0
                    break
        yDis = -int((finy-tiny)/math.fabs(finy-tiny))
        for n in range(finy, tiny, yDis):
            if finy!=n and tiny!=n:
                if not self.passgo(x, n):
                    mY=0
                    break
        
        if fX==1 and tX==1 and mY==1:
            return x+100
        
        return 0
    
    def scan_Y(self, y, finx, finy, tinx, tiny):
        """ 扫描Y坐标  """
        fY, mY, tY=1, 1, 1
        
        if y!=finy:
            yDis=int((finy-y)/math.fabs(finy-y))
            for n in range(y, finy, yDis):
                if not self.passgo(finx, n):
                    fY=0
                    break
        if y!=tiny:
            yDis = int((tiny-y)/math.fabs(tiny-y))
            for n in range(y, tiny, yDis):
                if not self.passgo(tinx, n):
                    tY=0
                    break
                
        xDis = -int((finx-tinx)/math.fabs(finx-tinx))
        for n in range(finx, tinx, xDis):
            if finx!=n and tinx!=n:
                if not self.passgo(n, y):
                    mY=0
                    break
        
        if fY==1 and tY==1 and mY==1:
            return y+10000
        
        return 0
    
    def find_path(self, fc, tc):
        """ 搜索所有在两个精灵之间的连线，找出中间线的矩阵索引 ind_x or ind_y  """
        if fc.ind_x!=tc.ind_x:
            cc = (fc.ind_y>tc.ind_y) and fc.ind_y or tc.ind_y
            res=0
            for yy in range(cc, -1, -1):
                res = self.scan_Y(yy, fc.ind_x, fc.ind_y, tc.ind_x, tc.ind_y)
                if res>0: return res
            for yy in range(cc+1, self.mapcol, 1):
                res = self.scan_Y(yy, fc.ind_x, fc.ind_y, tc.ind_x, tc.ind_y)
                if res>0: return res
        if fc.ind_y!=tc.ind_y:
            cc = (fc.ind_x>tc.ind_x) and fc.ind_x or tc.ind_x
            res=0
            for xx in range(cc, -1, -1):
                res = self.scan_X(xx, fc.ind_x, fc.ind_y, tc.ind_x, tc.ind_y)  
                if res>0: return res
            for xx in range(cc+1, self.maprow, 1):
                res = self.scan_X(xx, fc.ind_x, fc.ind_y, tc.ind_x, tc.ind_y)
                if res>0: return res
        
        return 0        
                
    def test_link(self):
        if not self.can_startlink():return False
        selcount = len(self.selected_cell)
        selidx,selidy = self.selected_cell[selcount-1]
        selidx1,selidy1 = self.selected_cell[selcount-2]
        cell1 = self.managed_cellinfo[selidx][selidy]
        cell2 = self.managed_cellinfo[selidx1][selidy1]
        startpoint = (cell1.pos[0]+self.HALFWD,cell1.pos[1]+self.HALFHT)
        endpoint = (cell2.pos[0]+self.HALFWD,cell2.pos[1]+self.HALFHT)
        midx,midy=0,0
        corner=0
        self.samelink=True
        if selidx==selidx1 and selidy==selidy1: return False,corner
        if cell1.picid==0 or cell2.picid==0: return False,corner
        if cell1.picid!=cell2.picid: 
            self.remove_selected_cell()
            return False,corner
        if cell1.picid==cell2.picid:
            coor = self.find_path(cell1, cell2)
            self.finded_path=[]
            
            
            if coor>=10000:
                find_coor = coor-10000
                
                midx = self.managed_cellinfo[0][find_coor].pos[0]+self.HALFWD
                #print midx,startpoint,endpoint
                if midx==startpoint[0]==endpoint[0]:
                    self.finded_path.append(startpoint)
                    self.finded_path.append(endpoint)
                    corner=1  
                else:
                                 
                    self.finded_path.append(startpoint)
                    if midx==startpoint[0]:
                       self.finded_path.append((midx,endpoint[1]))
                       corner=2
                    elif midx==endpoint[0]:
                       self.finded_path.append((midx,startpoint[1]))
                       corner=2
                    else:
                       self.finded_path.append((midx,startpoint[1]))
                       self.finded_path.append((midx,endpoint[1]))
                       corner=3
                    self.finded_path.append(endpoint)
                
                return True,corner
            elif 10000> coor >=100 :
                find_coor = coor-100
                
                midy = self.managed_cellinfo[find_coor][0].pos[1]+self.HALFHT
                #print midy,startpoint,endpoint
                if midy==startpoint[1]==endpoint[1]:
                    self.finded_path.append(startpoint)
                    self.finded_path.append(endpoint)
                    corner=1
                else:
                    self.finded_path.append(startpoint)
                    if midy==startpoint[1]:
                       self.finded_path.append((startpoint[0],midy))
                       corner=2
                    elif midy==endpoint[1]:
                       self.finded_path.append((endpoint[0],midy))
                       corner=2
                    else:
                       self.finded_path.append((startpoint[0],midy))
                       self.finded_path.append((endpoint[0],midy))
                       corner=3
                    self.finded_path.append(endpoint)
                
                return True,corner
            else:
                self.samelink=False
                self.clear_selected_cell()
                return False,corner
    
    def search_path(self):
        self.clear_selected_cell()
        arr_cell=[]
        for r in self.managed_cellinfo:
            for c in r:
               if c.picid>0:
                   arr_cell.append((c.ind_x,c.ind_y))
        
        for ii in range(len(arr_cell)):
            self.pot1 = arr_cell[ii]
            for jj in range(ii+1,len(arr_cell)):
                self.pot2 = arr_cell[jj]
                self.clear_selected_cell()
                self.add_selected_cell(self.pot1)
                self.add_selected_cell(self.pot2)
                tt,co=self.test_link()
                if tt==True:
                    self.clear_selected_cell()
                    return True
        return False   
     
    def draw_line(self,graph):
        #print self.finded_path
        pygame.draw.lines(graph, (255,50,0), False, self.finded_path, 3)

                         
class cellObject:
    """ 每个单元格对象，包括精灵坐标位置，矩阵索引，图片编号
        """
    def __init__(self, p, inx, iny, pid):
        self.pos=p
        self.ind_x=inx
        self.ind_y=iny
        self.picid=pid

class gameComm:
    WINWIDTH = 880
    WINHEIGHT = 660
    PROGLEN = 400    
    GAMETIME = 120000   #2min时间限制 ms
    def __init__(self):
        import pygame
        self.Font = pygame.font.Font('data/yyf.ttf', 20)
        self.scorecount=0
        self.hintcount=15
        self.heart=3
        self.misslv=1
        self.gamelv=0
        self.sptime=0
        self.prosslen=self.PROGLEN     #进程条长度
        self.size= self.WINWIDTH,self.WINHEIGHT
        self.backgd=None
        self.txtcolor=(255,255,20)
        self.infoimg=pygame.image.load(INFOSTYLE).convert_alpha()
    
    def reinit(self):
        self.scorecount=0
        self.hintcount=15
        self.heart=3
        self.misslv=1
        self.gamelv=0
        self.sptime=0   
    def update_score(self,sc):
        self.scorecount +=sc
    
    def update_hint(self,hit):
        self.hintcount +=hit
    
    def update_heart(self,ht):
        self.heart +=ht
    
    def update_misslv(self,ml):
        self.misslv +=ml
                
    def showtext(self,win, pos, text, color, bgcolor=None):
       if bgcolor is not None:
           textimg = self.Font.render(text, 1, color, bgcolor)
       else:
           textimg = self.Font.render(text, 1, color)
       win.blit(textimg, pos)
       return pos[0] + textimg.get_width() + 25, pos[1]
   
    def loadimg(self,file):
       fpath=os.path.join('data', file)
       try:
          img = pygame.image.load(fpath)
          if img.get_alpha is None:
             img = img.convert()
          else:
             img = img.convert_alpha()
       except Exception as message:
           print ("Con't load image:" , file)
           raise (SystemExit, message)
       return img, img.get_rect()
   
    def _show_num(self,win,num,stpos):
        i=0
        imwd=55
        onumwd=25
        for sc in str(num):
            isc=int(sc)
            recnm=[isc*onumwd,0,onumwd,30]
            win.blit(self.infoimg,(stpos[0]+imwd+20*i,stpos[1]),recnm)
            i=i+1
        return stpos[0]+i*onumwd+imwd+10,stpos[1]
        
    def show_gameinfo(self,win):
        self.Font.set_bold(True)
        recht = pygame.Rect(0,90,60,30)
        
        inx,iny = 30,10         #起始显示信息位置
        win.blit(self.infoimg,(inx,iny),recht)
        ps = self._show_num(win, self.heart, (inx,iny))
        #ps=self.showtext(win,(inx+recht.width,iny),str(self.heart),self.txtcolor)
        recht.move_ip(0, -30)
        win.blit(self.infoimg,ps,recht)
        ps = self._show_num(win, self.hintcount, ps)
        #ps=self.showtext(win,(ps[0]+recht.width,iny), str(self.hintcount), self.txtcolor)
        recht.move_ip(0, -30)
        win.blit(self.infoimg,ps,recht)
        ps = self._show_num(win, self.scorecount, ps)
        #ps=self.showtext(win,(ps[0]+recht.width,iny), str(self.scorecount), self.txtcolor)
        #-----------显示进度条------------#
        recht.move_ip(0,90)
        recht.width=self.prosslen 
        win.blit(self.infoimg,(self.WINWIDTH-405,iny),recht)
        #rec=pygame.draw.rect(win, self.txtcolor,[ps,(300,30)], 1)
        #win.fill((255,0,0,150),rec)
    def set_spendTime(self,tm):
        """游戏花费时间"""
        self.sptime=tm + 0.0
        if self.sptime>self.GAMETIME:return False
        self.prosslen=int(self.PROGLEN*(1-(self.sptime/self.GAMETIME)))
        return True
    
    def set_background(self,filename=None,tile=None,color=None):
        size=self.size
        if filename is not None:
            bg,frec = self.loadimg(filename)
        elif tile is not None:
            tiles,tilerec = self.loadimg(tile)
            bg = pygame.Surface(size).convert()
            for y in range(0, size[1], tilerec.width):
                for x in range(0, size[0], tilerec.height):
                    bg.blit(tiles, (x, y))
        elif color is not None:
            bg = pygame.Surface(size).convert()
            bg.fill(color)
        
        self.backgd=bg
    
            