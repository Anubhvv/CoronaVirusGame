import sys
import cv2
import pygame 
import numpy as np
import time
import os
import sys


# determine if application is a script file or frozen exe
if getattr(sys, 'frozen', False):
    application_path = os.path.dirname(sys.executable)
elif __file__:
    application_path = os.path.dirname(__file__)

#config_path = os.path.join(application_path, config_name)

print('app path=',application_path)
application_path=application_path.replace('\\','/')
print('app path=',application_path)
game_folder = application_path
face_recog_folder=game_folder+'/'
img_folder =game_folder+'/'
print("img folder=",img_folder)
fps=60
file= open(game_folder+'/'+"highscore.txt",'r+')
highScore=file.read()
highScore=int(highScore)
cascPath =face_recog_folder+ "haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascPath)

video_capture = cv2.VideoCapture(0)

catch=0
pygame.init()

display_width = 1500
display_height = 800

gameDisplay = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption('CoronaVirusVaccine Game')

clock=pygame.time.Clock()
crashed = False

cam_error=pygame.image.load(img_folder+"cam_error.jpg")

#mask=pygame.image.load('C:/Crux/Dev/datasets/mygame/mask.png')
black = (0,0,0)
white = (255,255,255)
def text_objects(text, font):
    textSurface = font.render(text, True, black)
    return textSurface, textSurface.get_rect()
def message_display(text,x,y,catch):
    #largeText = pygame.font.Font('freesansbold.ttf',115)
    font = pygame.font.SysFont ("Arial", 35)
    largeText = font.render(text, True, (0, 128, 0)).convert_alpha()
    
    if highScore<catch:
        hs=catch
    else:
        hs=highScore
    hs="Highscore :"+str(hs)
    hs=font.render(hs, True, (0, 128, 0)).convert_alpha()
    gameDisplay.blit(largeText, (x,y))
    gameDisplay.blit(hs, (830,250))
    pygame.display.update()

x =  150
y = 150
x_change = 0
car_speed = 0
uncatch=0
carImg = pygame.image.load(img_folder+'bag.png').convert_alpha()
vaccine=pygame.image.load(img_folder+'vaccine.png').convert_alpha()
virus=pygame.image.load(img_folder+'virus.png').convert_alpha()
infected=pygame.image.load(img_folder+'infected.png').convert_alpha()
strong=pygame.image.load(img_folder+'strong.png').convert_alpha()
vacx=np.random.randint(0,display_width/2-100,100)
vacspeed=np.random.randint(10,19,30)
vacspeedf=np.random.randint(25,30,30)
vacspeedff=np.random.randint(50,70,30)

vacy=[0]*100
i=0
j=0
catch=0
crashed=False
message_display('Catch samples',100,100,catch)
message_display('to make corona vaccine',100,300,catch)

