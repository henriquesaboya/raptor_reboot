'''
Raptor - Call of the Shadows reboot
Created on 25/06/2016



 Notes:
     Many times you will encounter if 1: statements these were used to fold the test

'''

import os,sys,random,time,threading,sqlite3,colorama
import sound_engine,classes

from def_lib import *
from render import *
from sound_engine import *
from classes import *
from colorama import Fore,Back,Style

colorama.init()
#boot no console
if 1:
    print('\n\n\n\n\n\n')
    print(Back.RED+Fore.WHITE+Style.BRIGHT+'RAPTOR: Call of the Birl'+Style.RESET_ALL+Back.RESET)
    print(Fore.BLACK+Back.LIGHTWHITE_EX+'Created by myself')
    print('2016 @ No Copyrights at all'+Fore.RESET+Back.RESET)

print('\nImporting pygame library...')
import pygame
from pygame.locals import *

print('Importing pyganim library...')
import pyganim

#deve-se pre-incializar esta merda! pq se nao fica com lag de entrada
pygame.mixer.pre_init(frequency=22050,size=-16,channels=2,buffer=32)

print('Initializing pygame')
pygame.init()
pygame.display.init()
pygame.mixer.init()
sound_engine.mixer=sound_engine.Mixer(22050,16,32)

#CONFIGURAÇOES
if 1:
    sresH=1280
    sresV=800
    fps=75
    BGMVOL=0.3
    SFXVOL=0.4
    enable_shadows=True

#CONTROLE/FLAGS
if 1:
    debug=True
    op=0
    kappa=0
    a=0
    distance=0
    main_engine_fps=0
    main_engine_fps_show=0
    main_engine_fps_clock=pygame.time.get_ticks()
    clock=pygame.time.get_ticks()
    enemy_ships=[]

#inicializaões + tela de loading
if 1:
    #loading crosshair file, and starting the renderer thread
    crosshair_file='images/cursor/crosshair.png'
    pygame.mouse.set_visible(False)

    #initializes renderer
    renderer=render.render_thread_class(sresH,sresV,'Raptor',crosshair_file,fps,enable_shadows)
    renderer.start()

    #printing loading screen
    file='images/menu/falido e falencia.png'
    aux=pygame.image.load(file).convert_alpha()
    render.objects.append(classes.Object(aux,430,100,0,0))

    #loading everything from the user and starting the menu
    data_db_file='sql/data.db'
    items_db_file='sql/items.db'
    classes.BGMVOL=BGMVOL
    classes.SFXVOL=SFXVOL
    classes.enable_shadows=enable_shadows
    classes.sresH=sresH
    classes.sresV=sresV
    classes.init(data_db_file,items_db_file)

    bgm_file='bgm/raptor11.ogg'
    bgm_file2='bgm/raptor09.ogg'
    button_sound_file='sounds/menu/button-21.ogg'
    button_select_file='sounds/menu/button-22.ogg'

    menu=classes.menu(crosshair_file,bgm_file,\
                      bgm_file2,button_sound_file,button_select_file)
    renderer.clear_control()




    # aqui tem que ter uma tela se for a primeira vez

    #if menu.lastplayer == -1:
    #se nao houver jogadores criar um.. to do
    #else:
    #   print('lindao!!!!!!')

