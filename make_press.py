"""Genera una storia Press SY Design (layout A) 1080x1920.
Uso: python3 make_press.py spec.json   (spec: oggetto o lista di oggetti)
Campi: out (percorso jpg), n (numero PRESS N°), img (es. img/saetta_1.jpg), lines (righe della citazione,
usare “ ” per le parole citate testualmente), meta ("25 NOVEMBER 2025  ·  AUTORE" in maiuscolo),
attrib (opzionale, chi parla), logo (es. "boat.png" in logos/, oppure null), text_logo (nome testata se manca il logo),
logoh (altezza logo, default 110)."""
import sys,os,json
D=os.path.dirname(os.path.abspath(__file__)); os.chdir(D)
from styl import F,NAVY,CREAM,SAND
from PIL import Image,ImageDraw,ImageFont
W,H=1080,1920
def S(sz): return ImageFont.truetype('fonts/CG-500-italic.ttf',sz)
mark=Image.open('logo/SY_mark_cream.png').convert('RGBA')
def fit169(path,w):
    im=Image.open(path).convert('RGB'); Wi,Hi=im.size; h=round(w*9/16)
    if abs(Wi/Hi-16/9)>.01:
        ch=int(Wi*9/16); top=(Hi-ch)//2; im=im.crop((0,top,Wi,top+ch))
    return im.resize((w,h),Image.LANCZOS)
def sp(d,x,y,t,f,s,fill):
    for c in t: d.text((x,y),c,font=f,fill=fill,anchor='ls'); x+=d.textlength(c,font=f)+s
def spw(d,t,f,s): return sum(d.textlength(c,font=f)+s for c in t)-s
def story(out,n,img,lines,meta,logo=None,attrib=None,size=72,logoh=110,text_logo=None):
    im=Image.new('RGBA',(W,H),NAVY+(255,)); ph=fit169(img,W); im.paste(ph,(0,0))
    g=Image.new('L',(1,220)); [g.putpixel((0,i),int(255*i/219)) for i in range(220)]
    im.paste(Image.new('RGBA',(W,220),NAVY+(255,)),(0,ph.height-220),g.resize((W,220)))
    gt=Image.new('L',(1,240)); [gt.putpixel((0,i),int(150*(1-i/239))) for i in range(240)]
    im.alpha_composite(Image.merge('RGBA',[Image.new('L',(W,240),NAVY[0]),Image.new('L',(W,240),NAVY[1]),Image.new('L',(W,240),NAVY[2]),gt.resize((W,240))]))
    d=ImageDraw.Draw(im)
    sp(d,70,90,f'PRESS  N°{n:02d}',F('600-normal',22),8,CREAM+(255,))
    d.text((60,ph.height+30),'“',font=S(240),fill=SAND+(255,),anchor='lt')
    f=S(size)
    while max(d.textlength(t,font=f) for t in lines)>930: size-=2; f=S(size)
    y=ph.height+230
    for t in lines: d.text((80,y),t,font=f,fill=CREAM+(255,),anchor='ls'); y+=int(size*1.22)
    y+=20; d.line((80,y,200,y),fill=SAND+(255,),width=2); y+=55
    if attrib: sp(d,80,y,attrib,F('600-normal',20),5,CREAM+(220,)); y+=40
    sp(d,80,y,meta,F('600-normal',20),5,SAND+(255,))
    if y>=1340: raise SystemExit(f'Testo troppo lungo in {out}: accorcia le righe')
    if logo and os.path.exists('logos/'+logo):
        lg=Image.open('logos/'+logo).convert('RGBA'); s=min(logoh/lg.height,420/lg.width); lg=lg.resize((int(lg.width*s),int(lg.height*s)),Image.LANCZOS)
        im.alpha_composite(lg,((W-lg.width)//2,1440-lg.height//2))
    else:
        t=(text_logo or '').upper(); ft=F('700-normal',40); w=spw(d,t,ft,6); sp(d,W/2-w/2,1455,t,ft,6,(255,255,255,255))
    d=ImageDraw.Draw(im)
    t="LEGGI L'ARTICOLO"; ft=F('600-normal',24); w=spw(d,t,ft,10); sp(d,W/2-w/2,1600,t,ft,10,CREAM+(255,))
    for a,b in [((W/2,1625),(W/2,1665)),((W/2-12,1653),(W/2,1665)),((W/2+12,1653),(W/2,1665))]: d.line((a,b),fill=CREAM+(255,),width=2)
    m=mark.resize((56,int(mark.height*56/mark.width)),Image.LANCZOS); im.alpha_composite(m,((W-56)//2,1820))
    im.convert('RGB').save(out,quality=95,subsampling=0); print('ok',out)
if __name__=='__main__':
    spec=json.load(open(sys.argv[1])); spec=spec if isinstance(spec,list) else [spec]
    for s in spec: story(**s)
