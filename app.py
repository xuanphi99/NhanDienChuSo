
import pygame
from  process_image import get_output_image

# pre defined colors, pen radius and font color
black = [0, 0, 0]
white = [255, 255, 255]
red = [255, 0, 0]
green = [0, 255, 0]
draw_on = False
last_pos = (0, 0)
color = (255, 128, 0)
radius = 7
font_size = 500

#image size
width = 640
height = 640

# initializing screen
screen = pygame.display.set_mode((width*2, height))
screen.fill(white)
pygame.font.init()


# sau ảnh kết quả nên màn hình bên phải
def show_output_image(img):
    # khởi tạo 1 mảng giống mảng của ảnh
    surf = pygame.pixelcopy.make_surface(img)
    surf = pygame.transform.rotate(surf, -270)
    # thay đổi độ phân giải 0=false,true =1
    surf = pygame.transform.flip(surf, 0, 1)
    # hiện ảnh lên với width+2
    screen.blit(surf, (width+2, 0))

# cat ảnh để lưu
def crope(orginal):
    # cắt ảnh  với width =640 -5 ,.. 
    cropped = pygame.Surface((width-5, height-5))
    # cắt ảnh từ vị trí 0 ,0 tới (640-5 , 640-5)
    cropped.blit(orginal, (0, 0), (0, 0, width-5, height-5))
   
    return cropped

# vẽ số
def roundline(srf, color, start, end, radius=1):
    dx = end[0] - start[0]
    dy = end[1] - start[1]
    distance = max(abs(dx), abs(dy))
    for i in range(distance):
        x = int(start[0] + float(i) / distance * dx)
        y = int(start[1] + float(i) / distance * dy)
        pygame.draw.circle(srf, color, (x, y), radius)


def draw_partition_line():
    # vẽ dg thẳng ngăn cách draw và test
    pygame.draw.line(screen, black, [width, 0], [width,height ], 8)


try:
    while True:
        # get all events set vào biến e
        
        e = pygame.event.wait()
        draw_partition_line()

        # clear screen after right click
        # xóa màn hình khi click chuột phải button = 3
        if(e.type == pygame.MOUSEBUTTONDOWN and e.button == 3):
            screen.fill(white)

        # quit
        if e.type == pygame.QUIT:
            raise StopIteration

        # start drawing after left click
        # khi click chuột trái và dữ chuột vẽ
        if(e.type == pygame.MOUSEBUTTONDOWN and e.button != 3):
            # set cho text màu đen
            color = black
            # vẽ hình tròn lên screen với color = black , tạo độ và góc bo tròn  = 7
            pygame.draw.circle(screen, color, e.pos, radius)
            draw_on = True # đang vẽ

        # stop drawing after releasing left click
        #khi nhả chuột k vẽ
        if e.type == pygame.MOUSEBUTTONUP and e.button != 3:
            draw_on = False # dừng vẽ
            fname = "out.png" # tên file ảnh output sẽ lưu ra
            # hàm crop ảnh output
            img = crope(screen)
            # lưu  ảnh lại
            pygame.image.save(img, fname)
            # sau khi cắt đc ảnh vẽ thì đưa vào hàm xử lý ảnh nhận dangj
            output_img = get_output_image(fname)
            # đưa kết quả ra giao diện bên phải
            show_output_image(output_img)

        # start drawing line on screen if draw is true
        # bắt sự kiện di chuột là đang vẽ số
        if e.type == pygame.MOUSEMOTION:
            # nếu là vẽ
            if draw_on:
                # vẽ 
                pygame.draw.circle(screen, color, e.pos, radius)
                roundline(screen, color, e.pos, last_pos, radius)
            last_pos = e.pos

        pygame.display.flip()

except StopIteration:
    pass

pygame.quit()
