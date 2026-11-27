from PIL import Image,ImageDraw,ImageFont,ImageFilter
W,H=1080,1920; NAVY=(28,40,48); CREAM=(242,237,230); SAND=(200,185,154)
def F(w,s): return ImageFont.truetype(f'fonts/Montserrat-latin-{w}.ttf',s)
def runs(d,cy,parts,sp,fill):
    w=sum(sum(d.textlength(c,font=f)+sp for c in t) for t,f in parts)-sp; x=W/2-w/2
    for t,f in parts:
        for c in t: d.text((x,cy),c,font=f,fill=fill,anchor='lm'); x+=d.textlength(c,font=f)+sp
    return w
def parse(s,size):
    # *word* -> bold italic
    out=[];bold=False
    for i,chunk in enumerate(s.split('*')):
        if chunk: out.append((chunk,F('700-italic',size) if i%2 else F('300-normal',size)))
    return out
def title_block(d,cy,text,label=None,size=44,lines=True,fill=CREAM+(255,),lab_fill=None):
    w=runs(d,cy,parse(text,size),5,fill)
    if lines:
        for yy in (cy-int(size*1.3),cy+int(size*1.3)): d.rectangle((W/2-w/2,yy,W/2+w/2,yy+1),fill=fill[:3]+(210,))
    if label:
        runs(d,cy-int(size*1.3)-34,[(label,F('400-normal',20))],8,lab_fill or fill)
def shadowed(ov,k=0.5):
    a=ov.split()[3].filter(ImageFilter.GaussianBlur(10)).point(lambda v:int(v*k)); s=Image.new('RGBA',(W,H),(0,0,0,0)); s.putalpha(a); return Image.alpha_composite(s,ov)
def ov_full(text,y=300,label=None):
    ov=Image.new('RGBA',(W,H),(0,0,0,0)); title_block(ImageDraw.Draw(ov),y,text,label); return shadowed(ov)
def ov_kairos(sub_alpha=1.0):
    ov=Image.new('RGBA',(W,H),(0,0,0,0)); d=ImageDraw.Draw(ov)
    w=runs(d,330,[('KAIROS',F('300-normal',120))],34,CREAM+(255,))
    if sub_alpha>0:
        a=int(255*sub_alpha); y=470
        d.rectangle((W/2-w/2,y-46,W/2+w/2,y-45),fill=CREAM+(int(210*sub_alpha),))
        runs(d,y,parse('52 METRES  ·  *MOTOR YACHT*',30),6,CREAM+(a,))
        d.rectangle((W/2-w/2,y+45,W/2+w/2,y+46),fill=CREAM+(int(210*sub_alpha),))
    return shadowed(ov)
def ov_band(label,text):
    ov=Image.new('RGBA',(W,H),(0,0,0,0)); d=ImageDraw.Draw(ov)
    title_block(d,995,text,label,size=44,lab_fill=SAND+(255,)); return ov
mark=Image.open('logo/SY_mark_cream.png')
def ov_end(mw=300,ym=690):
    ov=Image.new('RGBA',(W,H),(0,0,0,0)); d=ImageDraw.Draw(ov)
    m=mark.resize((mw,int(mark.height*mw/mark.width)),Image.LANCZOS); ov.alpha_composite(m,((W-mw)//2,ym))
    title_block(d,ym+m.height+150,'THE *ART* OF THE ESSENTIAL LINE',size=40)
    runs(d,H-220,[('SYDESIGN.IT',F('300-normal',22))],8,CREAM+(150,))
    return ov
