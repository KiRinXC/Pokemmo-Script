import cv2
import easyocr

# 读取图片
img = cv2.imread('PokeScript2-0/Pic/flash.png')

# 定义要识别的区域
x, y, w, h = 170,200,380,45
roi = img[y:y + h, x:x + w]
cv2.imwrite('roi_image.jpg', roi)
# 初始化 EasyOCR
reader = easyocr.Reader(['ch_sim', 'en'])

# 识别特定区域
result = reader.readtext(roi)

# 处理识别结果
for (bbox, text, prob) in result:
    print(f'Bounding Box: {bbox}')
    print(f'Text: {text}')
    print(f'Confidence: {prob}')
