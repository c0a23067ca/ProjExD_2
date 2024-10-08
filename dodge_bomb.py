import os
import sys
import pygame as pg
import random
import time

WIDTH, HEIGHT = 1100, 650
os.chdir(os.path.dirname(os.path.abspath(__file__)))
DELTA={
        pg.K_UP:(0,-5),
        pg.K_DOWN:(0,5),
        pg.K_LEFT:(-5,0),
        pg.K_RIGHT:(5,0)
        }

def bomb(lst1,lst2,count):
    """
    引数：リスト、リスト、インデックス
    戻り値　タプル（１つ目のリストからインデックスで取り出した値、２つ目のリストからインデックスで取り出した値）
    """

    return lst1[count],lst2[count]


def check_bound(obj_rct: pg.Rect) -> tuple[bool,bool]:
    """
    引数：こうかとん　または　爆弾のRect
    戻り値：真理値タプル（横判定結果、縦判定結果）
    画面内ならTrue、画面外ならFalse
    """
    yoko,tate = True,True
    if obj_rct.left < 0 or WIDTH < obj_rct.right:
         yoko = False
    if obj_rct.top < 0 or HEIGHT < obj_rct.bottom:
         tate = False
    return yoko,tate


def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    fonto = pg.font.Font(None,80)
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200
    #bb_img = pg.Surface((20,20))
    
    accs = [a for a in range(1, 11)]
    bb_imgs=[]
    bb_rcts=[]
    for r in range(1, 11):                                       #拡大のために大きくしていく
         bb_img = pg.Surface((20*r, 20*r))
         pg.draw.circle(bb_img, (255, 0, 0), (10*r, 10*r), 10*r)
         bb_imgs.append(bb_img)
         bb_img.set_colorkey((0,0,0))
         bb_rcts.append(bb_img.get_rect())                       #リストに追加
    #pg.draw.circle(bb_img,(255,0,0),(10,10),10)
    #bb_rct = bb_imgs[0].get_rect()
    bb_rcts[0].center = random.randint(0,WIDTH),random.randint(0,HEIGHT)
    vx,vy = 5,5
    go_img = pg.Surface((WIDTH,HEIGHT))                 #game over時の表示のsurface
    go_img.set_alpha(100)
    go_rct = go_img.get_rect()
    go_rct.center = WIDTH/2,HEIGHT/2
    go_txt = fonto.render("Game Over", True, (255,255,255))
    txt_rct = go_txt.get_rect()
    txt_rct.center = WIDTH/2,HEIGHT/2
    cry_img = pg.transform.rotozoom(pg.image.load("fig/8.png"), 0, 0.9)  #泣いているこうかとんの画像読み込み
    cry_rct1= cry_img.get_rect()
    cry_rct2 = cry_img.get_rect()
    cry_rct1.center = WIDTH/2-200,HEIGHT/2
    cry_rct2.center = WIDTH/2+200,HEIGHT/2
    clock = pg.time.Clock()
    tmr = 0

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        screen.blit(bg_img, [0, 0]) 
        if kk_rct.colliderect(bb_rcts[min(tmr//500, 9)]):       #こうかとんと爆弾が衝突したら
            screen.blit(go_img,go_rct)
            screen.blit(go_txt,txt_rct)
            screen.blit(cry_img,cry_rct1)
            screen.blit(cry_img,cry_rct2)
            pg.display.update()
            time.sleep(5)
            return
        bb_rcts[min(tmr//500, 9)+1][0] = bb_rcts[min(tmr//500, 9)][0]
        bb_rcts[min(tmr//500, 9)+1][1] = bb_rcts[min(tmr//500, 9)][1]
        avx = vx*accs[min(tmr//500, 9)]
        bb_img = bb_imgs[min(tmr//500, 9)]
        screen.blit(bb_img, bb_rcts[min(tmr//500, 9)])

        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        
        for key , tpl in DELTA.items():
            if key_lst[key]:
                    sum_mv[0]+=tpl[0]
                    sum_mv[1]+=tpl[1]

        # if key_lst[pg.K_UP]:
        #     sum_mv[1] -= 5
        # if key_lst[pg.K_DOWN]:
        #     sum_mv[1] += 5
        # if key_lst[pg.K_LEFT]:
        #     sum_mv[0] -= 5
        # if key_lst[pg.K_RIGHT]:
        #     sum_mv[0] += 5
        kk_rct.move_ip(sum_mv)
        if check_bound(kk_rct) != (True,True):
             kk_rct.move_ip(-sum_mv[0],-sum_mv[1])
        screen.blit(kk_img, kk_rct)
        bb_rcts[min(tmr//500, 9)].move_ip(avx,vy)
        yoko,tate = check_bound(bb_rcts[min(tmr//500, 9)])
        if not yoko:
             vx *= -1
        if not tate:
             vy *= -1
        
        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
