import sys,json,os
from PIL import Image
import numpy as np
B=json.load(open('/home/claude/korean/card_batches.json'))
D='/mnt/user-data/uploads/Downloads/'
OUT='/home/claude/korean/site/cards/'
def cuts(prof,n):
    L=len(prof);res=[0]
    for k in range(1,3):
        c=int(L*k/3);w=int(L*0.06)
        seg=prof[c-w:c+w];i=int(np.argmax(seg))+c-w
        res.append(i)
    res.append(L);return res
def gutter_bounds(prof,center):
    # expand around center while bright
    t=prof[center]-6
    a=center
    while a>0 and prof[a-1]>=t: a-=1
    b=center
    while b<len(prof)-1 and prof[b+1]>=t: b+=1
    return a,b
for idx in sys.argv[1:]:
    i=int(idx);name=f'card-B{i:03d}.png'
    im=Image.open(D+name).convert('RGB');a=np.asarray(im).astype(float)
    g=a.mean(axis=2)
    colp=np.median(g,axis=0);rowp=np.median(g,axis=1)
    xs=cuts(colp,3);ys=cuts(rowp,3)
    xb=[(0,0)]+[gutter_bounds(colp,x) for x in xs[1:3]]+[(im.width,im.width)]
    yb=[(0,0)]+[gutter_bounds(rowp,y) for y in ys[1:3]]+[(im.height,im.height)]
    for j,(w,m,_) in enumerate(B[i-1]):
        r,c=divmod(j,3)
        x0=xb[c][1]+4;x1=xb[c+1][0]-4;y0=yb[r][1]+4;y1=yb[r+1][0]-4
        cell=im.crop((x0,y0,x1,y1))
        s=min(cell.size);cx,cy=cell.width//2,cell.height//2
        cell=cell.crop((cx-s//2,cy-s//2,cx-s//2+s,cy-s//2+s))
        for ext in ('.png','.jpg'):
            p=OUT+w+ext
            if os.path.exists(p): os.remove(p)
        cell.save(OUT+w+'.jpg',quality=88,optimize=True)
    print(i,'ok',xb,yb)
