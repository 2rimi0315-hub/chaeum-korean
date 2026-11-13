import sys
from PIL import Image
ids=[int(x) for x in sys.argv[1:]]
n=len(ids);cols=4;rows=(n+cols-1)//cols
g=Image.new('RGB',(cols*400,rows*400),'white')
for k,i in enumerate(ids):
    im=Image.open(f'/mnt/user-data/uploads/Downloads/card-B{i:03d}.png').convert('RGB');im.thumbnail((396,396))
    g.paste(im,((k%cols)*400,(k//cols)*400))
g.save('/tmp/vb.jpg',quality=80)