#loop principal
print('\n\nStarting main loop:')
menu.swap('main')
while 1:
    #rotinas pontuais da troca de menu(executam uma só vez)
    if menu.changed:
        #primeiro finaliza os arquivos do menu anterior

        if menu.last_status=='main':
            print('Leaving main menu...')
            if menu.next_status=='hangar':
                sound_engine.mixer.channel[0].fadeout(500)
                sound_engine.mixer.channel[1].play(menu.bgm2,fade_ms=500)

        elif menu.last_status=='profile':
            print('Leaving profile menu...')

        elif menu.last_status=='hangar':
            print('Leaving '+menu.last_status+' menu...')
            if menu.next_status=='main':
                sound_engine.mixer.channel[1].fadeout(500)
                sound_engine.mixer.channel[0].play(menu.bgm,fade_ms=500)
            elif menu.next_status=='mission':
                sound_engine.mixer.channel[1].fadeout(500)

        elif menu.last_status=='supply':
            print('Leaving '+menu.last_status+' menu...')
            menu.player.ship.redefine_magazine()

        elif menu.last_status=='ship':
            print('Leaving '+menu.last_status+' menu...')

        elif menu.last_status=='mission':
            print('Leaving '+menu.last_status+' menu...')
            menu.cursor.diff_mode()
            renderer.show_cursor=True
            renderer.show_player=False
            renderer.background=False
            renderer.show_static_objects=False
            renderer.showUI=False

            enemy_ships=[]
            distance=0
            if menu.next_status=='hangar':
                sound_engine.mixer.channel[1].play(menu.bgm2,fade_ms=500)
                sound_engine.mixer.channel[2].fadeout(500)
                sound_engine.mixer.channel[3].stop()

            if  menu.next_status=='post_mortum':
                sound_engine.mixer.channel[1].stop()
                sound_engine.mixer.channel[2].stop()
                sound_engine.mixer.channel[3].stop()


        elif menu.last_status=='post_mortum':
            print('Leaving '+menu.last_status)
            sound_engine.mixer.channel[2].stop()

        #então realiza a inicialização do novo menu
        if menu.next_status=='quit':
            print('Flaging renderer')
            renderer.run_flag=False
            print('Flaging sound engine')
            sound_engine.mixer.run_flag=False

            menu.save_data()
            print('Wiping memory...')
            print('Ready to quit...')

            sys.exit()

        if menu.next_status=='main':
            print('Generating main menu...')
            renderer.clear_control()
            renderer.show_cursor=True

            #objetos
            file='images/menu/background.png'#fundo
            #print('loading file: ' + file)
            aux=pygame.image.load(file).convert_alpha()
            render.objects.append(classes.Object(aux,0,0,0,0))

            file='images/menu/menu.png'#fundo
            #print('loading file: ' + file)
            aux=pygame.image.load(file).convert_alpha()
            render.objects.append(classes.Object(aux,700,100,0,0))

            file='images/menu/logo.png'
            aux=pygame.image.load(file).convert_alpha()
            render.objects.append(classes.Object(aux,150,70,0,0))

            file='images/menu/menu_profile_square.png'#moldura
            #print('loading file: ' + file)
            aux=pygame.image.load(file).convert_alpha()
            render.objects.append(classes.Object(aux,715,150,0,0))

            file='images/menu/menu_statistics.png'#texto das estatisticas
            #print('loading file: ' + file)
            aux=pygame.image.load(file).convert_alpha()
            render.objects.append(classes.Object(aux,930,170,0,0))

            render.objects.append(classes.Object(menu.player.image,727,163,0,0))#foto do player atual

            #textos
            filepath='fonts/major_shift.ttf'
            #print('loading file: ' + filepath)
            render.texts.append(classes.text(menu.player.name,filepath,24,colors.WHITE,930,190,1))#nome
            render.texts.append(classes.text(menu.player.callsign,filepath,24,colors.WHITE,930,245,1))#callsign
            render.texts.append(classes.text(menu.player.shipname,filepath,24,colors.WHITE,930,300,1))#shipname
            filepath='fonts/AndikaNewBasic-BI.ttf'
            #print('loading file: '+ filepath)
            render.texts.append(classes.text('Selected profile',filepath,30,colors.RED1,800,110,1))#elementos do menu

            #carrega os botoes
            k=480
            for i in ['a','b','c','d']:
                patha='dev_menu/buttons/'+menu.next_status+'/button_'+i+'0.png'
                pathb='dev_menu/buttons/'+menu.next_status+'/button_'+i+'1.png'
                render.buttons.append(classes.MenuButton(patha,pathb,100,k))
                k+=30

            #linhas
            render.lines.append(classes.line((600,450),(600,700),colors.RED,3))

            sound_engine.mixer.channel[0].play(menu.bgm,fade_ms=500)


            menu.update(renderer)

        if menu.next_status=='profile':
            print('Generating profiles menu...')
            renderer.clear_control()
            #controle pra nao dar merda

            #objetos
            file='images/menu/menu.png'#fundo
            #print('loading file: ' + file)
            aux=pygame.image.load(file).convert_alpha()
            render.objects.append(classes.Object(aux,700,100,0,0))

            file='images/menu/menu_profile_square.png'#molduras
            #print('loading file: ' + file)
            aux=pygame.image.load(file).convert_alpha()
            render.objects.append(classes.Object(aux,715,150,0,0))

            file='images/menu/menu_statistics.png'#texto das estatisticas
            #print('loading file: ' + file)
            aux=pygame.image.load(file).convert_alpha()
            render.objects.append(classes.Object(aux,930,170,0,0))

            render.objects.append(classes.Object(menu.player.image,727,163,0,0))#foto do player atual

            #botoes
            #menu
            k=480
            for i in ['a','b']:
                patha='dev_menu/buttons/'+menu.next_status+'/button_'+i+'0.png'
                pathb='dev_menu/buttons/'+menu.next_status+'/button_'+i+'1.png'
                render.buttons.append(classes.MenuButton(patha,pathb,100,k))
                k+=30

                #setinhas

            i='c'
            patha='dev_menu/buttons/'+menu.next_status+'/button_'+i+'0.png'
            pathb='dev_menu/buttons/'+menu.next_status+'/button_'+i+'1.png'
            render.buttons.append(classes.MenuButton(patha,pathb,640,365,'centered'))

            i='d'
            patha='dev_menu/buttons/'+menu.next_status+'/button_'+i+'0.png'
            pathb='dev_menu/buttons/'+menu.next_status+'/button_'+i+'1.png'
            render.buttons.append(classes.MenuButton(patha,pathb,1170,365,'centered'))

            #textos
            filepath='fonts/Capture_it.ttf'
            #print('loading file: ' + filepath)
            render.texts.append(classes.text('RAPTOR',filepath,70,colors.WHITE,300,100))#título
            render.texts.append(classes.text('Call of the Birl',filepath,40,colors.RED,300,180))#subtítulo

            filepath='fonts/major_shift.ttf'
            #print('loading file: ' + filepath)
            render.texts.append(classes.text(menu.player.name,filepath,24,colors.WHITE,930,190,1))#nome
            menu.player_text_index=len(render.texts)-1
            render.texts.append(classes.text(menu.player.callsign,filepath,24,colors.WHITE,930,245,1))#callsign
            render.texts.append(classes.text(menu.player.shipname,filepath,24,colors.WHITE,930,300,1))#shipname
            filepath='fonts/AndikaNewBasic-BI.ttf'
            #print('loading file: '+ filepath)
            render.texts.append(classes.text('Selected profile',filepath,30,colors.RED1,800,110,1))#elementos do menu

            #linhas
            render.lines.append(classes.line((600,450),(600,700),colors.RED,3))
            menu.update_menu_profile_data()


            menu.update(renderer)

        if menu.next_status=='hangar':
            print('Generating hangar menu...')
            renderer.clear_control()

            #fundo + timer da lmapada piscante
            patha='dev_menu/hangar/hangar1.png'
            pathb='dev_menu/hangar/hangar2.png'
            render.objects.append(classes.MenuButton(patha,pathb,0,0,abs))
            light_interval=500
            light_timer=pygame.time.get_ticks()

            filepath='fonts/Capture_it.ttf'
            render.texts.append(classes.text('aaaaaa',filepath,50,colors.RED,sresH/2,780))

            #botoes
            patha='dev_menu/buttons/hangar/exit.png'
            render.buttons.append(classes.MenuButton(patha,patha,(sresH/2)-300,sresV-80,abs))

            patha='dev_menu/buttons/hangar/supply.png'
            render.buttons.append(classes.MenuButton(patha,patha,740,470,abs))

            patha='dev_menu/buttons/hangar/my_ship.png'
            render.buttons.append(classes.MenuButton(patha,patha,0,sresV-675,abs))

            patha='dev_menu/buttons/hangar/mission.png'
            render.buttons.append(classes.MenuButton(patha,patha,195,460,abs))

            patha='dev_menu/buttons/hangar/save.png'
            render.buttons.append(classes.MenuButton(patha,patha,680,140,abs))

        if menu.next_status=='supply':
            print('Generating supply menu...')
            renderer.clear_control()
            classes.play_sound('menu_swap')

            #objetos
            if 1:
                file='images/supply_room/background.png'#background
                aux=pygame.image.load(file).convert_alpha()
                render.objects.append(classes.Object(aux,0,0,0,0))

                file='images/supply_room/ledG.png'  # background
                aux=pygame.image.load(file).convert_alpha()
                render.objects.append(classes.Object(aux,230,625,0,0,'centered'))

                file='images/supply_room/ledR.png'  # background
                aux=pygame.image.load(file).convert_alpha()
                render.objects.append(classes.Object(aux,250,625,0,0,'centered'))

                #foto do pleie
                aux=menu.player.image
                aux=classes.Object(aux,105,290,0,0)
                render.objects.append(aux)

                # foto item
                item_picture_id=len(render.objects)
                file='dev_menu/supply_room/audrey.png'
                aux=pygame.image.load(file).convert_alpha()
                aux=classes.Object(aux,930,168,0,0)
                render.objects.append(aux)

            #butoes
            if 1:
                #exit(invisivel)#0
                patha='images/supply_room/exit_btn.png'
                pathb='images/supply_room/exit_btn.png'
                render.buttons.append(classes.MenuButton(patha,pathb,0,670,'abs'))

                # select buy#1
                buy_btn_index=len(render.buttons)
                patha='images/supply_room/buy_ON.png'
                pathb='images/supply_room/buy_ON.png'
                render.buttons.append(classes.MenuButton(patha,pathb,467,643,'abs'))

                # sel sell#2
                sell_btn_index=len(render.buttons)
                patha='images/supply_room/sell_OFF.png'
                pathb='images/supply_room/sell_OFF.png'
                render.buttons.append(classes.MenuButton(patha,pathb,560,643,'abs'))

                # acao#3
                patha='images/supply_room/BUY_SELL_BTN.png'
                pathb='images/supply_room/BUY_SELL_BTN.png'
                render.buttons.append(classes.MenuButton(patha,pathb,706,620,'abs'))

                # crusor esq#4
                patha='images/supply_room/sel_LEFT.png'
                pathb='images/supply_room/sel_LEFT.png'
                render.buttons.append(classes.MenuButton(patha,pathb,976,639,'abs'))

                # cursordir#5
                patha='images/supply_room/sel_RIGHT.png'
                pathb='images/supply_room/sel_RIGHT.png'
                render.buttons.append(classes.MenuButton(patha,pathb,1087,639,'abs'))

            # textos
            player_money_text_id=len(render.texts)
            filepath='fonts/AndikaNewBasic-R.ttf'
            txt=''
            render.texts.append(classes.text(txt,filepath,32,colors.GRAY_MENU,185,580,0))  # dinhero

            buy_sell_text_id=len(render.texts)
            filepath='fonts/AndikaNewBasic-R.ttf'
            txt=''
            render.texts.append(classes.text(txt,filepath,48,colors.GREEN_SUP_ROOM,798,666,0))  # botao sell/buy

            have_str_text_id=len(render.texts)
            filepath='fonts/AndikaNewBasic-R.ttf'
            txt=''
            render.texts.append(classes.text(txt,filepath,30,colors.GREEN_MENU,512,500,1))

            cost_text_id=len(render.texts)
            filepath='fonts/AndikaNewBasic-R.ttf'
            txt=''
            render.texts.append(classes.text(txt,filepath,30,colors.GREEN_MENU,900,500,1))

            # textos de descrição

            #name
            name_text_id=len(render.texts)
            filepath='fonts/AndikaNewBasic-R.ttf'
            txt="WELCOME TO AUDREY'S"
            render.texts.append(classes.text(txt,filepath,30,colors.YELLOW_MENU,542,180,1))

            #function
            function_text_id=len(render.texts)
            filepath='fonts/AndikaNewBasic-R.ttf'
            txt='WEAPONS EMPORIUM'
            render.texts.append(classes.text(txt,filepath,28,colors.RED_MENU,600,220,1))

            # cost
            value_text_id=len(render.texts)
            filepath='fonts/AndikaNewBasic-R.ttf'
            txt=''
            render.texts.append(classes.text(txt,filepath,36,colors.GRAY_MENU,980,556,0))

            # have or not
            have_text_id=len(render.texts)
            filepath='fonts/AndikaNewBasic-R.ttf'
            txt=''
            render.texts.append(classes.text(txt,filepath,36,colors.GRAY_MENU,610,556,0))



            #description
            shop_texts_id=[]
            k=0
            for i in range(6):
                shop_texts_id.append(len(render.texts))
                filepath='fonts/AndikaNewBasic-R.ttf'
                txt=classes.shop_description_lines[16][i]
                render.texts.append(classes.text(txt,filepath,30,colors.RED,512,280+k,1))
                k+=32



            #audio
            aux='sounds/ship/change_weapon.ogg'
            action_sound=pygame.mixer.Sound(aux)
            action_sound.set_volume(SFXVOL*0.9)

            #variaveis de controle
            if 1:
                mode='buy'
                cursor=0
                display=classes.Display(player_money_text_id,item_picture_id,name_text_id,function_text_id,\
                                        shop_texts_id,have_text_id,cost_text_id,value_text_id,\
                                        buy_sell_text_id,have_str_text_id)

        if menu.next_status=='ship':
            print('Generating ship menu...')
            renderer.clear_control()
            filepath='fonts/Capture_it.ttf'
            render.texts.append(classes.text('SHIP MENU',filepath,70,colors.WHITE,sresH/2,sresV/2))

        if menu.next_status=='mission':
            print('Generating mission...')
            renderer.clear_control()
            #entra no modo diferencial
            menu.cursor.diff_mode()
            #esconde o cursor
            renderer.show_cursor=False
            classes.play_sound('menu_swap')
            menu.player.ship.redefine_magazine()

            # define canal 2 - bgm
            if 1:
                wave_bgm_file='bgm/raptor02.ogg'
                wave_sound=pygame.mixer.Sound(wave_bgm_file)
                wave_sound.set_volume(0.5*BGMVOL)
                sound_engine.mixer.channel[2].play(wave_sound,loops=-1)

            #loading
            if 1:
                render.lines.append(classes.loading_line((50,sresV-10),(sresH-50,sresV-10),colors.RED1,2))

                wave='a0'
                print('Loading enemy ships list - may take some time (wave '+str(wave)+')')

                total_ships,overtime=classes.load_wave_list(wave,enemy_ships,render.lines[0])
                next_ship_spawn=enemy_ships[0]
                next_ship=0
                wave_over=False
                ship_died=False
                ship_died_time=-1
                ship_boom_clock=-1
                played_sound=False
                big_boom=True
                last_ship_killed_time=-1
                renderer.clear_control()
                renderer.show_static_objects=True
                renderer.showUI=True
                player_halt=-1

            #inits basicos
            if 1:

                #define canal 3 - barulho do vento
                jet_sound_file='sounds/jet_interior.ogg'
                jet_sound=pygame.mixer.Sound(jet_sound_file)
                jet_sound.set_volume(0.5*SFXVOL)
                sound_engine.mixer.channel[3].play(jet_sound,loops=-1)

                desired_pos=[]
                desired_pos.append(sresH/2)
                desired_pos.append(100)
                was_firing=False
                clicked_wm2=False

                #fundo
                file='images/background.png'#fundo
                #print('loading file: ' + file)
                aux=pygame.image.load(file).convert_alpha()
                render.background=classes.Background(aux,2)
                renderer.background=True

                render.player=menu.player.ship
                renderer.show_player=True

                weapon_object_number=len(render.objects)

                render.objects.append(menu.player.ship.weapon_magazine[menu.player.ship.active_weapon])

                #linhas
                render.lines.append(classes.line((1250,0),(1250,800),colors.WHITE,1))
                render.lines.append(classes.line((30,0),(30,800),colors.WHITE,1))

                 #avisa pra nave q vai entrar em batalha
                menu.player.ship.enter_battle()
                kappa=pygame.time.get_ticks()

            #carrega ja a tela de post portum
            if 1:
                post_mortum_a=[]
                post_mortum_b=[]
                name='post_mortum_a'
                n=30
                spritelist=[]
                for i in range(n):
                    aux='images/'+name+'/'+str(i)+'.jpg'
                    post_mortum_a.append(pygame.image.load(aux))
                name='post_mortum_b'
                n=11
                spritelist=[]
                for i in range(n):
                    aux='images/'+name+'/'+str(i)+'.jpg'
                    post_mortum_b.append(pygame.image.load(aux))

        if menu.next_status=='post_mortum':
            print('Entering post-mortum')
            renderer.clear_control()
            renderer.show_cursor=False
            renderer.debug_text.update_text('post-mortum')

            clock=pygame.time.get_ticks()
            # define canal 2 - bgm
            wave_bgm_file='bgm/raptor08.ogg'
            wave_sound=pygame.mixer.Sound(wave_bgm_file)
            wave_sound.set_volume(1*BGMVOL)
            sound_engine.mixer.channel[2].play(wave_sound,loops=-1)


            #
            k=0
            state=0
            t=250
            render.objects.append(classes.Object(post_mortum_a[k],0,0,0,0))
            clock=pygame.time.get_ticks()



        menu.done_loading()#informa ao menu,que Load/Unloads foram realizados


    #rotinas cíclicas    
    else:
        while menu.status=='main':
            for event in pygame.event.get():
                if event.type==QUIT:
                    menu.swap('quit')
                if event.type==KEYDOWN:
                    if event.key==K_p:
                        menu.cursor.diff_mode()
                    elif event.key==K_F2:
                        menu.swap('profile')

            keys=pygame.key.get_pressed()
            if keys[K_q] and keys[K_LALT]:
                menu.swap('quit')

            #atualiza o menu
            menu.update(renderer)

            #debug_text
            renderer.debug_text.update_text('Mouse: X,Y('+str(menu.cursor.posX)\
                                            +','+str(menu.cursor.posY)+')'\
                                            +' dX,dY('+str(menu.cursor.posdX)\
                                            +','+str(menu.cursor.posdY)+')'\
                                            +'m1,m2,m3'+str(menu.cursor.buttons),colors.BLUE1)

        while menu.status=='profile':
            for event in pygame.event.get():
                if event.type==QUIT:
                    menu.swap('quit')
                if event.type==KEYDOWN:
                    if event.key==K_p:
                        menu.cursor.diff_mode()
                    elif event.key==K_F1:
                        menu.swap('main')
                    elif event.key==K_r:
                        menu.swap_player('+')
                    elif event.key==K_e:
                        menu.swap_player('-')
                    elif event.key==K_w:
                        menu.swap_player('*')
                    elif event.key==K_q:
                        menu.swap_player('**')

            keys=pygame.key.get_pressed()
            if keys[K_q]&keys[K_LALT]:
                menu.swap('quit')

            #atualiza o menu
            menu.update(renderer)

            #debugs
            renderer.debug_text.update_text('Mouse: X,Y('+str(menu.cursor.posX)+','+str(menu.cursor.posY)+')'\
                                            +'  dX,dY('+str(menu.cursor.posdX)+','+str(menu.cursor.posdY)+')'\
                                            +'  m1,m2,m3'+str(menu.cursor.buttons)\
                                            +'  selected player:'+str(menu.selected_player)\
                                            +'  active player:'+str(menu.active_player),colors.BLUE1)

        while menu.status=='hangar':
            for event in pygame.event.get():
                if event.type==QUIT:
                    menu.swap('quit')
                if event.type==KEYDOWN:
                    if event.key==K_p:
                        menu.cursor.diff_mode()
                    elif event.key==K_F1:
                        menu.swap('main')

            keys=pygame.key.get_pressed()
            if keys[K_q]&keys[K_LALT]:
                menu.swap('quit')

            #lampada flickerando no hangar
            if (pygame.time.get_ticks()-light_timer)>=light_interval:
                light_timer=pygame.time.get_ticks()
                light_interval=random.randrange(150)+50
                render.objects[0].swap_image()


                #atualiza o menu
            menu.update(renderer)

            if menu.op!=None:
                if menu.op==0:
                    render.texts[0].update_text('RETURN TO MAIN MENU')
                elif menu.op==1:
                    render.texts[0].update_text('SUPPLY ROOM')
                elif menu.op==2:
                    render.texts[0].update_text('MY SHIP')
                elif menu.op==3:
                    render.texts[0].update_text('MISSION MENU')
                elif menu.op==4:
                    render.texts[0].update_text('SAVE PROFILE')
            else:
                render.texts[0].update_text('')

            #debugs
            renderer.debug_text.update_text('Mouse: X,Y('+str(menu.cursor.posX)+','+str(menu.cursor.posY)+')'\
                                            +' dX,dY('+str(menu.cursor.posdX)+','+str(menu.cursor.posdY)+')'\
                                            +'m1,m2,m3'+str(menu.cursor.buttons)\
                                            +'op('+str(menu.op)+')',colors.BLACK)

        while menu.status=='supply':
            for event in pygame.event.get():
                if event.type==QUIT:
                    menu.swap('quit')
                if event.type==KEYDOWN:
                    if event.key==K_p:
                        menu.cursor.diff_mode()
                    elif event.key==K_F1:
                        menu.swap('hangar')

            #atualiza o menu
            a=menu.update(renderer)


            if display.status=='intro':
                if menu.cursor.buttons[2]==1 or menu.cursor.buttons[0]==1:
                   display.swap(mode)
                   render.objects[item_picture_id].rect.centerx+=50
                   display.update(menu.player.money,cursor,classes.get_if_have(menu.player.ship,cursor),False)
                   render.texts[have_str_text_id].update_text('YOU HAVE')
                   render.texts[cost_text_id].update_text('COST')

            elif display.status=='error':
                if a!=None:
                    a=a[1:]
                    if a=='ok':
                        display.status=mode
                        display.recover_from_error()
                        display.update(menu.player.money,cursor,classes.get_if_have(menu.player.ship,cursor),False)

            elif display.status=='buy':
                if a!=None:
                    a=a[1:]
                    if a=='main':
                        menu.swap('hangar')
                        classes.play_sound('menu_swap')
                    else:
                        action_sound.play()
                        if a=='+':
                            mode='buy'
                            render.buttons[buy_btn_index].update_image('images/supply_room/buy_ON.png')
                            render.buttons[sell_btn_index].update_image('images/supply_room/sell_OFF.png')
                            render.texts[buy_sell_text_id].update_text('BUY')
                        elif a=='-':
                            mode='sell'
                            display.enter_sell_mode(menu.player)
                            cursor=0
                            render.texts[cost_text_id].update_text('RESALE')
                            display.update(menu.player.money,cursor,\
                                           classes.get_if_have(menu.player.ship,cursor),True)
                            render.buttons[buy_btn_index].update_image('images/supply_room/buy_OFF.png')
                            render.buttons[sell_btn_index].update_image('images/supply_room/sell_ON.png')
                            render.texts[buy_sell_text_id].update_text('SELL')
                        elif a=='ok':
                            b=classes.buy_weapon(menu.player,cursor)
                            if b<0:
                                display.swap('error',b)
                            else:
                                display.update(menu.player.money,cursor,\
                                               classes.get_if_have(menu.player.ship,cursor),False)

                        elif a=='l':
                            if cursor==0:
                                cursor=15
                            else:
                                cursor-=1
                            display.update(menu.player.money,cursor,classes.get_if_have(menu.player.ship,cursor),False)
                        elif a=='r':
                            if cursor==15:
                                cursor=0
                            else:
                                cursor+=1
                            display.update(menu.player.money,cursor,classes.get_if_have(menu.player.ship,cursor),False)

            elif display.status=='sell':
                if a!=None:
                    a=a[1:]
                    if a=='main':
                        menu.swap('hangar')
                        classes.play_sound('menu_swap')

                    else:
                        action_sound.play()
                        if a=='+':
                            mode='buy'
                            render.texts[cost_text_id].update_text('COST')
                            display.swap('buy')
                            render.buttons[buy_btn_index].update_image('images/supply_room/buy_ON.png')
                            render.buttons[sell_btn_index].update_image('images/supply_room/sell_OFF.png')
                            render.texts[buy_sell_text_id].update_text('BUY')
                        elif a=='-':
                            mode='sell'
                            render.buttons[buy_btn_index].update_image('images/supply_room/buy_OFF.png')
                            render.buttons[sell_btn_index].update_image('images/supply_room/sell_ON.png')
                            render.texts[buy_sell_text_id].update_text('SELL')
                        elif a=='ok':
                            if classes.sell_weapon(menu.player,cursor,display)==-1:
                                cursor=display.next(cursor)
                            display.update(menu.player.money,cursor, \
                                        classes.get_if_have(menu.player.ship,cursor),True)
                        elif a=='l':
                            cursor=display.prev(cursor)
                            display.update(menu.player.money,cursor, \
                                        classes.get_if_have(menu.player.ship,cursor),True)
                        elif a=='r':
                            cursor=display.next(cursor)
                            display.update(menu.player.money,cursor, \
                                        classes.get_if_have(menu.player.ship,cursor),True)

            #debug_text
            renderer.debug_text.update_text('Mouse: X,Y('+str(menu.cursor.posX)\
                                            +','+str(menu.cursor.posY)+')'\
                                            +' dX,dY('+str(menu.cursor.posdX)\
                                            +','+str(menu.cursor.posdY)+')'\
                                            +'m1,m2,m3'+str(menu.cursor.buttons)\
                                            +'op('+str(menu.op)+')' \
                                            +'cursor('+str(cursor)+')'\
                                            +'display_status('+str(display.status)+')',colors.BLACK)

        while menu.status=='ship':
            for event in pygame.event.get():
                if event.type==QUIT:
                    menu.swap('quit')
                if event.type==KEYDOWN:
                    if event.key==K_p:
                        menu.cursor.diff_mode()
                    elif event.key==K_F1:
                        menu.swap('hangar')

        while menu.status=='mission':
            #le os eventos
            for event in pygame.event.get():
                if event.type==QUIT:
                    menu.swap('quit')
                if event.type==KEYDOWN:
                    if event.key==K_p:
                        menu.cursor.diff_mode()
                    elif event.key==K_F1:
                        menu.swap('hangar')
                    elif event.key==K_BACKQUOTE:
                        render.player.switch_weapon(weapon_object_number,0)
                    elif event.key==K_1:
                        render.player.switch_weapon(weapon_object_number,1)
                    elif event.key==K_2:
                        render.player.switch_weapon(weapon_object_number,2)
                    elif event.key==K_3:
                        render.player.switch_weapon(weapon_object_number,3)
                    elif event.key==K_4:
                        render.player.switch_weapon(weapon_object_number,4)
                    elif event.key==K_5:
                        render.player.switch_weapon(weapon_object_number,5)
                    elif event.key==K_6:
                        render.player.switch_weapon(weapon_object_number,6)
                    elif event.key==K_7:
                        render.player.switch_weapon(weapon_object_number,7)
                    elif event.key==K_8:
                        render.player.switch_weapon(weapon_object_number,8)
                    elif event.key==K_9:
                        render.player.switch_weapon(weapon_object_number,9)

            # atualiza o menu
            menu.update(renderer)




            #move a nave &verifica posição desejada para ver se cabe na tela
            if last_ship_killed_time==-1:
                if desired_pos[0]+menu.cursor.posdX<sresH-34 and desired_pos[0]+menu.cursor.posdX>34:
                    desired_pos[0]+=menu.cursor.posdX
                if desired_pos[1]+menu.cursor.posdY>40 and desired_pos[1]+menu.cursor.posdY<sresV-40:
                    desired_pos[1]+=menu.cursor.posdY
                #move a nave
                render.player.move(desired_pos)



            if pygame.time.get_ticks()-clock>=16:
                clock=pygame.time.get_ticks()

                #verifica naves inimgas novas na lista e as adiciona ate a wave acabar
                distance+=1
                if ship_died:
                    if pygame.time.get_ticks()-ship_died_time>=3000:
                        menu.swap('post_mortum')


                    else:
                        if pygame.time.get_ticks()-ship_died_time>=1500 and big_boom:
                            for i in classes.big_boom_list:
                                classes.spawn_sprite(menu.player.ship.rect.centerx+i[0],menu.player.ship.rect.centery+i[1],'medium_explosion')

                            big_boom=False
                            renderer.show_player=False

                        if pygame.time.get_ticks()-ship_boom_clock>=30:
                            ship_boom_clock=pygame.time.get_ticks()
                            a=random.randrange(2)
                            if a==0:
                                a='small_explosion'
                            elif a==1:
                                a='medium_explosion'
                            x=random.randrange(-50,50)
                            y=random.randrange(-50,50)
                            classes.spawn_sprite(menu.player.ship.rect.centerx+x,menu.player.ship.rect.centery+y,a)


                else:
                    if not wave_over:
                        if distance>=enemy_ships[next_ship].spawn_distance:
                            render.enemy_ships.append(enemy_ships[next_ship])
                            next_ship+=1
                            if next_ship==total_ships:
                                wave_over=True


                    elif wave_over:
                        if len(render.enemy_ships)==0:
                            if last_ship_killed_time==-1:
                                last_ship_killed_time=pygame.time.get_ticks()
                            else:
                                if pygame.time.get_ticks()-last_ship_killed_time>=100:
                                    if not played_sound:
                                        classes.play_sound('leave_wave')
                                        played_sound=True
                                    render.player.move((render.player.rect.centerx,render.player.rect.centery-20))

                            if pygame.time.get_ticks()-last_ship_killed_time>=overtime:



                                menu.swap('hangar')



                #atualiza posicoes
                render.update_list(render.projectiles)
                render.update_list(render.sprites)
                render.update_list(render.enemy_ships)

                render.background.update_rect()

                #verica colisoes com projeteis
                for i in render.projectiles:
                    #se o projetil ainda for valido
                    if i.valid:

                    #se o tiro nao for amigavel eu tomo dano
                        if not i.friendly:
                            #verifica se eu tomei dano, retorna true se sim
                            if render.player.colliderect(i.rect):
                                #entao me desconta a vida
                                if render.player.take_damage(i.damage,i.rect.centerx):
                                    ship_died=True
                                    ship_died_time=pygame.time.get_ticks()
                                    classes.play_sound('death_boom')
                                #e invalida o projetil
                                i.valid=False

                        #se algum inimigo tomou dano:
                        else:
                            for a in render.enemy_ships:
                                #se tiver viva
                                    #verifica se colidiu
                                if a.rect.colliderect(i.rect):
                                    if a.alive:
                                        #na funcao take damage, retorna se ela acabou de morrer, pois outros projeteis
                                        #podem pegar ao memsmo tempo
                                        if a.take_damage(i):
                                            #se tudo occoreu bem voce leva o dinheiro para casa
                                            menu.player.money+=a.value
                                    #invalida o projetil
                                    i.valid=False

                #verifica colisoes com naves inimigas
                for i in render.enemy_ships:
                    if render.player.colliderect(i.rect):
                        if render.player.take_damage(i.hp//100,i.rect.centerx):
                            ship_died=True
                            ship_died_time=pygame.time.get_ticks()
                            classes.play_sound('death_boom')
                        i.take_damage(render.player)

            #atira se tiver com wm1 apertado
            if menu.cursor.buttons[0]:
                a,b,src=render.player.fire()

                if a!=None:
                    if render.enemy_ships[a].take_damage(src):
                        menu.player.money+=render.enemy_ships[a].value
                        if a==b:
                            b=None
                if b!=None:
                    if render.enemy_ships[b].take_damage(src):
                        menu.player.money+=render.enemy_ships[b].value
            else:
                render.player.unfire()


            #troca de arma se APERTOU wm2
            if not clicked_wm2:
                if menu.cursor.buttons[2]:
                    render.player.switch_weapon(weapon_object_number)
                clicked_wm2=True
            if clicked_wm2:
                if not menu.cursor.buttons[2]:
                    clicked_wm2=False

            #faz naves inimiags atirarem
            for i in render.enemy_ships:
                i.fire()

            #conta fps
            main_engine_fps+=1
            if pygame.time.get_ticks()-main_engine_fps_clock >=1000:
                main_engine_fps_clock=pygame.time.get_ticks()
                main_engine_fps_show=main_engine_fps
                main_engine_fps=0


            #debug_text
            a=pygame.time.get_ticks()
            renderer.debug_text.update_text('mBtt'+str(menu.cursor.buttons)\
                                            +'  dpos('+str(desired_pos)+')'\
                                            +'  nProj:'+str(len(render.projectiles))\
                                            +'  nObj:'+str(len(render.objects))\
                                            +'  nEnemy:'+str(len(render.enemy_ships)) \
                                            +'  nLines:'+str(len(render.lines)) \
                                            +'  HP:'+str(menu.player.ship.energy_module.current_hp)\
                                            +'  Shld:'+str(menu.player.ship.shield.current_hp)\
                                            +'  Dead:'+str(ship_died)\
                                            +'  plyr$:'+str(menu.player.money)\
                                            +'  Dist:'+str(distance)\
                                            +'  Enemy:'+str(next_ship)+'/'+str(total_ships)\
                                            +'  MainFPS:'+str(main_engine_fps_show)\
                                            +'  RenderFPS:'+str(renderer.fps_show)\
                                            +'  fTime: '+str(renderer.frametime)+'ms'\
                                            +'  ActiveWpN: '+str(render.player.active_weapon),colors.WHITE)

        while menu.status=='post_mortum':
            for event in pygame.event.get():
                if event.type==QUIT:
                    menu.swap('quit')
                if event.type==KEYDOWN:
                    menu.swap('main')

            menu.update(renderer)

            if menu.cursor.buttons[0]:
                menu.swap('main')

            if pygame.time.get_ticks()-clock>=t:
                clock=pygame.time.get_ticks()
                if state==0:
                    k+=1
                    render.objects[0].change_image(post_mortum_a[k])
                    if k==29:
                        state=1
                        k=0
                        t=160
                else:
                    render.objects[0].image=post_mortum_b[k]
                    k+=1
                    if k==11:
                        k=0



#########################################
########### FUNÇOES AUXILIARES ##########
#########################################