time.sleep(4)
while crashed==False:
    # Capture frame-by-frame
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            crashed = True
    #ret, frame = video_capture.read()
    
    while ((video_capture.isOpened())==False):
        gameDisplay.blit(cam_error, (display_width/2,display_height/2))
        pygame.display.update()
        time.sleep(3)
        video_capture = cv2.VideoCapture(0)
    ret, frame = video_capture.read()
    frame=cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    print(ret)
    print("\n\n")
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.05,
        minNeighbors=50,
        minSize=(30, 30),
        flags=cv2.CASCADE_SCALE_IMAGE
    )

    # Draw a rectangle around the faces
    
    for (x, y, w, h) in faces:
        print(x,y)
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        

    # Display the resulting frame
    #cv2.imshow('Video', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything is done, release the capture

    #print('not crashed')
        ############################
    x_change=0
    y_change=0
    z=50
    for (x,y,w,h) in faces:
        x_change=550-x
        y_change=y
        z=h
        ######################
    ##
   ##   
    if vacy[i]<=display_height or vacy[i+1]<=display_height or vacy[i+2]<=display_height:
        vacy[i]+=vacspeed[j]
        vacy[i+1]+=vacspeedf[j]
        vacy[i+2]+=vacspeedff[j]
    else:
        i=i+3 
        j+=1     
    #print('x=',x)
    gameDisplay.fill(black)
    gameDisplay.blit(carImg, (x_change,display_height-128))
    frame2 = np.rot90(frame)

    
    frame2 = pygame.surfarray.make_surface(frame2)
    gameDisplay.blit(vaccine, (vacx[i],vacy[i]))    
    gameDisplay.blit(vaccine, (vacx[i+1],vacy[i+1]))  
    gameDisplay.blit(vaccine, (vacx[i+2],vacy[i+2]))     
    gameDisplay.blit(frame2, (830,300))
    #gameDisplay.blit(mask, (650+x_change+10,300+y_change+z/2-25))
    pygame.display.update()
    
    if vacx[i]+100>=x_change and vacx[i]<=x_change+128 and vacy[i]>=display_height-240 and vacy[i]<=display_height:
        vacy[i]=2000
        vacx[i]=2000
        catch+=1
        message_display('Sample:'+str(catch),830,200,catch)
    elif (vacx[i]+100<x_change  or (vacx[i]>x_change+128 and vacx[i]<800)) and vacy[i]+vacspeed[j]>=display_height-20 and vacy[i]<=display_height:
        uncatch+=1
        vacy[i]=2000
        vacx[i]=2000
    elif uncatch>5:
        crashed=True
        gameDisplay.blit(infected, (830+x_change,300+y_change)) 
        message_display('Sample:'+str(catch),830,200,catch)
        pygame.display.update()
        time.sleep(2)
        


    if vacx[i+1]+100>=x_change and vacx[i+1]<=x_change+128 and vacy[i+1]>=display_height-240 and vacy[i+1]<=display_height:
        vacy[i+1]=2000
        vacx[i+1]=2000
        catch+=1
        message_display('Sample:'+str(catch),830,200,catch)
    elif (vacx[i+1]+100<x_change  or (vacx[i+1]>x_change+128 and vacx[i+1]<800)) and vacy[i+1]+vacspeedf[j]>=display_height-20 and vacy[i+1]<=display_height:
        uncatch+=1
        vacy[i+1]=2000
        vacx[i+1]=2000
    elif uncatch>5:
        crashed=True
        gameDisplay.blit(infected, (830+x_change,300+y_change)) 
        pygame.display.update()
        time.sleep(2)

    if vacx[i+2]+100>=x_change and vacx[i+2]<=x_change+128 and vacy[i+2]>=display_height-240 and vacy[i+2]<=display_height :
        vacy[i+1+1]=2000
        vacx[i+2]=2000
        catch+=1
        message_display('Sample:'+str(catch),830,200,catch)
    elif (vacx[i+1+1]+100<x_change  or (vacx[i+1+1]>x_change+128 and vacx[i+1+1]<800)) and vacy[i+1+1]+vacspeedff[j]>=display_height-20 and vacy[i+2]<=display_height:
        uncatch+=1
        vacy[i+2]=2000
        vacx[i+2]=2000
    elif uncatch>5:
        crashed=True
        gameDisplay.blit(infected, (830+x_change,300+y_change)) 
        pygame.display.update()
        time.sleep(2)
    #print('\n\t\t\ti=',i)
    #print("\n~~~~~~~~~~~~~~~~catches=",catch,"\tdropped=",uncatch)
    gameDisplay.blit(vaccine, (vacx[i],vacy[i]))    
    gameDisplay.blit(vaccine, (vacx[i+1],vacy[i+1]))  
    gameDisplay.blit(vaccine, (vacx[i+2],vacy[i+2])) 
    gameDisplay.blit(frame2, (830,300))  
    #gameDisplay.blit(mask, (650+x_change+15,300+y_change+z/2-25))
    k=1
    if uncatch>0:
        while ( k<=uncatch):
            gameDisplay.blit(virus, (830+128*k-128,10))
            k+=1  
    gameDisplay.blit(frame2, (830,300))
    #gameDisplay.blit(mask, (650+x_change+15,300+y_change+z/2-25))
    message_display('Sample:'+str(catch),830,200,catch)
    pygame.display.update()
    clock.tick(fps)
    if crashed==True:
        gameDisplay.blit(strong, (200,100))
        pygame.display.update()
        time.sleep(2)
    
if catch>highScore:
    file.seek(0)
    file.write(str(catch))

video_capture.release()    
cv2.destroyAllWindows()

def message_display(text):
    largeText = pygame.font.Font('freesansbold.ttf',115)
    TextSurf, TextRect = text_objects(text, largeText)
    TextRect.center = ((830+60),(200))
    gameDisplay.blit(TextSurf, TextRect)
    pygame.display.update()
